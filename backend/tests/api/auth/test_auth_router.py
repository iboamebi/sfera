from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException, Response

from app.api.routers.auth import change_password, login
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.core.config import settings
from app.domains.auth.entities.session import Session
from app.domains.user.entities.user import User
from app.schemas.auth import ChangePasswordRequest, LoginRequest
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




class FakeChangePasswordService:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.command = None

    def change(self, command: object) -> None:
        self.command = command
        if self.error is not None:
            raise self.error


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

    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        pass


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
    assert result.role == user.role
    assert result.must_change_password is False
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



def test_change_password_forwards_authenticated_user_and_passwords() -> None:
    user = User(
        id=uuid4(),
        username="alice",
        password_hash="temporary-hash",
        must_change_password=True,
    )
    service = FakeChangePasswordService()

    change_password(
        data=ChangePasswordRequest(
            current_password="temporary-password",
            new_password="new-password",
        ),
        user=user,
        service=service,
    )

    assert service.command.user_id == user.id
    assert service.command.current_password == "temporary-password"
    assert service.command.new_password == "new-password"


def test_change_password_maps_invalid_current_password_to_400() -> None:
    user = User(
        id=uuid4(),
        username="alice",
        password_hash="temporary-hash",
    )
    service = FakeChangePasswordService(
        error=AuthenticationFailedApplicationError(),
    )

    with pytest.raises(HTTPException) as exc_info:
        change_password(
            data=ChangePasswordRequest(
                current_password="wrong-password",
                new_password="new-password",
            ),
            user=user,
            service=service,
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Current password is incorrect"
