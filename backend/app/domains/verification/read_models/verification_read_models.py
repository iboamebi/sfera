"""
Verification read models.
"""

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.domains.verification.value_objects.verification_type import VerificationType


@dataclass(frozen=True)
class VerificationListReadData:
    """Read data for the general Verification list."""

    id: UUID
    order_item_id: UUID
    order_id: UUID
    order_number: str
    customer_id: UUID
    customer_name: str
    instrument_id: UUID | None
    instrument_name: str | None
    instrument_type_id: UUID | None
    instrument_type_name: str | None
    serial_number: str | None
    verification_date: date
    verification_type: VerificationType
    status: VerificationStatus
    result: VerificationResult | None
    valid_until: date | None
    created_at: datetime
    started_at: datetime | None
    decision_at: datetime | None
    archived: bool
