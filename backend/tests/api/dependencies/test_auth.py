from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.api.dependencies.auth import (
    get_current_user,
    require_password_change_completed,
)
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.domains.user.entities.user import User


class FakeService:
    def __init__(
        self,
        user: User | None = None,
        error: Exception | None = None,
    ) -> None:
        self.user = user
        self.error = error
        self.command = None

    def get(self, command: object) -> User:
        self.command = command
        if self.error is not None:
            raise self.error
        assert self.user is not None
        return self.user


def test_get_current_user_rejects_missing_session_cookie() -> None:
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(session_id=None, service=FakeService())

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Authentication required"


def test_get_current_user_returns_user_from_application_service() -> None:
    user = User(
        id=uuid4(),
        username="alice",
        password_hash="secret",
    )
    service = FakeService(user=user)

    result = get_current_user(
        session_id="session-token",
        service=service,
    )

    assert result is user
    assert service.command.session_id == "session-token"
    assert service.command.now.tzinfo == UTC
    assert isinstance(service.command.now, datetime)


def test_get_current_user_maps_authentication_failure_to_401() -> None:
    service = FakeService(error=AuthenticationFailedApplicationError())

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            session_id="expired-session",
            service=service,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Authentication required"


def test_first_login_user_is_blocked_from_business_endpoints() -> None:
    user = User(
        id=uuid4(),
        username="alice",
        password_hash="secret",
        must_change_password=True,
    )

    with pytest.raises(HTTPException) as exc_info:
        require_password_change_completed(user=user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Password change required"


def test_user_with_changed_password_can_access_business_endpoints() -> None:
    user = User(
        id=uuid4(),
        username="alice",
        password_hash="secret",
        must_change_password=False,
    )

    result = require_password_change_completed(user=user)

    assert result is None
