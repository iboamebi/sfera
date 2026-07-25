from datetime import date
from uuid import UUID, uuid4

from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
    ApproveVerificationHandler,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
    RejectVerificationHandler,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.domains.verification.entities.verification import Verification
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)


class FakeVerificationRepository(VerificationRepository):
    def __init__(self) -> None:
        self._items: dict[UUID, Verification] = {}

    def get(
        self,
        verification_id: UUID,
    ) -> Verification | None:
        return self._items.get(verification_id)

    def save(
        self,
        verification: Verification,
    ) -> None:
        self._items[verification.id] = verification


def test_approve_verification():
    repository = FakeVerificationRepository()

    verification = Verification(
        id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.UNSUITABLE,
    )

    repository.save(verification)

    service = VerificationApplicationService(repository)

    ApproveVerificationHandler(service).handle(
        ApproveVerificationCommand(
            verification_id=verification.id,
            valid_until=date(2030, 1, 1),
        )
    )

    assert verification.result == VerificationResult.SUITABLE
    assert verification.valid_until == date(2030, 1, 1)


def test_reject_verification():
    repository = FakeVerificationRepository()

    verification = Verification(
        id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.SUITABLE,
    )

    repository.save(verification)

    service = VerificationApplicationService(repository)

    RejectVerificationHandler(service).handle(
        RejectVerificationCommand(
            verification_id=verification.id,
            reason="Broken seal",
        )
    )

    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Broken seal"
