from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.domains.verification.exceptions import (
    InvalidUnsuitableReasonDomainError,
)
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False, kw_only=True)
class Verification(AggregateRoot):
    order_item_id: UUID
    verification_date: date
    result: VerificationResult

    instrument_id: UUID | None = None
    valid_until: date | None = None
    unsuitable_reason: str | None = None
    methodology: str | None = None

    def mark_suitable(
        self,
        valid_until: date,
    ) -> None:
        self.result = VerificationResult.SUITABLE
        self.valid_until = valid_until
        self.unsuitable_reason = None

    def mark_unsuitable(
        self,
        reason: str,
    ) -> None:
        if not reason:
            raise InvalidUnsuitableReasonDomainError

        self.result = VerificationResult.UNSUITABLE
        self.valid_until = None
        self.unsuitable_reason = reason
