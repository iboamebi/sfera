"""
Command: create authenticated session.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateSessionCommand:
    """Create an authenticated server-side session."""

    user_id: UUID
    now: datetime
