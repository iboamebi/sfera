"""Application query service for warehouse movement history."""

from datetime import datetime
from uuid import UUID

from app.domains.warehouse.read_models.warehouse_movement_read_models import (
    WarehouseMovementReadData,
)
from app.domains.warehouse.repositories.warehouse_movement_read_repository import (
    WarehouseMovementReadRepository,
)
from app.domains.warehouse.value_objects.movement_type import MovementType


class WarehouseMovementReadService:
    """Provides read access to warehouse movement history."""

    def __init__(self, repository: WarehouseMovementReadRepository) -> None:
        self._repository = repository

    def list_by_warehouse(
        self,
        warehouse_id: UUID,
        *,
        material_id: UUID | None = None,
        order_id: UUID | None = None,
        movement_type: MovementType | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[WarehouseMovementReadData], int]:
        return self._repository.list_by_warehouse(
            warehouse_id,
            material_id=material_id,
            order_id=order_id,
            movement_type=movement_type,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )
