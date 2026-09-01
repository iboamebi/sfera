"""
Application service for verification use cases.
"""

from uuid import UUID

from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.shared.audit.repositories.audit_repository import AuditRepository
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
from app.shared.audit.models import AuditOperation, AuditRecord
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class VerificationApplicationService:
    """Coordinates verification use cases."""

    def __init__(
        self,
        repository: VerificationRepository,
        unit_of_work: UnitOfWork,
        audit_operation_repository: AuditOperationRepository,
        audit_repository: AuditRepository,
    ) -> None:
        self._repository = repository
        self._uow = unit_of_work
        self._audit_operation_repository = audit_operation_repository
        self._audit_repository = audit_repository

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
            operation = AuditOperation(initiated_by=user.id)
            old_result = verification.result
            old_valid_until = verification.valid_until
            old_unsuitable_reason = verification.unsuitable_reason

            verification.mark_suitable(command.valid_until)

            self._repository.save(verification)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(
                AuditRecord(
                    operation_id=operation.operation_id,
                    actor_id=user.id,
                    action="verification.approved",
                    entity_type="Verification",
                    entity_id=verification.id,
                    changes={
                        "result": {
                            "old": old_result.value,
                            "new": verification.result.value,
                        },
                        "valid_until": {
                            "old": old_valid_until.isoformat()
                            if old_valid_until is not None
                            else None,
                            "new": verification.valid_until.isoformat()
                            if verification.valid_until is not None
                            else None,
                        },
                        "unsuitable_reason": {
                            "old": old_unsuitable_reason,
                            "new": verification.unsuitable_reason,
                        },
                    },
                )
            )

        return verification

    def reject(
        self,
        command: RejectVerificationCommand,
        user: User,
    ) -> Verification:
        require_role(user, UserRole.METROLOGIST, UserRole.ADMIN)

        with self._uow:
            verification = self.get(command.verification_id)
            operation = AuditOperation(initiated_by=user.id)
            old_result = verification.result
            old_valid_until = verification.valid_until
            old_unsuitable_reason = verification.unsuitable_reason

            verification.mark_unsuitable(command.reason)

            self._repository.save(verification)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(
                AuditRecord(
                    operation_id=operation.operation_id,
                    actor_id=user.id,
                    action="verification.rejected",
                    entity_type="Verification",
                    entity_id=verification.id,
                    changes={
                        "result": {
                            "old": old_result.value,
                            "new": verification.result.value,
                        },
                        "valid_until": {
                            "old": old_valid_until.isoformat()
                            if old_valid_until is not None
                            else None,
                            "new": None,
                        },
                        "unsuitable_reason": {
                            "old": old_unsuitable_reason,
                            "new": verification.unsuitable_reason,
                        },
                    },
                    reason=command.reason,
                )
            )

        return verification
