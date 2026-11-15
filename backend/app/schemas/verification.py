from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.domains.verification.value_objects.verification_type import (
    VerificationType,
)


class VerificationBase(BaseModel):
    order_item_id: UUID
    verification_date: date
    valid_until: date | None = None
    result: VerificationResult | None = None
    unsuitable_reason: str | None = None
    cancellation_reason: str | None = None
    methodology: str | None = None


class VerificationCreate(BaseModel):
    order_item_id: UUID
    verification_date: date
    verification_type: VerificationType
    methodology: str | None = None


class VerificationUpdate(BaseModel):
    verification_date: date | None = None
    valid_until: date | None = None
    result: VerificationResult | None = None
    unsuitable_reason: str | None = None
    methodology: str | None = None


class VerificationRead(VerificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    instrument_id: UUID | None = None
    created_at: datetime
    started_at: datetime | None = None
    decision_at: datetime | None = None
    status: VerificationStatus
    verification_type: VerificationType
    archived: bool


class VerificationListRead(BaseModel):
    """Verification row for the general read-only list."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_item_id: UUID
    order_id: UUID
    order_number: str
    customer_id: UUID
    customer_name: str
    instrument_id: UUID | None = None
    instrument_name: str | None = None
    instrument_type_id: UUID | None = None
    instrument_type_name: str | None = None
    serial_number: str | None = None
    verification_date: date
    verification_type: VerificationType
    status: VerificationStatus
    result: VerificationResult | None = None
    valid_until: date | None = None
    created_at: datetime
    started_at: datetime | None = None
    decision_at: datetime | None = None
    archived: bool


class VerificationCancellation(BaseModel):
    reason: str | None = None


class VerificationDecisionCorrection(BaseModel):
    """Payload for correcting a previously decided verification result."""

    result: VerificationResult
    valid_until: date | None = None
    unsuitable_reason: str | None = None
    reason: str
