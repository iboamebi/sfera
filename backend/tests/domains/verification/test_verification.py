from datetime import date, datetime, timezone
from uuid import uuid4

import pytest

from app.domains.verification.entities.verification import Verification
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
from app.domains.verification.value_objects.verification_type import (
    VerificationType,
)


DECISION_AT = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)


def create_verification() -> Verification:
    """Create a verification in its initial lifecycle state."""
    return Verification.create(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=uuid4(),
        verification_date=date.today(),
        created_at=datetime(2026, 9, 5, 10, 0, tzinfo=timezone.utc),
        verification_type=VerificationType.PERIODIC,
    )


def test_create_verification_starts_in_created_state():
    verification = create_verification()

    assert verification.status == VerificationStatus.CREATED
    assert verification.verification_type == VerificationType.PERIODIC
    assert verification.result is None
    assert verification.decision_at is None
    assert verification.valid_until is None
    assert verification.unsuitable_reason is None


def test_start_moves_verification_to_in_progress():
    verification = create_verification()

    verification.start()

    assert verification.status == VerificationStatus.IN_PROGRESS
    assert verification.result is None
    assert verification.decision_at is None


def test_mark_suitable_completes_verification():
    verification = create_verification()
    verification.start()

    verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)

    assert verification.status == VerificationStatus.DECIDED
    assert verification.result == VerificationResult.SUITABLE
    assert verification.valid_until == date(2030, 1, 1)
    assert verification.unsuitable_reason is None
    assert verification.decision_at == DECISION_AT


def test_mark_unsuitable_completes_verification():
    verification = create_verification()
    verification.start()

    verification.mark_unsuitable("Broken seal", decision_at=DECISION_AT)

    assert verification.status == VerificationStatus.DECIDED
    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Broken seal"
    assert verification.decision_at == DECISION_AT


def test_unsuitable_requires_reason():
    verification = create_verification()
    verification.start()

    with pytest.raises(InvalidUnsuitableReasonDomainError):
        verification.mark_unsuitable("", decision_at=DECISION_AT)


def test_suitable_requires_valid_until():
    verification = create_verification()
    verification.start()

    with pytest.raises(InvalidSuitableValidUntilDomainError):
        verification.mark_suitable(None, decision_at=DECISION_AT)


def test_decision_requires_in_progress_state():
    verification = create_verification()

    with pytest.raises(InvalidVerificationResultStateDomainError):
        verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)


def test_decided_verification_cannot_be_decided_again():
    verification = create_verification()
    verification.start()
    verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)

    with pytest.raises(InvalidVerificationResultStateDomainError):
        verification.mark_unsuitable("Broken seal", decision_at=DECISION_AT)


def test_start_requires_created_state():
    verification = create_verification()
    verification.start()

    with pytest.raises(InvalidVerificationResultStateDomainError):
        verification.start()
