from datetime import date
from uuid import UUID, uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.verification.entities.verification import Verification
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


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


def make_user(role: UserRole) -> User:
    return User(
        id=uuid4(),
        username="test-user",
        password_hash="test-hash",
        role=role,
    )


def test_approve_verification():
    repository = FakeVerificationRepository()

    verification = Verification(
        id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.UNSUITABLE,
    )

    repository.save(verification)

    service = VerificationApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    service.approve(
        ApproveVerificationCommand(
            verification_id=verification.id,
            valid_until=date(2030, 1, 1),
        ),
        make_user(UserRole.METROLOGIST),
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

    service = VerificationApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    service.reject(
        RejectVerificationCommand(
            verification_id=verification.id,
            reason="Broken seal",
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Broken seal"


def test_verification_approval_requires_metrologist_or_admin():
    repository = FakeVerificationRepository()

    verification = Verification(
        id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.UNSUITABLE,
    )

    repository.save(verification)

    service = VerificationApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    with pytest.raises(AuthorizationError):
        service.approve(
            ApproveVerificationCommand(
                verification_id=verification.id,
                valid_until=date(2030, 1, 1),
            ),
            make_user(UserRole.OPERATOR),
        )


def test_verification_rejection_requires_metrologist_or_admin():
    repository = FakeVerificationRepository()

    verification = Verification(
        id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.SUITABLE,
    )

    repository.save(verification)

    service = VerificationApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    with pytest.raises(AuthorizationError):
        service.reject(
            RejectVerificationCommand(
                verification_id=verification.id,
                reason="Broken seal",
            ),
            make_user(UserRole.TECHNICIAN),
        )
