"""
Tests for Authentication application service.
"""

from uuid import uuid4

import pytest

from app.application.auth.commands.authenticate_user import (
    AuthenticateUserCommand,
)
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.application.auth.ports.password_hasher import PasswordHasher
from app.application.auth.services.authentication_application_service import (
    AuthenticationApplicationService,
)
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository


class FakePasswordHasher(PasswordHasher):
    def __init__(self, valid_password: str) -> None:
        self.valid_password = valid_password

    def verify(self, password: str, password_hash: str) -> bool:
        return password == self.valid_password and password_hash == "stored-hash"


class FakeUserRepository(UserRepository):
    def __init__(self, user: User | None = None) -> None:
        self.user = user

    def get_by_id(
        self,
        user_id,
        include_archived: bool = False,
    ) -> User | None:
        if self.user is None or self.user.id != user_id:
            return None

        if self.user.archived and not include_archived:
            return None

        return self.user

    def get_by_username(
        self,
        username: str,
        include_archived: bool = False,
    ) -> User | None:
        if self.user is None or self.user.username != username:
            return None

        if self.user.archived and not include_archived:
            return None

        return self.user

    def save(self, user: User) -> User:
        self.user = user
        return user


def test_authenticate_user_returns_user_for_valid_credentials():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="stored-hash",
    )
    service = AuthenticationApplicationService(
        FakeUserRepository(user),
        FakePasswordHasher("secret"),
    )

    authenticated = service.authenticate(
        AuthenticateUserCommand(
            username="admin",
            password="secret",
        )
    )

    assert authenticated is user


def test_authenticate_user_rejects_invalid_password():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="stored-hash",
    )
    service = AuthenticationApplicationService(
        FakeUserRepository(user),
        FakePasswordHasher("secret"),
    )

    with pytest.raises(AuthenticationFailedApplicationError):
        service.authenticate(
            AuthenticateUserCommand(
                username="admin",
                password="wrong",
            )
        )


def test_authenticate_user_rejects_missing_user():
    service = AuthenticationApplicationService(
        FakeUserRepository(),
        FakePasswordHasher("secret"),
    )

    with pytest.raises(AuthenticationFailedApplicationError):
        service.authenticate(
            AuthenticateUserCommand(
                username="missing",
                password="secret",
            )
        )


def test_authenticate_user_rejects_archived_user():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="stored-hash",
        archived=True,
    )
    service = AuthenticationApplicationService(
        FakeUserRepository(user),
        FakePasswordHasher("secret"),
    )

    with pytest.raises(AuthenticationFailedApplicationError):
        service.authenticate(
            AuthenticateUserCommand(
                username="admin",
                password="secret",
            )
        )
