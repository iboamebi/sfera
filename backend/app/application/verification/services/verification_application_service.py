"""
Application service for verification use cases.
"""

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.application.authorization.authorization import require_role
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.correct_verification_decision import (
    CorrectVerificationDecisionCommand,
)
from app.application.verification.commands.correct_verification_valid_until import (
    CorrectVerificationValidUntilCommand,
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
    VerificationAlreadyActiveApplicationError,
    VerificationCannotBeStartedApplicationError,
    VerificationCannotBeCancelledApplicationError,
    VerificationCancellationReasonRequiredApplicationError,
    VerificationInstrumentRequiredApplicationError,
    VerificationNotFoundApplicationError,
    VerificationOrderItemNotFoundApplicationError,
)
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.verification.entities.verification import Verification
from app.domains.verification.exceptions import (
    ActiveVerificationAlreadyExistsDomainError,
    InvalidVerificationResultStateDomainError,
    InvalidVerificationCancellationDomainError,
    InvalidVerificationCancellationReasonDomainError,
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

            if self._repository.has_active_for_order_item(command.order_item_id):
                raise VerificationAlreadyActiveApplicationError

            verification = Verification.create(
                id=uuid4(),
                order_item_id=command.order_item_id,
                instrument_id=item.instrument_id,
                verification_date=command.verification_date,
                created_at=datetime.now(UTC),
                verification_type=command.verification_type,
                methodology=command.methodology,
            )
            try:
                self._repository.save(verification)
            except ActiveVerificationAlreadyExistsDomainError:
                raise VerificationAlreadyActiveApplicationError from None

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
            order = self._order_repository.get_by_order_item_id(
                verification.order_item_id,
            )
            old_status = verification.status.value
            old_order_status = order.status.value if order is not None else None
            started_at = datetime.now(UTC)
            try:
                verification.start(started_at=started_at)
            except InvalidVerificationResultStateDomainError:
                raise VerificationCannotBeStartedApplicationError from None
            if order is not None:
                order.start_work()
                self._order_repository.save(order)

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
                        "status": {
                            "old": old_status,
                            "new": verification.status.value,
                        },
                        "started_at": {
                            "old": None,
                            "new": verification.started_at.isoformat(),
                        },
                    },
                )
            )
            if order is not None and old_order_status != order.status.value:
                self._audit_repository.save(
                    AuditRecord(
                        operation_id=operation.operation_id,
                        actor_id=user.id,
                        action="order.started_work",
                        entity_type="order",
                        entity_id=order.id,
                        changes={
                            "status": {
                                "old": old_order_status,
                                "new": order.status.value,
                            },
                        },
                    )
                )
        return verification

    def cancel(self, command, user: User) -> Verification:
        require_role(user, UserRole.METROLOGIST, UserRole.ADMIN)
        with self._uow:
            verification = self.get(command.verification_id)
            old_status = verification.status.value
            try:
                verification.cancel(reason=command.reason)
            except InvalidVerificationCancellationDomainError:
                raise VerificationCannotBeCancelledApplicationError from None
            except InvalidVerificationCancellationReasonDomainError:
                raise VerificationCancellationReasonRequiredApplicationError from None
            self._repository.save(verification)
            operation = AuditOperation(initiated_by=user.id)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(AuditRecord(
                operation_id=operation.operation_id, actor_id=user.id,
                action="verification.cancelled", entity_type="Verification",
                entity_id=verification.id,
                changes={"status": {"old": old_status, "new": verification.status.value},
                         "cancellation_reason": {"old": None, "new": verification.cancellation_reason}},
                reason=verification.cancellation_reason,
            ))
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
            decision_at = datetime.now(UTC)
            valid_until = command.valid_until
            if valid_until is None:
                if command.duration_years is None or command.time_zone is None:
                    raise ValueError(
                        "Provide valid_until or duration_years and time_zone"
                    )
                if command.duration_years < 1 or command.duration_years > 100:
                    raise ValueError("duration_years must be between 1 and 100")
                try:
                    local_decision_date = decision_at.astimezone(
                        ZoneInfo(command.time_zone),
                    ).date()
                except (ZoneInfoNotFoundError, ValueError):
                    raise ValueError("Invalid IANA time zone") from None
                try:
                    anniversary = local_decision_date.replace(
                        year=local_decision_date.year + command.duration_years,
                    )
                except ValueError:
                    anniversary = local_decision_date.replace(
                        year=local_decision_date.year + command.duration_years,
                        day=28,
                    )
                valid_until = anniversary - timedelta(days=1)

            assert valid_until is not None
            verification.mark_suitable(
                valid_until,
                decision_at=decision_at,
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

    def correct_valid_until(
        self,
        command: CorrectVerificationValidUntilCommand,
        user: User,
    ) -> Verification:
        """Correct the validity date of an already suitable decision."""
        require_role(user, UserRole.METROLOGIST, UserRole.ADMIN)
        with self._uow:
            verification = self.get(command.verification_id)
            old_valid_until = verification.valid_until
            verification.correct_valid_until(
                command.valid_until,
                reason=command.reason,
            )
            self._repository.save(verification)
            operation = AuditOperation(initiated_by=user.id)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(
                AuditRecord(
                    operation_id=operation.operation_id,
                    actor_id=user.id,
                    action="verification.valid_until_corrected",
                    entity_type="Verification",
                    entity_id=verification.id,
                    changes={
                        "valid_until": {
                            "old": old_valid_until.isoformat()
                            if old_valid_until is not None
                            else None,
                            "new": verification.valid_until.isoformat(),
                        },
                    },
                    reason=command.reason,
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

    def correct_decision(
        self,
        command: CorrectVerificationDecisionCommand,
        user: User,
    ) -> Verification:
        """Correct a final verification decision and append an audit record."""
        require_role(user, UserRole.METROLOGIST, UserRole.ADMIN)
        with self._uow:
            verification = self.get(command.verification_id)
            old_result = verification.result
            old_valid_until = verification.valid_until
            old_unsuitable_reason = verification.unsuitable_reason
            old_decision_at = verification.decision_at
            decision_at = datetime.now(UTC)

            verification.correct_decision(
                result=command.result,
                valid_until=command.valid_until,
                unsuitable_reason=command.unsuitable_reason,
                reason=command.reason,
                decision_at=decision_at,
            )
            self._repository.save(verification)
            operation = AuditOperation(initiated_by=user.id)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(
                AuditRecord(
                    operation_id=operation.operation_id,
                    actor_id=user.id,
                    action="verification.decision_corrected",
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
                        "decision_at": {
                            "old": old_decision_at.isoformat()
                            if old_decision_at is not None
                            else None,
                            "new": verification.decision_at.isoformat(),
                        },
                    },
                    reason=command.reason,
                )
            )
        return verification
