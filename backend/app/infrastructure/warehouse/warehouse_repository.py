"""
SQLAlchemy warehouse repository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.warehouse.entities.warehouse import Warehouse
from app.domains.warehouse.repositories.warehouse_repository import (
    WarehouseRepository,
)
from app.infrastructure.mappers.warehouse_mapper import WarehouseMapper
from app.models.warehouse import Warehouse as WarehouseModel


class WarehouseRepositorySQLAlchemy(
    WarehouseRepository,
):
    """SQLAlchemy warehouse repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._mapper = WarehouseMapper()

    def get(
        self,
        warehouse_id: UUID,
    ) -> Warehouse | None:
        """Get warehouse by identifier."""

        model = self._session.get(
            WarehouseModel,
            warehouse_id,
        )

        if model is None:
            return None

        return self._mapper.to_domain(
            model,
        )

    def save(
        self,
        warehouse: Warehouse,
    ) -> None:
        """Save warehouse."""

        model = self._session.get(
            WarehouseModel,
            warehouse.id,
        )

        if model is None:
            model = WarehouseModel(
                id=warehouse.id,
            )
            self._session.add(model)

        self._mapper.to_model(
            warehouse,
            model,
        )

        self._session.flush()
