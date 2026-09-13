"""Tests for Verification mapper."""

from datetime import UTC, date, datetime
from uuid import uuid4

from app.domains.verification.entities.verification import Verification
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.infrastructure.mappers.verification_mapper import VerificationMapper
from app.models.verification import Verification as VerificationModel


def test_verification_mapper_to_domain_preserves_instrument_id() -> None:
    """Map ORM verification to domain with instrument association."""
    instrument_id = uuid4()
    decision_at = datetime(2026, 9, 5, 12, 0, tzinfo=UTC)

    model = VerificationModel(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=instrument_id,
        verification_date=date(2026, 9, 5),
        status=VerificationStatus.DECIDED,
        decision_at=decision_at,
        result=VerificationResult.SUITABLE,
        valid_until=date(2027, 9, 5),
    )

    entity = VerificationMapper().to_domain(model)

    assert entity.instrument_id == instrument_id
    assert entity.status == VerificationStatus.DECIDED
    assert entity.result == VerificationResult.SUITABLE
    assert entity.valid_until == date(2027, 9, 5)
    assert entity.decision_at == decision_at


def test_verification_mapper_to_model_preserves_instrument_id() -> None:
    """Map domain verification to ORM with instrument association."""
    instrument_id = uuid4()
    decision_at = datetime(2026, 9, 5, 12, 0, tzinfo=UTC)

    entity = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=instrument_id,
        verification_date=date(2026, 9, 5),
        status=VerificationStatus.DECIDED,
        result=VerificationResult.SUITABLE,
        valid_until=date(2027, 9, 5),
        decision_at=decision_at,
    )
    model = VerificationModel(
        id=entity.id,
        order_item_id=entity.order_item_id,
        verification_date=entity.verification_date,
        status=VerificationStatus.DECIDED,
        result=entity.result,
        valid_until=entity.valid_until,
    )

    VerificationMapper().to_model(entity, model)

    assert model.instrument_id == instrument_id
    assert model.status == VerificationStatus.DECIDED
    assert model.result == VerificationResult.SUITABLE
    assert model.valid_until == date(2027, 9, 5)
    assert model.decision_at == decision_at


def test_verification_mapper_preserves_null_instrument_id() -> None:
    """Map historical verification without an instrument association."""
    model = VerificationModel(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=None,
        verification_date=date(2026, 9, 5),
        status=VerificationStatus.DECIDED,
        decision_at=datetime(2026, 9, 5, tzinfo=UTC),
        result=VerificationResult.SUITABLE,
        valid_until=date(2027, 9, 5),
    )

    entity = VerificationMapper().to_domain(model)

    assert entity.instrument_id is None


def test_verification_mapper_preserves_in_progress_state() -> None:
    """Map an active verification without a final decision."""
    model = VerificationModel(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=uuid4(),
        verification_date=date(2026, 9, 5),
        status=VerificationStatus.IN_PROGRESS,
        result=None,
        decision_at=None,
        valid_until=None,
        unsuitable_reason=None,
    )

    entity = VerificationMapper().to_domain(model)

    assert entity.status == VerificationStatus.IN_PROGRESS
    assert entity.result is None
    assert entity.decision_at is None
    assert entity.valid_until is None
