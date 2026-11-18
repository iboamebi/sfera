"""Warehouse movement read repository contract."""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.domains.warehouse.read_models.warehouse_movement_read_models import (
    WarehouseMovementReadData,
)
from app.domains.warehouse.value_objects.movement_type import MovementType


class WarehouseMovementReadRepository(ABC):
    """Read-only access to warehouse movement history."""

    @abstractmethod
    def list_by_warehouse(
        self,
        warehouse_id: UUID,
        *,
        material_id: UUID | None,
        order_id: UUID | None,
        movement_type: MovementType | None,
        date_from: datetime | None,
        date_to: datetime | None,
        limit: int,
        offset: int,
    ) -> tuple[list[WarehouseMovementReadData], int]:
        """Return a page of movements and the total matching count."""
        raise NotImplementedError
