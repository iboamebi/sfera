from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from app.domains.verification.exceptions import (
    InvalidSuitableValidUntilDomainError,
    InvalidUnsuitableReasonDomainError,
    InvalidVerificationResultStateDomainError,
)
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False, kw_only=True)
class Verification(AggregateRoot):
    """Aggregate representing one concrete instrument verification."""

    order_item_id: UUID
    verification_date: date
    status: VerificationStatus = VerificationStatus.CREATED
    result: VerificationResult | None = None

    instrument_id: UUID | None = None
    valid_until: date | None = None
    unsuitable_reason: str | None = None
    methodology: str | None = None
    decision_at: datetime | None = None
    archived: bool = False

    @classmethod
    def create(
        cls,
        *,
        id: UUID,
        order_item_id: UUID,
        instrument_id: UUID,
        verification_date: date,
        methodology: str | None = None,
    ) -> "Verification":
        """Create a verification before the final suitability decision."""
        return cls(
            id=id,
            order_item_id=order_item_id,
            instrument_id=instrument_id,
            verification_date=verification_date,
            status=VerificationStatus.CREATED,
            result=None,
            methodology=methodology,
        )

    def start(self) -> None:
        """Move the verification into active execution."""
        if self.status != VerificationStatus.CREATED:
            raise InvalidVerificationResultStateDomainError

        self.status = VerificationStatus.IN_PROGRESS

    def mark_suitable(
        self,
        valid_until: date,
        *,
        decision_at: datetime,
    ) -> None:
        """Record the final suitable decision."""
        if self.status != VerificationStatus.IN_PROGRESS:
            raise InvalidVerificationResultStateDomainError
        if valid_until is None:
            raise InvalidSuitableValidUntilDomainError
        if self.unsuitable_reason is not None:
            raise InvalidVerificationResultStateDomainError

        self.status = VerificationStatus.DECIDED
        self.result = VerificationResult.SUITABLE
        self.valid_until = valid_until
        self.unsuitable_reason = None
        self.decision_at = decision_at

    def mark_unsuitable(
        self,
        reason: str,
        *,
        decision_at: datetime,
    ) -> None:
        """Record the final unsuitable decision."""
        if self.status != VerificationStatus.IN_PROGRESS:
            raise InvalidVerificationResultStateDomainError
        if not reason:
            raise InvalidUnsuitableReasonDomainError
        if self.valid_until is not None:
            raise InvalidVerificationResultStateDomainError

        self.status = VerificationStatus.DECIDED
        self.result = VerificationResult.UNSUITABLE
        self.valid_until = None
        self.unsuitable_reason = reason
        self.decision_at = decision_at
