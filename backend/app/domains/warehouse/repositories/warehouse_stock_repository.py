"""
Warehouse stock repository interface.
"""

from abc import abstractmethod
from uuid import UUID

from app.domains.warehouse.entities.warehouse_stock import (
    WarehouseStock,
)
from app.shared.base.repository import Repository


class WarehouseStockRepository(
    Repository[WarehouseStock],
):
    """Warehouse stock repository interface."""

    @abstractmethod
    def get_by_material(
        self,
        warehouse_id: UUID,
        material_id: UUID,
    ) -> WarehouseStock | None:
        """Get stock by warehouse and material."""

    @abstractmethod
    def save(
        self,
        stock: WarehouseStock,
    ) -> None:
        """Save stock."""
