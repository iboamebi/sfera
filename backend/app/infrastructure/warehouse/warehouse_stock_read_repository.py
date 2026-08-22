"""
SQLAlchemy implementation of WarehouseStockReadRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.warehouse.read_models.warehouse_stock_read_models import (
    WarehouseStockReadData,
)
from app.domains.warehouse.repositories.warehouse_stock_read_repository import (
    WarehouseStockReadRepository,
)
from app.models.material import Material
from app.models.warehouse import Warehouse
from app.models.warehouse_stock import WarehouseStock


class WarehouseStockReadRepositorySQLAlchemy(
    WarehouseStockReadRepository,
):
    """SQLAlchemy read repository for warehouse stock."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def get_by_warehouse(
        self,
        warehouse_id: UUID,
    ) -> list[WarehouseStockReadData]:
        rows = (
            self.session.query(
                WarehouseStock,
                Warehouse.name,
                Material.name,
            )
            .join(
                Warehouse,
                Warehouse.id == WarehouseStock.warehouse_id,
            )
            .join(
                Material,
                Material.id == WarehouseStock.material_id,
            )
            .filter(
                WarehouseStock.warehouse_id == warehouse_id,
            )
            .all()
        )

        return [
            WarehouseStockReadData(
                id=stock.id,
                warehouse_id=stock.warehouse_id,
                warehouse_name=warehouse_name,
                material_id=stock.material_id,
                material_name=material_name,
                quantity=stock.quantity,
                reserved_quantity=stock.reserved_quantity,
                available_quantity=(
                    stock.quantity - stock.reserved_quantity
                ),
            )
            for stock, warehouse_name, material_name in rows
        ]
