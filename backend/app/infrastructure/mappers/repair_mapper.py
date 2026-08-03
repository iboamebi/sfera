"""
Repair mapper.
"""

from app.domains.repair.entities.repair import Repair
from app.domains.repair.value_objects.repair_status import (
    RepairStatus,
)
from app.models.repair import Repair as RepairModel
from app.models.repair import RepairStatus as RepairModelStatus


class RepairMapper:
    """Maps repair between domain and persistence."""

    @staticmethod
    def to_domain(
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

    @staticmethod
    def to_model(
        entity: Repair,
    ) -> RepairModel:
        """Convert domain entity to model."""

        return RepairModel(
            id=entity.id,
            order_item_id=entity.order_item_id,
            status=RepairModelStatus(
                entity.status.value,
            ),
            description=entity.description,
            result=entity.result,
        )
