"""
Create warehouse movement command.
"""

from dataclasses import dataclass
from uuid import UUID

from app.domains.warehouse.value_objects.movement_type import (
    MovementType,
)


@dataclass(frozen=True)
class CreateMovementCommand:
    """Create warehouse movement command."""

    warehouse_id: UUID
    material_id: UUID
    movement_type: MovementType
    quantity: float
    order_id: UUID | None = None
    comment: str | None = None
