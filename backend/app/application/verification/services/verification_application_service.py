"""
Application service for verification use cases.
"""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.application.authorization.authorization import require_role
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.create_verification import (
    CreateVerificationCommand,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
)
from app.application.verification.commands.start_verification import (
    StartVerificationCommand,
)
from app.application.verification.exceptions import (
    VerificationCannotBeStartedApplicationError,
    VerificationInstrumentRequiredApplicationError,
    VerificationNotFoundApplicationError,
    VerificationOrderItemNotFoundApplicationError,
)
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.verification.entities.verification import Verification
from app.domains.verification.exceptions import (
    InvalidVerificationResultStateDomainError,
)
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.shared.audit.models import AuditOperation, AuditRecord
from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.shared.audit.repositories.audit_repository import AuditRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class VerificationApplicationService:
    """Coordinates verification use cases."""

    def __init__(
        self,
        repository: VerificationRepository,
        order_repository: OrderRepository,
        unit_of_work: UnitOfWork,
        audit_operation_repository: AuditOperationRepository,
        audit_repository: AuditRepository,
    ) -> None:
        self._repository = repository
        self._order_repository = order_repository
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

    def create(
        self,
        command: CreateVerificationCommand,
        user: User,
    ) -> Verification:
        """Register a verification for a concrete instrument."""
        require_role(user, UserRole.METROLOGIST, UserRole.ADMIN)

        with self._uow:
            order = self._order_repository.get_by_order_item_id(
                command.order_item_id,
            )
            if order is None:
                raise VerificationOrderItemNotFoundApplicationError

            item = next(
                (item for item in order.items if item.id == command.order_item_id),
                None,
            )
            if item is None:
                raise VerificationOrderItemNotFoundApplicationError

            if item.instrument_id is None:
                raise VerificationInstrumentRequiredApplicationError

            verification = Verification.create(
                id=uuid4(),
                order_item_id=command.order_item_id,
                instrument_id=item.instrument_id,
                verification_date=command.verification_date,
                created_at=datetime.now(UTC),
                verification_type=command.verification_type,
                methodology=command.methodology,
            )
            self._repository.save(verification)

            operation = AuditOperation(initiated_by=user.id)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(
                AuditRecord(
                    operation_id=operation.operation_id,
                    actor_id=user.id,
                    action="verification.created",
                    entity_type="Verification",
                    entity_id=verification.id,
                    changes={
                        "order_item_id": {
                            "old": None,
                            "new": str(verification.order_item_id),
                        },
                        "instrument_id": {
                            "old": None,
                            "new": str(verification.instrument_id),
                        },
                        "verification_date": {
                            "old": None,
                            "new": verification.verification_date.isoformat(),
                        },
                        "created_at": {
                            "old": None,
                            "new": verification.created_at.isoformat(),
                        },
                        "verification_type": {
                            "old": None,
                            "new": verification.verification_type.value,
                        },
                        "status": {
                            "old": None,
                            "new": verification.status.value,
                        },
                        "methodology": {
                            "old": None,
                            "new": verification.methodology,
                        },
                    },
                )
            )

        return verification

    def start(self, command: StartVerificationCommand, user: User) -> Verification:
        """Start execution of a previously registered verification."""
        require_role(user, UserRole.METROLOGIST, UserRole.ADMIN)
        with self._uow:
            verification = self.get(command.verification_id)
            old_status = verification.status.value
            started_at = datetime.now(UTC)
            try:
                verification.start(started_at=started_at)
            except InvalidVerificationResultStateDomainError:
                raise VerificationCannotBeStartedApplicationError from None
            self._repository.save(verification)
            operation = AuditOperation(initiated_by=user.id)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(
                AuditRecord(
                    operation_id=operation.operation_id,
                    actor_id=user.id,
                    action="verification.started",
                    entity_type="Verification",
                    entity_id=verification.id,
                    changes={
                        "status": {"old": old_status, "new": verification.status.value},
                        "started_at": {"old": None, "new": verification.started_at.isoformat()},
                    },
                )
            )
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

            verification.mark_suitable(
                command.valid_until,
                decision_at=datetime.now(UTC),
            )

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
                            "old": old_result.value if old_result is not None else None,
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

            verification.mark_unsuitable(
                command.reason,
                decision_at=datetime.now(UTC),
            )

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
                            "old": old_result.value if old_result is not None else None,
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
