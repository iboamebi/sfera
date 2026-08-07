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
        self._mapper = WarehouseStockMapper()

    def get_by_material(
        self,
        warehouse_id: UUID,
        material_id: UUID,
    ) -> WarehouseStock | None:
        """Get stock by warehouse and material."""

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

        return self._mapper.to_domain(
            model,
        )

    def save(
        self,
        stock: WarehouseStock,
    ) -> None:
        """Save warehouse stock."""

        model = self._session.get(
            WarehouseStockModel,
            stock.id,
        )

        if model is None:
            model = WarehouseStockModel(
                id=stock.id,
            )
            self._session.add(model)

        self._mapper.to_model(
            stock,
            model,
        )

        self._session.flush()
