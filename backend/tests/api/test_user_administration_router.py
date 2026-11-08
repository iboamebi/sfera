from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.api.routers.users import (
    archive_user,
    change_user_role,
    create_user,
    get_users,
    restore_user,
    reset_user_password,
    set_user_active,
)
from app.application.user.exceptions import (
    LastActiveAdministratorApplicationError,
    UserAlreadyExistsApplicationError,
    UserNotFoundApplicationError,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.schemas.user import UserActiveUpdate, UserCreate, UserRoleUpdate


class FakeUserAdministrationService:
    def __init__(self) -> None:
        self.users: list[User] = []
        self.created: User | None = None
        self.temporary_password = "temporary-password"
        self.create_error: Exception | None = None
        self.include_archived = False
        self.actor: User | None = None
        self.role_change_error: Exception | None = None
        self.status_change_error: Exception | None = None
        self.archive_error: Exception | None = None
        self.restore_error: Exception | None = None
        self.reset_error: Exception | None = None

    def get_all(
        self,
        user: User,
        include_archived: bool = False,
    ) -> list[User]:
        self.actor = user
        self.include_archived = include_archived
        return self.users

    def change_role(self, command: object, actor: User) -> User:
        self.actor = actor
        if self.role_change_error is not None:
            raise self.role_change_error
        target = next(user for user in self.users if user.id == command.user_id)
        target.change_role(command.role)
        return target

    def set_active(self, command: object, actor: User) -> User:
        self.actor = actor
        if self.status_change_error is not None:
            raise self.status_change_error
        target = next(user for user in self.users if user.id == command.user_id)
        if command.is_active:
            target.activate()
        else:
            target.deactivate()
        return target

    def archive(self, command: object, actor: User) -> User:
        self.actor = actor
        if self.archive_error is not None:
            raise self.archive_error
        target = next(user for user in self.users if user.id == command.user_id)
        target.archive()
        return target

    def restore(self, command: object, actor: User) -> User:
        self.actor = actor
        if self.restore_error is not None:
            raise self.restore_error
        target = next(user for user in self.users if user.id == command.user_id)
        target.restore()
        return target

    def reset_password(self, command: object, actor: User) -> tuple[User, str]:
        self.actor = actor
        if self.reset_error is not None:
            raise self.reset_error
        target = next(user for user in self.users if user.id == command.user_id)
        target.must_change_password = True
        return target, self.temporary_password

    def create(self, command: object, actor: User) -> tuple[User, str]:
        self.actor = actor
        if self.create_error is not None:
            raise self.create_error
        self.created = User(
            id=uuid4(),
            username=command.username,
            password_hash="$argon2id$hashed",
            role=command.role,
            must_change_password=True,
        )
        return self.created, self.temporary_password


def make_user(role: UserRole = UserRole.ADMIN) -> User:
    return User(
        id=uuid4(),
        username="admin",
        password_hash="$argon2id$hashed",
        role=role,
    )


def test_get_users_forwards_actor_and_archived_filter() -> None:
    actor = make_user()
    service = FakeUserAdministrationService()
    service.users = [make_user()]

    result = get_users(
        include_archived=True,
        user=actor,
        service=service,
    )

    assert result == service.users
    assert service.actor is actor
    assert service.include_archived is True


def test_change_user_role_returns_updated_user() -> None:
    actor = make_user()
    target = User(
        id=uuid4(),
        username="operator-1",
        password_hash="$argon2id$hashed",
        role=UserRole.OPERATOR,
    )
    service = FakeUserAdministrationService()
    service.users = [target]

    result = change_user_role(
        user_id=target.id,
        data=UserRoleUpdate(role=UserRole.ADMIN),
        actor=actor,
        service=service,
    )

    assert result.id == target.id
    assert result.role is UserRole.ADMIN
    assert service.actor is actor


def test_change_user_role_maps_missing_user_to_404() -> None:
    service = FakeUserAdministrationService()
    service.role_change_error = UserNotFoundApplicationError()

    with pytest.raises(HTTPException) as exc_info:
        change_user_role(
            user_id=uuid4(),
            data=UserRoleUpdate(role=UserRole.ADMIN),
            actor=make_user(),
            service=service,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_set_user_active_returns_updated_account_state() -> None:
    actor = make_user()
    target = User(
        id=uuid4(),
        username="operator-1",
        password_hash="$argon2id$hashed",
        role=UserRole.OPERATOR,
    )
    service = FakeUserAdministrationService()
    service.users = [target]

    result = set_user_active(
        user_id=target.id,
        data=UserActiveUpdate(is_active=False),
        actor=actor,
        service=service,
    )

    assert result.id == target.id
    assert result.is_active is False
    assert service.actor is actor


def test_set_user_active_maps_missing_user_to_404() -> None:
    service = FakeUserAdministrationService()
    service.status_change_error = UserNotFoundApplicationError()

    with pytest.raises(HTTPException) as exc_info:
        set_user_active(
            user_id=uuid4(),
            data=UserActiveUpdate(is_active=True),
            actor=make_user(),
            service=service,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_archive_user_returns_archived_account() -> None:
    actor = make_user()
    target = User(
        id=uuid4(),
        username="operator-1",
        password_hash="$argon2id$hashed",
        role=UserRole.OPERATOR,
    )
    service = FakeUserAdministrationService()
    service.users = [target]

    result = archive_user(
        user_id=target.id,
        actor=actor,
        service=service,
    )

    assert result.id == target.id
    assert result.archived is True
    assert service.actor is actor


def test_archive_user_maps_missing_user_to_404() -> None:
    service = FakeUserAdministrationService()
    service.archive_error = UserNotFoundApplicationError()

    with pytest.raises(HTTPException) as exc_info:
        archive_user(user_id=uuid4(), actor=make_user(), service=service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_restore_user_returns_restored_account() -> None:
    actor = make_user()
    target = User(
        id=uuid4(),
        username="operator-1",
        password_hash="$argon2id$hashed",
        role=UserRole.OPERATOR,
        archived=True,
    )
    service = FakeUserAdministrationService()
    service.users = [target]

    result = restore_user(
        user_id=target.id,
        actor=actor,
        service=service,
    )

    assert result.id == target.id
    assert result.archived is False
    assert service.actor is actor


def test_restore_user_maps_missing_user_to_404() -> None:
    service = FakeUserAdministrationService()
    service.restore_error = UserNotFoundApplicationError()

    with pytest.raises(HTTPException) as exc_info:
        restore_user(user_id=uuid4(), actor=make_user(), service=service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_create_user_returns_temporary_password_and_account_state() -> None:
    actor = make_user()
    service = FakeUserAdministrationService()

    result = create_user(
        data=UserCreate(username="operator-1", role=UserRole.OPERATOR),
        actor=actor,
        service=service,
    )

    assert result.username == "operator-1"
    assert result.role == UserRole.OPERATOR
    assert result.must_change_password is True
    assert result.temporary_password == "temporary-password"
    assert "password_hash" not in result.model_dump()
    assert service.actor is actor


def test_create_user_maps_duplicate_username_to_conflict() -> None:
    service = FakeUserAdministrationService()
    service.create_error = UserAlreadyExistsApplicationError()

    with pytest.raises(HTTPException) as exc_info:
        create_user(
            data=UserCreate(username="existing", role=UserRole.OPERATOR),
            actor=make_user(),
            service=service,
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Username already exists"



@pytest.mark.parametrize(
    ("operation", "error_attribute"),
    [
        ("role", "role_change_error"),
        ("status", "status_change_error"),
        ("archive", "archive_error"),
    ],
)
def test_last_active_administrator_conflict_maps_to_409(
    operation: str,
    error_attribute: str,
) -> None:
    service = FakeUserAdministrationService()
    setattr(service, error_attribute, LastActiveAdministratorApplicationError())
    target_id = uuid4()

    with pytest.raises(HTTPException) as exc_info:
        if operation == "role":
            change_user_role(
                user_id=target_id,
                data=UserRoleUpdate(role=UserRole.OPERATOR),
                actor=make_user(),
                service=service,
            )
        elif operation == "status":
            set_user_active(
                user_id=target_id,
                data=UserActiveUpdate(is_active=False),
                actor=make_user(),
                service=service,
            )
        else:
            archive_user(
                user_id=target_id,
                actor=make_user(),
                service=service,
            )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "At least one active administrator must remain"

def test_reset_user_password_returns_one_time_password() -> None:
    actor = make_user()
    target = User(
        id=uuid4(),
        username="operator-1",
        password_hash="$argon2id$hashed",
        role=UserRole.OPERATOR,
    )
    service = FakeUserAdministrationService()
    service.users = [target]

    result = reset_user_password(user_id=target.id, actor=actor, service=service)

    assert result.username == "operator-1"
    assert result.must_change_password is True
    assert result.temporary_password == "temporary-password"
    assert "password_hash" not in result.model_dump()
    assert service.actor is actor


def test_reset_user_password_maps_missing_user_to_404() -> None:
    service = FakeUserAdministrationService()
    service.reset_error = UserNotFoundApplicationError()

    with pytest.raises(HTTPException) as exc_info:
        reset_user_password(user_id=uuid4(), actor=make_user(), service=service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
