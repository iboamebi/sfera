"""
Create verification command.
"""

from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.domains.verification.value_objects.verification_type import VerificationType


@dataclass(frozen=True)
class CreateVerificationCommand:
    """Create verification data before the final decision."""

    order_item_id: UUID
    verification_date: date
    verification_type: VerificationType
    methodology: str | None = None
