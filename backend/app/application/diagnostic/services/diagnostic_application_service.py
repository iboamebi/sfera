"""
Application service for diagnostic use cases.
"""

from uuid import UUID, uuid4

from app.application.diagnostic.commands.create_diagnostic import (
    CreateDiagnosticCommand,
)
from app.application.diagnostic.exceptions import (
    DiagnosticNotFoundApplicationError,
)
from app.domains.diagnostic.entities.diagnostic import Diagnostic
from app.domains.diagnostic.repositories.diagnostic_repository import (
    DiagnosticRepository,
)
from app.domains.diagnostic.value_objects.recommendation import (
    Recommendation,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class DiagnosticApplicationService:
    """Coordinates diagnostic use cases."""

    def __init__(
        self,
        repository: DiagnosticRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = unit_of_work

    def get(
        self,
        diagnostic_id: UUID,
    ) -> Diagnostic:
        diagnostic = self._repository.get(
            diagnostic_id,
        )

        if diagnostic is None:
            raise DiagnosticNotFoundApplicationError

        return diagnostic

    def create(
        self,
        command: CreateDiagnosticCommand,
    ) -> Diagnostic:
        diagnostic = Diagnostic(
            id=uuid4(),
            order_item_id=command.order_item_id,
        )

        with self._uow:
            self._repository.save(
                diagnostic,
            )

        return diagnostic

    def update_conclusion(
        self,
        diagnostic_id: UUID,
        conclusion: str,
    ) -> Diagnostic:
        with self._uow:
            diagnostic = self.get(
                diagnostic_id,
            )

            diagnostic.update_conclusion(
                conclusion,
            )

            self._repository.save(
                diagnostic,
            )

        return diagnostic

    def set_recommendation(
        self,
        diagnostic_id: UUID,
        recommendation: Recommendation,
    ) -> Diagnostic:
        with self._uow:
            diagnostic = self.get(
                diagnostic_id,
            )

            diagnostic.set_recommendation(
                recommendation,
            )

            self._repository.save(
                diagnostic,
            )

        return diagnostic
