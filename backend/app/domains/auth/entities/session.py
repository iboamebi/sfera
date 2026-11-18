"""
Domain entity: authenticated session.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class Session(Entity):
    """Server-managed authenticated session."""

    user_id: UUID
    session_id: str
    expires_at: datetime
    last_activity_at: datetime
    revoked: bool = False

    def revoke(self) -> None:
        """Invalidate the session."""

        self.revoked = True

    def record_activity(self, now: datetime) -> None:
        """Record the latest observed user activity without extending absolute TTL."""

        if now > self.last_activity_at:
            self.last_activity_at = now

    def is_valid(
        self,
        now: datetime,
        inactivity_timeout: timedelta = timedelta(hours=1),
    ) -> bool:
        """Return whether the session is active, not idle-expired, and not expired."""

        return (
            not self.revoked
            and self.expires_at > now
            and self.last_activity_at + inactivity_timeout > now
        )
