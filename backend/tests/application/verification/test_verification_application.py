from datetime import date
from uuid import uuid4

from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
    ApproveVerificationHandler,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
    RejectVerificationHandler,
)
from app.domains.verification.entities.verification import Verification
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)


def test_approve_verification():
    verification = Verification(
        id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.UNSUITABLE,
    )

    ApproveVerificationHandler().handle(
        ApproveVerificationCommand(
            verification=verification,
            valid_until=date(2030, 1, 1),
        )
    )

    assert verification.result == VerificationResult.SUITABLE
    assert verification.valid_until == date(2030, 1, 1)


def test_reject_verification():
    verification = Verification(
        id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.SUITABLE,
    )

    RejectVerificationHandler().handle(
        RejectVerificationCommand(
            verification=verification,
            reason="Broken seal",
        )
    )

    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Broken seal"
