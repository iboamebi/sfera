"""
SQLAlchemy warehouse repository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.warehouse.entities.warehouse import Warehouse
from app.domains.warehouse.repositories.warehouse_repository import (
    WarehouseRepository,
)
from app.infrastructure.mappers.warehouse_mapper import (
    WarehouseMapper,
)
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

    def get(
        self,
        warehouse_id: UUID,
    ) -> Warehouse | None:
        model = self._session.get(
            WarehouseModel,
            warehouse_id,
        )

        if model is None:
            return None

        return WarehouseMapper.to_domain(
            model,
        )

    def save(
        self,
        warehouse: Warehouse,
    ) -> None:
        model = WarehouseMapper.to_model(
            warehouse,
        )

        self._session.merge(
            model,
        )
