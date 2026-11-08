"""Tests for user administration application service."""

from uuid import uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.user.commands.archive_user import ArchiveUserCommand
from app.application.user.commands.change_user_role import ChangeUserRoleCommand
from app.application.user.commands.create_user import CreateUserCommand
from app.application.user.commands.reset_user_password import (
    ResetUserPasswordCommand,
)
from app.application.user.commands.restore_user import RestoreUserCommand
from app.application.user.commands.set_user_active import SetUserActiveCommand
from app.application.user.exceptions import (
    LastActiveAdministratorApplicationError,
    UserAlreadyExistsApplicationError,
    UserNotFoundApplicationError,
)
from app.application.user.services.user_administration_application_service import (
    UserAdministrationApplicationService,
)
from app.domains.auth.repositories.session_repository import SessionRepository
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository
from app.domains.user.value_objects.user_role import UserRole
from app.shared.password_hasher import PasswordHasher
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUserRepository(UserRepository):
    def __init__(self, users: list[User]) -> None:
        self.users = users

    def get_by_id(self, user_id, include_archived: bool = False) -> User | None:
        return next(
            (
                user
                for user in self.users
                if user.id == user_id
                and (
                    include_archived
                    or (not user.archived and user.is_active)
                )
            ),
            None,
        )

    def get_by_username(
        self,
        username: str,
        include_archived: bool = False,
    ) -> User | None:
        return next(
            (user for user in self.users if user.username == username),
            None,
        )

    def get_all(self, include_archived: bool = False) -> list[User]:
        return [user for user in self.users if include_archived or not user.archived]

    def get_all_for_update(self) -> list[User]:
        return list(self.users)

    def save(self, user: User) -> User:
        for index, existing in enumerate(self.users):
            if existing.id == user.id:
                self.users[index] = user
                return user
        self.users.append(user)
        return user


class FakeSessionRepository(SessionRepository):
    def __init__(self) -> None:
        self.revoked_user_ids = []

    def save(self, session):
        return session

    def get_active(self, session_id, now):
        return None

    def revoke(self, session_id):
        pass

    def revoke_all_for_user(self, user_id) -> None:
        self.revoked_user_ids.append(user_id)


class FixedPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return "argon2-hash-value"

    def verify(self, password: str, password_hash: str) -> bool:
        return False


class FakePasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return f"argon2-hash:{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password_hash == f"argon2-hash:{password}"


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def register_aggregate(self, aggregate, operation_id=None) -> None:
        pass


def make_user(username: str, role: UserRole = UserRole.OPERATOR) -> User:
    return User(
        id=uuid4(),
        username=username,
        password_hash="hash",
        role=role,
    )


def make_service(
    users: list[User],
) -> tuple[UserAdministrationApplicationService, FakeUserRepository, FakeUnitOfWork]:
    repository = FakeUserRepository(users)
    uow = FakeUnitOfWork()
    service = UserAdministrationApplicationService(
        repository,
        FakePasswordHasher(),
        uow,
        FakeSessionRepository(),
    )
    return service, repository, uow


def test_get_all_requires_admin_role() -> None:
    service, _, _ = make_service([make_user("operator")])

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.get_all(make_user("operator", UserRole.OPERATOR))


def test_admin_can_list_users_including_inactive_accounts() -> None:
    active = make_user("active")
    inactive = make_user("inactive")
    inactive.deactivate()
    archived = make_user("archived")
    archived.archive()
    service, _, _ = make_service([inactive, archived, active])

    users = service.get_all(make_user("admin", UserRole.ADMIN))

    assert users == [inactive, active]
    assert archived not in users


def test_admin_can_include_archived_users() -> None:
    archived = make_user("archived")
    archived.archive()
    service, _, _ = make_service([archived])

    users = service.get_all(
        make_user("admin", UserRole.ADMIN),
        include_archived=True,
    )

    assert users == [archived]


def test_change_role_updates_existing_user_and_commits() -> None:
    target = make_user("operator")
    service, repository, uow = make_service([target])

    updated = service.change_role(
        ChangeUserRoleCommand(user_id=target.id, role=UserRole.ADMIN),
        make_user("admin", UserRole.ADMIN),
    )

    assert updated.role is UserRole.ADMIN
    assert repository.users == [updated]
    assert uow.committed is True


def test_change_role_requires_admin_role() -> None:
    target = make_user("operator")
    service, repository, uow = make_service([target])

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.change_role(
            ChangeUserRoleCommand(user_id=target.id, role=UserRole.ADMIN),
            make_user("operator", UserRole.OPERATOR),
        )

    assert target.role is UserRole.OPERATOR
    assert uow.committed is False


