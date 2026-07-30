"""
SQLAlchemy repair repository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.repair.entities.repair import Repair
from app.domains.repair.repositories.repair_repository import (
    RepairRepository,
)
from app.infrastructure.mappers.repair_mapper import (
    RepairMapper,
)
from app.models.repair import Repair as RepairModel


class RepairRepositorySQLAlchemy(RepairRepository):
    """SQLAlchemy implementation of repair repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get(
        self,
        repair_id: UUID,
    ) -> Repair | None:
        model = self._session.get(
            RepairModel,
            repair_id,
        )

        if model is None:
            return None

        return RepairMapper.to_domain(
            model,
        )

    def save(
        self,
        repair: Repair,
    ) -> None:
        model = RepairMapper.to_model(
            repair,
        )

        self._session.merge(
            model,
        )
