"""
Warehouse movement mapper.
"""

from app.domains.warehouse.entities.warehouse_movement import (
    WarehouseMovement,
)
from app.domains.warehouse.value_objects.movement_type import (
    MovementType as DomainMovementType,
)
from app.models.warehouse_movement import (
    MovementType as ModelMovementType,
)
from app.models.warehouse_movement import (
    WarehouseMovement as WarehouseMovementModel,
)


class WarehouseMovementMapper:
    """Map warehouse movement between domain and ORM."""

    @staticmethod
    def to_domain(
        model: WarehouseMovementModel,
    ) -> WarehouseMovement:
        return WarehouseMovement(
            id=model.id,
            warehouse_id=model.warehouse_id,
            material_id=model.material_id,
            order_id=model.order_id,
            movement_type=DomainMovementType(
                model.movement_type.value,
            ),
            quantity=float(model.quantity),
            comment=model.comment,
            archived=model.archived,
        )

    @staticmethod
    def to_model(
        entity: WarehouseMovement,
    ) -> WarehouseMovementModel:
        return WarehouseMovementModel(
            id=entity.id,
            warehouse_id=entity.warehouse_id,
            material_id=entity.material_id,
            order_id=entity.order_id,
            movement_type=ModelMovementType(
                entity.movement_type.value,
            ),
            quantity=entity.quantity,
            comment=entity.comment,
            archived=entity.archived,
        )
