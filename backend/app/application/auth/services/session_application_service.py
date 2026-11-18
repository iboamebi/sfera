"""
Application service: Authenticated sessions.
"""

from datetime import timedelta
from uuid import uuid4

from app.application.auth.commands.create_session import CreateSessionCommand
from app.application.auth.commands.revoke_session import RevokeSessionCommand
from app.domains.auth.entities.session import Session
from app.domains.auth.repositories.session_repository import SessionRepository
from app.domains.auth.services.session_token_generator import SessionTokenGenerator


class SessionApplicationService:
    """Create, track, and revoke authenticated sessions."""

    def __init__(
        self,
        repository: SessionRepository,
        token_generator: SessionTokenGenerator,
        ttl: timedelta = timedelta(hours=12),
        inactivity_timeout: timedelta = timedelta(hours=1),
    ) -> None:
        self._repository = repository
        self._token_generator = token_generator
        self._ttl = ttl
        self._inactivity_timeout = inactivity_timeout

    def create(self, command: CreateSessionCommand) -> Session:
        """Create and persist an authenticated session."""

        session = Session(
            id=uuid4(),
            user_id=command.user_id,
            session_id=self._token_generator.generate(),
            expires_at=command.now + self._ttl,
            last_activity_at=command.now,
        )
        return self._repository.save(session)

    def record_activity(self, session_id: str, now) -> bool:
        """Record activity only for a session that has not expired or gone idle."""

        session = self._repository.get_active(session_id, now)
        if session is None or not session.is_valid(now, self._inactivity_timeout):
            return False

        session.record_activity(now)
        self._repository.save(session)
        return True

    def revoke(self, command: RevokeSessionCommand) -> None:
        """Revoke an authenticated session."""

        self._repository.revoke(command.session_id)
