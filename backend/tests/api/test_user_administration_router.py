from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.api.routers.users import change_user_role, create_user, get_users
from app.application.user.exceptions import (
    UserAlreadyExistsApplicationError,
    UserNotFoundApplicationError,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.schemas.user import UserCreate, UserRoleUpdate


class FakeUserAdministrationService:
    def __init__(self) -> None:
        self.users: list[User] = []
        self.created: User | None = None
        self.temporary_password = "temporary-password"
        self.create_error: Exception | None = None
        self.include_archived = False
        self.actor: User | None = None
        self.role_change_error: Exception | None = None

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
