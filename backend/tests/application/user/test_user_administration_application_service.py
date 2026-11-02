"""Tests for user administration application service."""

from uuid import uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.user.services.user_administration_application_service import (
    UserAdministrationApplicationService,
)
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository
from app.domains.user.value_objects.user_role import UserRole


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
        return next((user for user in self.users if user.username == username), None)

    def get_all(self, include_archived: bool = False) -> list[User]:
        return [user for user in self.users if include_archived or not user.archived]

    def save(self, user: User) -> User:
        return user


def make_user(username: str, role: UserRole = UserRole.OPERATOR) -> User:
    return User(
        id=uuid4(),
        username=username,
        password_hash="hash",
        role=role,
    )


def test_get_all_requires_admin_role() -> None:
    repository = FakeUserRepository([make_user("operator")])
    service = UserAdministrationApplicationService(repository)

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.get_all(make_user("operator", UserRole.OPERATOR))


def test_admin_can_list_users_including_inactive_accounts() -> None:
    active = make_user("active")
    inactive = make_user("inactive")
    inactive.deactivate()
    archived = make_user("archived")
    archived.archive()
    repository = FakeUserRepository([inactive, archived, active])
    service = UserAdministrationApplicationService(repository)

    users = service.get_all(make_user("admin", UserRole.ADMIN))

    assert users == [inactive, active]
    assert archived not in users


def test_admin_can_include_archived_users() -> None:
    archived = make_user("archived")
    archived.archive()
    repository = FakeUserRepository([archived])
    service = UserAdministrationApplicationService(repository)

    users = service.get_all(
        make_user("admin", UserRole.ADMIN),
        include_archived=True,
    )

    assert users == [archived]
