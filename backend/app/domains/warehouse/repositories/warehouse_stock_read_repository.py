"""
Warehouse stock read repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.warehouse.read_models.warehouse_stock_read_models import (
    WarehouseStockReadData,
)


class WarehouseStockReadRepository(ABC):
    """Read repository interface for warehouse stock."""

    @abstractmethod
    def get_by_warehouse(
        self,
        warehouse_id: UUID,
    ) -> list[WarehouseStockReadData]:
        """Get warehouse stock read data."""
        raise NotImplementedError
