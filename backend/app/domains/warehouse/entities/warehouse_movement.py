"""
Warehouse movement domain entity.
"""

from dataclasses import dataclass
from uuid import UUID

from app.domains.warehouse.value_objects.movement_type import (
    MovementType,
)
from app.shared.base.entity import Entity


@dataclass(eq=False)
class WarehouseMovement(Entity):
    """Warehouse movement entity."""

    warehouse_id: UUID
    material_id: UUID
    movement_type: MovementType
    quantity: float
    order_id: UUID | None = None
    comment: str | None = None

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(
                "Movement quantity must be positive",
            )
