"""
Command: get current authenticated user.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class GetCurrentUserCommand:
    """Resolve the user associated with an authenticated session."""

    session_id: str
    now: datetime
