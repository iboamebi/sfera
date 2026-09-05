from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.domains.verification.exceptions import (
    InvalidSuitableValidUntilDomainError,
    InvalidUnsuitableReasonDomainError,
    InvalidVerificationResultStateDomainError,
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
    archived: bool = False

    @classmethod
    def create(
        cls,
        *,
        id: UUID,
        order_item_id: UUID,
        instrument_id: UUID,
        verification_date: date,
        result: VerificationResult,
        valid_until: date | None = None,
        unsuitable_reason: str | None = None,
        methodology: str | None = None,
    ) -> "Verification":
        """Create a verification with a result-consistent initial state."""
        if result == VerificationResult.SUITABLE:
            if valid_until is None:
                raise InvalidSuitableValidUntilDomainError
            if unsuitable_reason is not None:
                raise InvalidVerificationResultStateDomainError

        if result == VerificationResult.UNSUITABLE:
            if not unsuitable_reason:
                raise InvalidUnsuitableReasonDomainError
            if valid_until is not None:
                raise InvalidVerificationResultStateDomainError

        return cls(
            id=id,
            order_item_id=order_item_id,
            instrument_id=instrument_id,
            verification_date=verification_date,
            result=result,
            valid_until=valid_until,
            unsuitable_reason=unsuitable_reason,
            methodology=methodology,
        )

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
