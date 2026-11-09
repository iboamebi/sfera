"""
Application service for diagnostic use cases.
"""

from uuid import UUID, uuid4

from app.application.authorization.authorization import require_role
from app.application.diagnostic.commands.complete_diagnostic import (
    CompleteDiagnosticCommand,
)
from app.application.diagnostic.commands.create_diagnostic import (
    CreateDiagnosticCommand,
)
from app.application.diagnostic.commands.set_recommendation import (
    SetRecommendationCommand,
)
from app.application.diagnostic.exceptions import (
    DiagnosticNotFoundApplicationError,
)
from app.domains.diagnostic.entities.diagnostic import Diagnostic
from app.domains.diagnostic.repositories.diagnostic_repository import (
    DiagnosticRepository,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.audit.models import AuditOperation, AuditRecord
from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.shared.audit.repositories.audit_repository import AuditRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class DiagnosticApplicationService:
    """Coordinates diagnostic use cases."""

    def __init__(
        self,
        repository: DiagnosticRepository,
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
        diagnostic_id: UUID,
    ) -> Diagnostic:
        """Get diagnostic."""

        diagnostic = self._repository.get(
            diagnostic_id,
        )

        if diagnostic is None:
            raise DiagnosticNotFoundApplicationError

        return diagnostic

    def create(
        self,
        command: CreateDiagnosticCommand,
        user: User,
    ) -> Diagnostic:
        """Create diagnostic."""

        require_role(
            user,
            UserRole.TECHNICIAN,
            UserRole.ADMIN,
        )

        diagnostic = Diagnostic(
            id=uuid4(),
            order_item_id=command.order_item_id,
        )

        with self._uow:
            self._repository.save(
                diagnostic,
            )

        return diagnostic

    def complete(
        self,
        command: CompleteDiagnosticCommand,
        user: User,
    ) -> Diagnostic:
        """Complete diagnostic."""

        require_role(
            user,
            UserRole.TECHNICIAN,
            UserRole.ADMIN,
        )

        with self._uow:
            diagnostic = self.get(
                command.diagnostic_id,
            )

            old_conclusion = diagnostic.conclusion
            diagnostic.complete(
                command.conclusion,
            )

            self._repository.save(
                diagnostic,
            )
            operation = AuditOperation(initiated_by=user.id)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(
                AuditRecord(
                    operation_id=operation.operation_id,
                    actor_id=user.id,
                    action="diagnostic.completed",
                    entity_type="diagnostic",
                    entity_id=diagnostic.id,
                    changes={
                        "conclusion": {
                            "old": old_conclusion,
                            "new": diagnostic.conclusion,
                        },
                    },
                )
            )

        return diagnostic

    def set_recommendation(
        self,
        command: SetRecommendationCommand,
        user: User,
    ) -> Diagnostic:
        """Set diagnostic recommendation."""

        require_role(
            user,
            UserRole.TECHNICIAN,
            UserRole.ADMIN,
        )

        with self._uow:
            diagnostic = self.get(
                command.diagnostic_id,
            )

            diagnostic.set_recommendation(
                command.recommendation,
            )

            self._repository.save(
                diagnostic,
            )

        return diagnostic
