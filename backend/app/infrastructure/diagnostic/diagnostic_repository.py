"""
SQLAlchemy diagnostic repository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.diagnostic.entities.diagnostic import Diagnostic
from app.domains.diagnostic.repositories.diagnostic_repository import (
    DiagnosticRepository,
)
from app.infrastructure.mappers.diagnostic_mapper import DiagnosticMapper
from app.models.diagnostic import Diagnostic as DiagnosticModel


class DiagnosticRepositorySQLAlchemy(DiagnosticRepository):
    """SQLAlchemy implementation of diagnostic repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._mapper = DiagnosticMapper()

    def get(
        self,
        diagnostic_id: UUID,
    ) -> Diagnostic | None:
        """Get diagnostic by identifier."""

        model = self._session.get(
            DiagnosticModel,
            diagnostic_id,
        )

        if model is None:
            return None

        return self._mapper.to_domain(
            model,
        )

    def save(
        self,
        diagnostic: Diagnostic,
    ) -> None:
        """Save diagnostic."""

        model = self._session.get(
            DiagnosticModel,
            diagnostic.id,
        )

        if model is None:
            model = DiagnosticModel(
                id=diagnostic.id,
            )
            self._session.add(model)

        self._mapper.to_model(
            diagnostic,
            model,
        )

        self._session.flush()
