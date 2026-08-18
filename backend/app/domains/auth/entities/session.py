"""
Domain entity: authenticated session.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class Session(Entity):
    """Server-managed authenticated session."""

    user_id: UUID
    session_id: str
    expires_at: datetime
    revoked: bool = False

    def revoke(self) -> None:
        """Invalidate the session."""

        self.revoked = True

    def is_valid(self, now: datetime) -> bool:
        """Return whether the session is currently valid."""

        return not self.revoked and self.expires_at > now
