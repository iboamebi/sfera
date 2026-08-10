"""
Approve verification command.
"""

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class ApproveVerificationCommand:
    """Command to approve verification."""

    verification_id: UUID
    valid_until: date
