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
    """Create and manage authenticated sessions."""

    def __init__(
        self,
        repository: SessionRepository,
        token_generator: SessionTokenGenerator,
        ttl: timedelta = timedelta(hours=12),
    ) -> None:
        self._repository = repository
        self._token_generator = token_generator
        self._ttl = ttl

    def create(self, command: CreateSessionCommand) -> Session:
        """Create and persist an authenticated session."""

        session = Session(
            id=uuid4(),
            user_id=command.user_id,
            session_id=self._token_generator.generate(),
            expires_at=command.now + self._ttl,
        )
        return self._repository.save(session)

    def revoke(self, command: RevokeSessionCommand) -> None:
        """Revoke an authenticated session."""

        self._repository.revoke(command.session_id)
