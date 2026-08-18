from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from app.application.auth.commands.get_current_user import GetCurrentUserCommand
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.application.auth.services.current_user_application_service import (
    CurrentUserApplicationService,
)
from app.domains.auth.entities.session import Session
from app.domains.auth.repositories.session_repository import SessionRepository
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository


class FakeSessionRepository(SessionRepository):
    def __init__(self, session: Session | None = None) -> None:
        self.session = session

    def save(self, session: Session) -> Session:
        self.session = session
        return session

    def get_active(self, session_id: str, now: datetime) -> Session | None:
        if self.session is None or self.session.session_id != session_id:
            return None
        return self.session

    def revoke(self, session_id: str) -> None:
        if self.session is not None and self.session.session_id == session_id:
            self.session.revoke()

    def revoke_all_for_user(self, user_id: UUID) -> None:
        if self.session is not None and self.session.user_id == user_id:
            self.session.revoke()


class FakeUserRepository(UserRepository):
    def __init__(self, user: User | None = None) -> None:
        self.user = user

    def get_by_id(self, user_id: UUID, include_archived: bool = False) -> User | None:
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
        return None

    def save(self, user: User) -> User:
        self.user = user
        return user


def test_get_returns_user_for_active_session() -> None:
    user = User(id=uuid4(), username="alice", password_hash="hash")
    session = Session(
        id=uuid4(),
        user_id=user.id,
        session_id="session-1",
        expires_at=datetime(2026, 8, 19, 20, tzinfo=UTC),
    )
    service = CurrentUserApplicationService(
        FakeSessionRepository(session),
        FakeUserRepository(user),
    )

    result = service.get(
        GetCurrentUserCommand(
            session_id="session-1",
            now=datetime(2026, 8, 18, 20, tzinfo=UTC),
        ),
    )

    assert result.id == user.id
    assert result.username == "alice"


def test_get_rejects_missing_session() -> None:
    service = CurrentUserApplicationService(
        FakeSessionRepository(),
        FakeUserRepository(),
    )

    with pytest.raises(AuthenticationFailedApplicationError):
        service.get(
            GetCurrentUserCommand(
                session_id="missing",
                now=datetime(2026, 8, 18, 20, tzinfo=UTC),
            ),
        )


def test_get_rejects_archived_user() -> None:
    user = User(
        id=uuid4(),
        username="alice",
        password_hash="hash",
        archived=True,
    )
    session = Session(
        id=uuid4(),
        user_id=user.id,
        session_id="session-1",
        expires_at=datetime(2026, 8, 19, 20, tzinfo=UTC),
    )
    service = CurrentUserApplicationService(
        FakeSessionRepository(session),
        FakeUserRepository(user),
    )

    with pytest.raises(AuthenticationFailedApplicationError):
        service.get(
            GetCurrentUserCommand(
                session_id="session-1",
                now=datetime(2026, 8, 18, 20, tzinfo=UTC),
            ),
        )
