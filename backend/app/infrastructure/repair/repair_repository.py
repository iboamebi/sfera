"""
SQLAlchemy repair repository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.repair.entities.repair import Repair
from app.domains.repair.repositories.repair_repository import (
    RepairRepository,
)
from app.infrastructure.mappers.repair_mapper import RepairMapper
from app.models.repair import Repair as RepairModel


class RepairRepositorySQLAlchemy(RepairRepository):
    """SQLAlchemy implementation of repair repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._mapper = RepairMapper()

    def get(
        self,
        repair_id: UUID,
    ) -> Repair | None:
        """Get repair by identifier."""

        model = self._session.get(
            RepairModel,
            repair_id,
        )

        if model is None:
            return None

        return self._mapper.to_domain(
            model,
        )

    def save(
        self,
        repair: Repair,
    ) -> None:
        """Save repair."""

        model = self._session.get(
            RepairModel,
            repair.id,
        )

        if model is None:
            model = RepairModel(
                id=repair.id,
            )
            self._session.add(model)

        self._mapper.to_model(
            repair,
            model,
        )

        self._session.flush()
