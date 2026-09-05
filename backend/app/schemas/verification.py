from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)


class VerificationBase(BaseModel):
    order_item_id: UUID
    verification_date: date
    valid_until: date | None = None
    result: VerificationResult
    unsuitable_reason: str | None = None
    methodology: str | None = None


class VerificationCreate(VerificationBase):
    pass


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
    archived: bool
