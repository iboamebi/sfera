"""
Application service for repair use cases.
"""

from uuid import UUID, uuid4

from app.application.authorization.authorization import require_role
from app.application.repair.commands.create_repair import (
    CreateRepairCommand,
)
from app.application.repair.exceptions import (
    RepairNotFoundApplicationError,
)
from app.domains.repair.entities.repair import Repair
from app.domains.repair.repositories.repair_repository import (
    RepairRepository,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.audit.models import AuditOperation, AuditRecord
from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.shared.audit.repositories.audit_repository import AuditRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class RepairApplicationService:
    """Coordinates repair use cases."""

    def __init__(
        self,
        repository: RepairRepository,
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
        repair_id: UUID,
    ) -> Repair:
        repair = self._repository.get(
            repair_id,
        )

        if repair is None:
            raise RepairNotFoundApplicationError

        return repair

    def create(
        self,
        command: CreateRepairCommand,
        user: User,
    ) -> Repair:
        require_role(
            user,
            UserRole.TECHNICIAN,
            UserRole.ADMIN,
        )

        repair = Repair.create(
            id=uuid4(),
            order_item_id=command.order_item_id,
            description=command.description,
        )

        with self._uow:
            self._repository.save(
                repair,
            )

        return repair

    def start(
        self,
        repair_id: UUID,
        user: User,
    ) -> Repair:
        require_role(
            user,
            UserRole.TECHNICIAN,
            UserRole.ADMIN,
        )

        with self._uow:
            repair = self.get(
                repair_id,
            )

            repair.start()

            self._repository.save(
                repair,
            )

        return repair

    def complete(
        self,
        repair_id: UUID,
        result: str,
        user: User,
    ) -> Repair:
        require_role(
            user,
            UserRole.TECHNICIAN,
            UserRole.ADMIN,
        )

        with self._uow:
            repair = self.get(
                repair_id,
            )

            old_status = repair.status.value
            old_result = repair.result
            repair.complete(
                result,
            )

            self._repository.save(
                repair,
            )
            operation = AuditOperation(initiated_by=user.id)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(
                AuditRecord(
                    operation_id=operation.operation_id,
                    actor_id=user.id,
                    action="repair.completed",
                    entity_type="repair",
                    entity_id=repair.id,
                    changes={
                        "status": {
                            "old": old_status,
                            "new": repair.status.value,
                        },
                        "result": {
                            "old": old_result,
                            "new": repair.result,
                        },
                    },
                )
            )

        return repair

    def cancel(
        self,
        repair_id: UUID,
        user: User,
    ) -> Repair:
        require_role(
            user,
            UserRole.TECHNICIAN,
            UserRole.ADMIN,
        )

        with self._uow:
            repair = self.get(
                repair_id,
            )

            repair.cancel()

            self._repository.save(
                repair,
            )

        return repair
