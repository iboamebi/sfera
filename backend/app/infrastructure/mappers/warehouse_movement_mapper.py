"""
Warehouse movement mapper.
"""

from app.domains.warehouse.entities.warehouse_movement import (
    WarehouseMovement,
)
from app.domains.warehouse.value_objects.movement_type import (
    MovementType as DomainMovementType,
)
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.warehouse_movement import (
    MovementType as ModelMovementType,
)
from app.models.warehouse_movement import (
    WarehouseMovement as WarehouseMovementModel,
)


class WarehouseMovementMapper(
    BaseMapper[
        WarehouseMovement,
        WarehouseMovementModel,
    ],
):
    """Map warehouse movement between domain and ORM."""

    def to_domain(
        self,
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

    def to_model(
        self,
        entity: WarehouseMovement,
        model: WarehouseMovementModel,
    ) -> WarehouseMovementModel:
        model.warehouse_id = entity.warehouse_id
        model.material_id = entity.material_id
        model.order_id = entity.order_id
        model.movement_type = ModelMovementType(
            entity.movement_type.value,
        )
        model.quantity = entity.quantity
        model.comment = entity.comment
        model.archived = entity.archived

        return model