def test_change_role_raises_when_user_does_not_exist() -> None:
    service, repository, uow = make_service([])

    with pytest.raises(UserNotFoundApplicationError):
        service.change_role(
            ChangeUserRoleCommand(user_id=uuid4(), role=UserRole.ADMIN),
            make_user("admin", UserRole.ADMIN),
        )

    assert repository.users == []
    assert uow.committed is False
    assert uow.rolled_back is True


def test_set_active_deactivates_existing_user_and_commits() -> None:
    target = make_user("operator")
    service, repository, uow = make_service([target])

    updated = service.set_active(
        SetUserActiveCommand(user_id=target.id, is_active=False),
        make_user("admin", UserRole.ADMIN),
    )

    assert updated.is_active is False
    assert repository.users == [updated]
    assert uow.committed is True


def test_set_active_activates_existing_user_and_commits() -> None:
    target = make_user("operator")
    target.deactivate()
    service, repository, uow = make_service([target])

    updated = service.set_active(
        SetUserActiveCommand(user_id=target.id, is_active=True),
        make_user("admin", UserRole.ADMIN),
    )

    assert updated.is_active is True
    assert repository.users == [updated]
    assert uow.committed is True


def test_set_active_requires_admin_role() -> None:
    target = make_user("operator")
    service, _, uow = make_service([target])

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.set_active(
            SetUserActiveCommand(user_id=target.id, is_active=False),
            make_user("operator", UserRole.OPERATOR),
        )

    assert target.is_active is True
    assert uow.committed is False


def test_set_active_rejects_archived_user() -> None:
    target = make_user("archived")
    target.archive()
    service, _, uow = make_service([target])

    with pytest.raises(UserNotFoundApplicationError):
        service.set_active(
            SetUserActiveCommand(user_id=target.id, is_active=True),
            make_user("admin", UserRole.ADMIN),
        )

    assert target.is_active is True
    assert uow.committed is False
    assert uow.rolled_back is True


def test_archive_user_marks_account_archived_and_commits() -> None:
    target = make_user("operator")
    service, repository, uow = make_service([target])

    updated = service.archive(
        ArchiveUserCommand(user_id=target.id),
        make_user("admin", UserRole.ADMIN),
    )

    assert updated.archived is True
    assert repository.users == [updated]
    assert uow.committed is True


def test_archive_user_requires_admin_role() -> None:
    target = make_user("operator")
    service, _, uow = make_service([target])

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.archive(
            ArchiveUserCommand(user_id=target.id),
            make_user("operator", UserRole.OPERATOR),
        )

    assert target.archived is False
    assert uow.committed is False


def test_archive_user_rejects_already_archived_account() -> None:
    target = make_user("archived")
    target.archive()
    service, _, uow = make_service([target])

    with pytest.raises(UserNotFoundApplicationError):
        service.archive(
            ArchiveUserCommand(user_id=target.id),
            make_user("admin", UserRole.ADMIN),
        )

    assert uow.committed is False
    assert uow.rolled_back is True


def test_restore_user_unarchives_account_and_commits() -> None:
    target = make_user("archived")
    target.archive()
    service, repository, uow = make_service([target])

    updated = service.restore(
        RestoreUserCommand(user_id=target.id),
        make_user("admin", UserRole.ADMIN),
    )

    assert updated.archived is False
    assert repository.users == [updated]
    assert uow.committed is True


def test_restore_user_requires_admin_role() -> None:
    target = make_user("archived")
    target.archive()
    service, _, uow = make_service([target])

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.restore(
            RestoreUserCommand(user_id=target.id),
            make_user("operator", UserRole.OPERATOR),
        )

    assert target.archived is True
    assert uow.committed is False


def test_restore_user_rejects_non_archived_account() -> None:
    target = make_user("operator")
    service, _, uow = make_service([target])

    with pytest.raises(UserNotFoundApplicationError):
        service.restore(
            RestoreUserCommand(user_id=target.id),
            make_user("admin", UserRole.ADMIN),
        )

    assert target.archived is False
    assert uow.committed is False
    assert uow.rolled_back is True


def test_create_user_generates_temporary_password_and_requires_change() -> None:
    service, repository, uow = make_service([])
    admin = make_user("admin", UserRole.ADMIN)

    user, temporary_password = service.create(
        CreateUserCommand(username="new-user", role=UserRole.METROLOGIST),
        admin,
    )

    assert user.username == "new-user"
    assert user.role is UserRole.METROLOGIST
    assert user.must_change_password is True
    assert user.password_hash == f"argon2-hash:{temporary_password}"
    assert temporary_password
    assert user in repository.users
    assert uow.committed is True


