"""
Warehouse stock read service.
"""

from uuid import UUID

from app.domains.warehouse.read_models.warehouse_stock_read_models import (
    WarehouseStockReadData,
)
from app.domains.warehouse.repositories.warehouse_stock_read_repository import (
    WarehouseStockReadRepository,
)


class WarehouseStockReadService:
    """Provides warehouse stock read operations."""

    def __init__(
        self,
        repository: WarehouseStockReadRepository,
    ) -> None:
        self._repository = repository

    def get_by_warehouse(
        self,
        warehouse_id: UUID,
    ) -> list[WarehouseStockReadData]:
        """Get warehouse stock read data."""
        return self._repository.get_by_warehouse(warehouse_id)
