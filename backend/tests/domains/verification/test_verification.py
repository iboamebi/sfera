from datetime import date
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


def test_mark_suitable():
    verification = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.UNSUITABLE,
    )

    verification.mark_suitable(date(2030, 1, 1))

    assert verification.result == VerificationResult.SUITABLE
    assert verification.valid_until == date(2030, 1, 1)
    assert verification.unsuitable_reason is None


def test_mark_unsuitable():
    verification = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.SUITABLE,
    )

    verification.mark_unsuitable("Broken seal")

    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Broken seal"


def test_unsuitable_requires_reason():
    verification = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.SUITABLE,
    )

    with pytest.raises(InvalidUnsuitableReasonDomainError):
        verification.mark_unsuitable("")


def test_create_suitable_verification_requires_valid_until():
    with pytest.raises(InvalidSuitableValidUntilDomainError):
        Verification.create(
            id=uuid4(),
            order_item_id=uuid4(),
            instrument_id=uuid4(),
            verification_date=date.today(),
            result=VerificationResult.SUITABLE,
        )


def test_create_unsuitable_verification_requires_reason():
    with pytest.raises(InvalidUnsuitableReasonDomainError):
        Verification.create(
            id=uuid4(),
            order_item_id=uuid4(),
            instrument_id=uuid4(),
            verification_date=date.today(),
            result=VerificationResult.UNSUITABLE,
        )


def test_create_suitable_verification_rejects_unsuitable_reason():
    with pytest.raises(InvalidVerificationResultStateDomainError):
        Verification.create(
            id=uuid4(),
            order_item_id=uuid4(),
            instrument_id=uuid4(),
            verification_date=date.today(),
            result=VerificationResult.SUITABLE,
            valid_until=date(2030, 1, 1),
            unsuitable_reason="Broken seal",
        )


def test_create_unsuitable_verification_rejects_valid_until():
    with pytest.raises(InvalidVerificationResultStateDomainError):
        Verification.create(
            id=uuid4(),
            order_item_id=uuid4(),
            instrument_id=uuid4(),
            verification_date=date.today(),
            result=VerificationResult.UNSUITABLE,
            valid_until=date(2030, 1, 1),
            unsuitable_reason="Broken seal",
        )


def test_create_verification_returns_result_consistent_state():
    verification = Verification.create(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.SUITABLE,
        valid_until=date(2030, 1, 1),
    )

    assert verification.result == VerificationResult.SUITABLE
    assert verification.valid_until == date(2030, 1, 1)
    assert verification.unsuitable_reason is None