def test_create_user_requires_admin_role() -> None:
    service, repository, uow = make_service([])

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.create(
            CreateUserCommand(username="new-user", role=UserRole.OPERATOR),
            make_user("operator", UserRole.OPERATOR),
        )

    assert repository.users == []
    assert uow.committed is False


def test_create_user_rejects_existing_username_even_if_archived() -> None:
    existing = make_user("existing")
    existing.archive()
    service, repository, uow = make_service([existing])

    with pytest.raises(UserAlreadyExistsApplicationError):
        service.create(
            CreateUserCommand(username="existing", role=UserRole.OPERATOR),
            make_user("admin", UserRole.ADMIN),
        )

    assert repository.users == [existing]
    assert uow.committed is False



def test_archive_rejects_last_active_administrator() -> None:
    admin = make_user("admin", UserRole.ADMIN)
    service, _, uow = make_service([admin])

    with pytest.raises(LastActiveAdministratorApplicationError):
        service.archive(
            ArchiveUserCommand(user_id=admin.id),
            admin,
        )

    assert admin.archived is False
    assert uow.committed is False
    assert uow.rolled_back is True


def test_deactivate_rejects_last_active_administrator() -> None:
    admin = make_user("admin", UserRole.ADMIN)
    service, _, uow = make_service([admin])

    with pytest.raises(LastActiveAdministratorApplicationError):
        service.set_active(
            SetUserActiveCommand(user_id=admin.id, is_active=False),
            admin,
        )

    assert admin.is_active is True
    assert uow.committed is False
    assert uow.rolled_back is True


def test_demote_rejects_last_active_administrator() -> None:
    admin = make_user("admin", UserRole.ADMIN)
    service, _, uow = make_service([admin])

    with pytest.raises(LastActiveAdministratorApplicationError):
        service.change_role(
            ChangeUserRoleCommand(user_id=admin.id, role=UserRole.OPERATOR),
            admin,
        )

    assert admin.role is UserRole.ADMIN
    assert uow.committed is False
    assert uow.rolled_back is True


def test_admin_lifecycle_change_is_allowed_when_another_active_admin_exists() -> None:
    admin = make_user("admin", UserRole.ADMIN)
    second_admin = make_user("second-admin", UserRole.ADMIN)
    service, _, uow = make_service([admin, second_admin])

    updated = service.archive(
        ArchiveUserCommand(user_id=admin.id),
        second_admin,
    )

    assert updated.archived is True
    assert second_admin.is_active is True
    assert uow.committed is True


def test_inactive_administrator_does_not_count_as_available_admin() -> None:
    admin = make_user("admin", UserRole.ADMIN)
    inactive_admin = make_user("inactive-admin", UserRole.ADMIN)
    inactive_admin.deactivate()
    service, _, uow = make_service([admin, inactive_admin])

    with pytest.raises(LastActiveAdministratorApplicationError):
        service.archive(
            ArchiveUserCommand(user_id=admin.id),
            admin,
        )

    assert admin.archived is False
    assert uow.committed is False



def test_reset_password_generates_temporary_password_and_revokes_sessions() -> None:
    target = make_user("operator")
    service, repository, uow = make_service([target])
    service._password_hasher = FixedPasswordHasher()

    updated, temporary_password = service.reset_password(
        ResetUserPasswordCommand(user_id=target.id),
        make_user("admin", UserRole.ADMIN),
    )

    assert updated is target
    assert updated.must_change_password is True
    assert updated.password_hash == "argon2-hash-value"
    assert updated.password_hash != temporary_password
    assert repository.users == [updated]
    assert service._session_repository.revoked_user_ids == [target.id]
    assert uow.committed is True


def test_reset_password_requires_admin_role() -> None:
    target = make_user("operator")
    service, _, uow = make_service([target])

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.reset_password(
            ResetUserPasswordCommand(user_id=target.id),
            make_user("operator", UserRole.OPERATOR),
        )

    assert target.password_hash == "hash"
    assert service._session_repository.revoked_user_ids == []
    assert uow.committed is False


def test_reset_password_rejects_missing_or_inactive_user() -> None:
    target = make_user("operator")
    target.deactivate()
    service, _, uow = make_service([target])

    with pytest.raises(UserNotFoundApplicationError):
        service.reset_password(
            ResetUserPasswordCommand(user_id=target.id),
            make_user("admin", UserRole.ADMIN),
        )

    assert target.password_hash == "hash"
    assert service._session_repository.revoked_user_ids == []
    assert uow.committed is False
    assert uow.rolled_back is True
