from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi import HTTPException, Response

from app.api.routers.auth import login
from app.application.auth.services.authentication_application_service import (
    AuthenticationApplicationService,
)
from app.application.auth.services.session_application_service import (
    SessionApplicationService,
)
from app.core.config import settings
from app.domains.auth.entities.session import Session
from app.domains.user.entities.user import User
from app.shared.unit_of_work.unit_of_work import UnitOfWork
from app.schemas.auth import LoginRequest


class FakeAuthenticationService:
    def __init__(self, user: User | None = None, error: Exception | None = None) -> None:
        self.user = user
        self.error = error

    def authenticate(self, command: object) -> User:
        if self.error is not None:
            raise self.error
        assert self.user is not None
        return self.user


class FakeSessionService:
    def __init__(self) -> None:
        self.created: Session | None = None

    def create(self, command: object) -> Session:
        self.created = Session(
            id=uuid4(),
            user_id=command.user_id,
            session_id="session-token",
            expires_at=command.now.replace(hour=(command.now.hour + 12) % 24),
        )
        return self.created


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True


def test_login_sets_http_only_session_cookie() -> None:
    user = User(
        id=uuid4(),
        username="alice",
        password_hash="$argon2id$secret",
    )
    authentication = FakeAuthenticationService(user=user)
    sessions = FakeSessionService()
    uow = FakeUnitOfWork()
    response = Response()

    result = login(
        data=LoginRequest(username="alice", password="password"),
        response=response,
        authentication_service=authentication,  # type: ignore[arg-type]
        session_service=sessions,  # type: ignore[arg-type]
        uow=uow,
    )

    assert result.id == user.id
    assert result.username == user.username
    assert "password_hash" not in result.model_dump()
    assert "session_id" not in result.model_dump()
    assert uow.committed is True

    set_cookie = response.headers["set-cookie"]
    assert f"{settings.AUTH_COOKIE_NAME}=session-token" in set_cookie
    assert "HttpOnly" in set_cookie
    assert f"Max-Age={settings.AUTH_SESSION_TTL_SECONDS}" in set_cookie


def test_login_returns_generic_401_for_authentication_failure() -> None:
    authentication = FakeAuthenticationService(
        error=Exception("authentication failed"),
    )
    response = Response()

    with pytest.raises(HTTPException) as exc_info:
        login(
            data=LoginRequest(username="missing", password="wrong"),
            response=response,
            authentication_service=authentication,  # type: ignore[arg-type]
            session_service=FakeSessionService(),  # type: ignore[arg-type]
            uow=FakeUnitOfWork(),
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid username or password"
