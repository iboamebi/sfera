from datetime import UTC, date, datetime
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

DECISION_AT = datetime(2030, 1, 1, 12, 0, tzinfo=UTC)


def create_verification() -> Verification:
    """Create a verification in its initial lifecycle state."""
    return Verification.create(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=uuid4(),
        verification_date=date.today(),
        created_at=datetime(2026, 9, 5, 10, 0, tzinfo=UTC),
        verification_type=VerificationType.PERIODIC,
    )


def test_create_verification_starts_in_created_state():
    verification = create_verification()

    assert verification.status == VerificationStatus.CREATED
    assert verification.verification_type == VerificationType.PERIODIC
    assert verification.result is None
    assert verification.started_at is None
    assert verification.decision_at is None
    assert verification.valid_until is None
    assert verification.unsuitable_reason is None


def test_start_moves_verification_to_in_progress():
    verification = create_verification()

    verification.start(started_at=DECISION_AT)

    assert verification.status == VerificationStatus.IN_PROGRESS
    assert verification.started_at == DECISION_AT
    assert verification.result is None
    assert verification.decision_at is None


def test_mark_suitable_completes_verification():
    verification = create_verification()
    verification.start(started_at=DECISION_AT)

    verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)

    assert verification.status == VerificationStatus.DECIDED
    assert verification.result == VerificationResult.SUITABLE
    assert verification.valid_until == date(2030, 1, 1)
    assert verification.unsuitable_reason is None
    assert verification.decision_at == DECISION_AT


def test_mark_unsuitable_completes_verification():
    verification = create_verification()
    verification.start(started_at=DECISION_AT)

    verification.mark_unsuitable("Broken seal", decision_at=DECISION_AT)

    assert verification.status == VerificationStatus.DECIDED
    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Broken seal"
    assert verification.decision_at == DECISION_AT


@pytest.mark.parametrize("reason", ["", " ", "   ", "\t\n"])
def test_unsuitable_requires_non_blank_reason(reason: str):
    verification = create_verification()
    verification.start(started_at=DECISION_AT)

    with pytest.raises(InvalidUnsuitableReasonDomainError):
        verification.mark_unsuitable(reason, decision_at=DECISION_AT)


def test_suitable_requires_valid_until():
    verification = create_verification()
    verification.start(started_at=DECISION_AT)

    with pytest.raises(InvalidSuitableValidUntilDomainError):
        verification.mark_suitable(None, decision_at=DECISION_AT)


def test_decision_requires_in_progress_state():
    verification = create_verification()

    with pytest.raises(InvalidVerificationResultStateDomainError):
        verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)


def test_decided_verification_cannot_be_decided_again():
    verification = create_verification()
    verification.start(started_at=DECISION_AT)
    verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)

    with pytest.raises(InvalidVerificationResultStateDomainError):
        verification.mark_unsuitable("Broken seal", decision_at=DECISION_AT)


def test_start_requires_created_state():
    verification = create_verification()
    verification.start(started_at=DECISION_AT)

    with pytest.raises(InvalidVerificationResultStateDomainError):
        verification.start(started_at=DECISION_AT)


def test_correct_valid_until_updates_only_suitable_decision():
    verification = create_verification()
    verification.start(started_at=DECISION_AT)
    verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)

    verification.correct_valid_until(
        date(2029, 12, 31),
        reason="Исправлена ошибка ввода",
    )

    assert verification.valid_until == date(2029, 12, 31)
    assert verification.decision_at == DECISION_AT


@pytest.mark.parametrize("reason", ["", " ", "  \t"])
def test_correct_valid_until_requires_non_blank_reason(reason: str):
    from app.domains.verification.exceptions import (
        InvalidValidityCorrectionReasonDomainError,
    )

    verification = create_verification()
    verification.start(started_at=DECISION_AT)
    verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)

    with pytest.raises(InvalidValidityCorrectionReasonDomainError):
        verification.correct_valid_until(date(2029, 12, 31), reason=reason)


def test_correct_valid_until_rejects_non_suitable_or_undecided_verification():
    verification = create_verification()

    with pytest.raises(InvalidVerificationResultStateDomainError):
        verification.correct_valid_until(
            date(2029, 12, 31),
            reason="Исправление",
        )


def test_correct_decision_changes_suitable_to_unsuitable():
    verification = create_verification()
    verification.start(started_at=DECISION_AT)
    verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)

    corrected_at = datetime(2030, 1, 2, 12, 0, tzinfo=UTC)
    verification.correct_decision(
        result=VerificationResult.UNSUITABLE,
        valid_until=None,
        unsuitable_reason="Повреждена пломба",
        reason="Обнаружена ошибка при оформлении решения",
        decision_at=corrected_at,
    )

    assert verification.status == VerificationStatus.DECIDED
    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Повреждена пломба"
    assert verification.decision_at == corrected_at


def test_correct_decision_rejects_unsuitable_to_suitable():
    from app.domains.verification.exceptions import (
        InvalidDecisionCorrectionDomainError,
    )

    verification = create_verification()
    verification.start(started_at=DECISION_AT)
    verification.mark_unsuitable("Ошибка осмотра", decision_at=DECISION_AT)

    with pytest.raises(InvalidDecisionCorrectionDomainError):
        verification.correct_decision(
            result=VerificationResult.SUITABLE,
            valid_until=date(2032, 1, 1),
            unsuitable_reason=None,
            reason="Повторная проверка подтвердила пригодность",
            decision_at=datetime(2030, 1, 2, 12, 0, tzinfo=UTC),
        )


@pytest.mark.parametrize("reason", ["", " ", "\t"])
def test_correct_decision_requires_reason(reason: str):
    verification = create_verification()
    verification.start(started_at=DECISION_AT)
    verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)

    from app.domains.verification.exceptions import (
        InvalidDecisionCorrectionReasonDomainError,
    )

    with pytest.raises(InvalidDecisionCorrectionReasonDomainError):
        verification.correct_decision(
            result=VerificationResult.UNSUITABLE,
            valid_until=None,
            unsuitable_reason="Повреждена пломба",
            reason=reason,
            decision_at=DECISION_AT,
        )


def test_correct_decision_requires_valid_until_for_suitable():
    verification = create_verification()
    verification.start(started_at=DECISION_AT)
    verification.mark_unsuitable("Ошибка", decision_at=DECISION_AT)

    from app.domains.verification.exceptions import (
        InvalidDecisionCorrectionDomainError,
    )

    with pytest.raises(InvalidDecisionCorrectionDomainError):
        verification.correct_decision(
            result=VerificationResult.SUITABLE,
            valid_until=None,
            unsuitable_reason=None,
            reason="Исправление",
            decision_at=DECISION_AT,
        )


def test_correct_decision_requires_unsuitable_reason_for_unsuitable():
    verification = create_verification()
    verification.start(started_at=DECISION_AT)
    verification.mark_suitable(date(2030, 1, 1), decision_at=DECISION_AT)

    with pytest.raises(InvalidUnsuitableReasonDomainError):
        verification.correct_decision(
            result=VerificationResult.UNSUITABLE,
            valid_until=None,
            unsuitable_reason=" ",
            reason="Исправление",
            decision_at=DECISION_AT,
        )


def test_correct_decision_rejects_undecided_verification():
    verification = create_verification()

    with pytest.raises(InvalidVerificationResultStateDomainError):
        verification.correct_decision(
            result=VerificationResult.SUITABLE,
            valid_until=date(2030, 1, 1),
            unsuitable_reason=None,
            reason="Исправление",
            decision_at=DECISION_AT,
        )
