"""Warehouse movement read models."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domains.warehouse.value_objects.movement_type import MovementType


@dataclass(frozen=True, kw_only=True)
class WarehouseMovementReadData:
    """Read data for one immutable warehouse movement."""

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
