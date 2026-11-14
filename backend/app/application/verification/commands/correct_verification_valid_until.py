"""
Correct a decided Verification validity date.
"""

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class CorrectVerificationValidUntilCommand:
    """Command to correct a suitable Verification validity date."""

    verification_id: UUID
    valid_until: date
    reason: str
