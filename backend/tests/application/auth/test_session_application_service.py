from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from app.application.auth.commands.create_session import CreateSessionCommand
from app.application.auth.services.session_application_service import (
    SessionApplicationService,
)
from app.domains.auth.entities.session import Session
from app.domains.auth.repositories.session_repository import SessionRepository
from app.domains.auth.services.session_token_generator import SessionTokenGenerator


class FakeSessionRepository(SessionRepository):
    def __init__(self) -> None:
        self.saved: Session | None = None

    def save(self, session: Session) -> Session:
        self.saved = session
        return session

    def get_active(self, session_id: str, now: datetime) -> Session | None:
        return None

    def revoke(self, session_id: str) -> None:
        pass

    def revoke_all_for_user(self, user_id: UUID) -> None:
        pass


class FakeSessionTokenGenerator(SessionTokenGenerator):
    def generate(self) -> str:
        return "secure-session-token"


def test_create_persists_session_with_expiration() -> None:
    now = datetime(2026, 8, 18, 20, 0, tzinfo=UTC)
    user_id = uuid4()
    repository = FakeSessionRepository()
    service = SessionApplicationService(
        repository,
        FakeSessionTokenGenerator(),
        ttl=timedelta(hours=12),
    )

    session = service.create(
        CreateSessionCommand(
            user_id=user_id,
            now=now,
        ),
    )

    assert repository.saved is session
    assert session.user_id == user_id
    assert session.session_id == "secure-session-token"
    assert session.expires_at == now + timedelta(hours=12)
    assert session.revoked is False
