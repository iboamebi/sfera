"""
Session repository interface.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.domains.auth.entities.session import Session


class SessionRepository(ABC):
    """Abstract authenticated session repository."""

    @abstractmethod
    def save(self, session: Session) -> Session:
        """Persist an authenticated session."""

        raise NotImplementedError

    @abstractmethod
    def get_active(
        self,
        session_id: str,
        now: datetime,
    ) -> Session | None:
        """Get a non-revoked, non-expired session."""

        raise NotImplementedError

    @abstractmethod
    def revoke(self, session_id: str) -> None:
        """Revoke an authenticated session."""

        raise NotImplementedError

    @abstractmethod
    def revoke_all_for_user(self, user_id: UUID) -> None:
        """Revoke all sessions belonging to a user."""

        raise NotImplementedError
