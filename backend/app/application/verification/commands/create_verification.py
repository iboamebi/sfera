"""
Create verification command.
"""

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class CreateVerificationCommand:
    """Create verification data before the final decision."""

    order_item_id: UUID
    verification_date: date
    methodology: str | None = None
