"""
Create verification command.
"""

from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)


@dataclass(frozen=True)
class CreateVerificationCommand:
    """Create verification data."""

    order_item_id: UUID
    verification_date: date
    result: VerificationResult
    valid_until: date | None = None
    unsuitable_reason: str | None = None
    methodology: str | None = None
