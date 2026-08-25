"""
Application service for verification use cases.
"""

from uuid import UUID

from app.application.authorization.authorization import require_role
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
)
from app.application.verification.exceptions import (
    VerificationNotFoundApplicationError,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.verification.entities.verification import Verification
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class VerificationApplicationService:
    """Coordinates verification use cases."""

    def __init__(
        self,
        repository: VerificationRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = unit_of_work

    def get(
        self,
        verification_id: UUID,
    ) -> Verification:
        verification = self._repository.get(verification_id)

        if verification is None:
            raise VerificationNotFoundApplicationError

        return verification

    def approve(
        self,
        command: ApproveVerificationCommand,
        user: User,
    ) -> Verification:
        require_role(user, UserRole.METROLOGIST, UserRole.ADMIN)

        with self._uow:
            verification = self.get(command.verification_id)

            verification.mark_suitable(command.valid_until)

            self._repository.save(verification)

        return verification

    def reject(
        self,
        command: RejectVerificationCommand,
        user: User,
    ) -> Verification:
        require_role(user, UserRole.METROLOGIST, UserRole.ADMIN)

        with self._uow:
            verification = self.get(command.verification_id)

            verification.mark_unsuitable(command.reason)

            self._repository.save(verification)

        return verification
