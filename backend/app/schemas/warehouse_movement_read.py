"""Warehouse movement history response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.domains.warehouse.value_objects.movement_type import MovementType


class WarehouseMovementListRead(BaseModel):
    """One warehouse movement in the history."""

    id: UUID
    warehouse_id: UUID
    warehouse_name: str
    material_id: UUID
    material_name: str
    order_id: UUID | None
    order_number: str | None
    movement_type: MovementType
    quantity: float
    comment: str | None
    created_at: datetime


class WarehouseMovementPageRead(BaseModel):
    """Paginated warehouse movement history."""

    items: list[WarehouseMovementListRead]
    total: int
    limit: int
    offset: int
