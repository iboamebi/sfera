"""
Repair mapper.
"""

from app.domains.repair.entities.repair import Repair
from app.domains.repair.value_objects.repair_status import RepairStatus
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.repair import Repair as RepairModel
from app.models.repair import RepairStatus as RepairModelStatus


class RepairMapper(
    BaseMapper[
        Repair,
        RepairModel,
    ],
):
    """Maps repair between domain and persistence."""

    def to_domain(
        self,
        model: RepairModel,
    ) -> Repair:
        """Convert model to domain entity."""

        return Repair(
            id=model.id,
            order_item_id=model.order_item_id,
            status=RepairStatus(
                model.status.value,
            ),
            description=model.description,
            result=model.result,
        )

    def to_model(
        self,
        entity: Repair,
        model: RepairModel,
    ) -> RepairModel:
        """Convert domain entity to model."""

        model.order_item_id = entity.order_item_id
        model.status = RepairModelStatus(
            entity.status.value,
        )
        model.description = entity.description
        model.result = entity.result

        return model
