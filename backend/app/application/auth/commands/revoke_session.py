"""
Command: revoke an authenticated session.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RevokeSessionCommand:
    """Revoke an authenticated server-side session."""

    session_id: str
