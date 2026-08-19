"""Tests for application authorization."""

from uuid import uuid4

import pytest

from app.application.authorization.authorization import (
    AuthorizationError,
    require_role,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole


def make_user(role: UserRole) -> User:
    return User(
        id=uuid4(),
        username="test-user",
        password_hash="hash",
        role=role,
    )


def test_require_role_allows_allowed_role() -> None:
    require_role(make_user(UserRole.OPERATOR), UserRole.OPERATOR)


def test_require_role_allows_admin() -> None:
    require_role(make_user(UserRole.ADMIN), UserRole.ADMIN, UserRole.OPERATOR)


def test_require_role_rejects_disallowed_role() -> None:
    with pytest.raises(AuthorizationError, match="not authorized"):
        require_role(make_user(UserRole.OPERATOR), UserRole.ADMIN)
