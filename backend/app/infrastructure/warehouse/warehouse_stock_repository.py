"""
SQLAlchemy warehouse stock repository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.warehouse.entities.warehouse_stock import (
    WarehouseStock,
)
from app.domains.warehouse.repositories.warehouse_stock_repository import (
    WarehouseStockRepository,
)
from app.infrastructure.mappers.warehouse_stock_mapper import (
    WarehouseStockMapper,
)
from app.models.warehouse_stock import (
    WarehouseStock as WarehouseStockModel,
)


class WarehouseStockRepositorySQLAlchemy(
    WarehouseStockRepository,
):
    """SQLAlchemy warehouse stock repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_material(
        self,
        warehouse_id: UUID,
        material_id: UUID,
    ) -> WarehouseStock | None:
        model = (
            self._session.query(
                WarehouseStockModel,
            )
            .filter(
                WarehouseStockModel.warehouse_id == warehouse_id,
                WarehouseStockModel.material_id == material_id,
            )
            .first()
        )

        if model is None:
            return None

        return WarehouseStockMapper.to_domain(
            model,
        )

    def save(
        self,
        stock: WarehouseStock,
    ) -> None:
        model = WarehouseStockMapper.to_model(
            stock,
        )

        self._session.merge(
            model,
        )
