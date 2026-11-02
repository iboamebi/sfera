"""Tests for user administration application service."""

from uuid import uuid4

import pytest

from app.application.auth.ports.password_hasher import PasswordHasher
from app.application.authorization.authorization import AuthorizationError
from app.application.user.commands.create_user import CreateUserCommand
from app.application.user.exceptions import UserAlreadyExistsApplicationError
from app.application.user.services.user_administration_application_service import (
    UserAdministrationApplicationService,
)
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUserRepository(UserRepository):
    def __init__(self, users: list[User]) -> None:
        self.users = users

    def get_by_id(self, user_id, include_archived: bool = False) -> User | None:
        return next((user for user in self.users if user.id == user_id), None)

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

    def save(self, user: User) -> User:
        self.users.append(user)
        return user


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
