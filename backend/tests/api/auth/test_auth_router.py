from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException, Response

from app.api.routers.auth import login
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.core.config import settings
from app.domains.auth.entities.session import Session
from app.domains.user.entities.user import User
from app.schemas.auth import LoginRequest
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeAuthenticationService:
    def __init__(
        self,
        user: User | None = None,
        error: Exception | None = None,
    ) -> None:
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
            expires_at=command.now + timedelta(hours=12),
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
        authentication_service=authentication,
        session_service=sessions,
        uow=uow,
    )

    assert result.id == user.id
    assert result.username == user.username
    assert "password_hash" not in result.model_dump()
    assert "session_id" not in result.model_dump()
    assert uow.committed is True
    assert isinstance(result.id, UUID)

    set_cookie = response.headers["set-cookie"]
    assert f"{settings.AUTH_COOKIE_NAME}=session-token" in set_cookie
    assert "HttpOnly" in set_cookie
    assert f"Max-Age={settings.AUTH_SESSION_TTL_SECONDS}" in set_cookie


def test_login_returns_generic_401_for_authentication_failure() -> None:
    authentication = FakeAuthenticationService(
        error=AuthenticationFailedApplicationError(),
    )
    response = Response()

    with pytest.raises(HTTPException) as exc_info:
        login(
            data=LoginRequest(username="missing", password="wrong"),
            response=response,
            authentication_service=authentication,
            session_service=FakeSessionService(),
            uow=FakeUnitOfWork(),
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid username or password"
