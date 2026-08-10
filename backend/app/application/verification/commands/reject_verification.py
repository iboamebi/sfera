"""
Reject verification command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RejectVerificationCommand:
    """Command to reject verification."""

    verification_id: UUID
    reason: str
