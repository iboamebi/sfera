"""
Workflow instance mapper.
"""

from app.domains.workflow.entities.workflow_instance import (
    WorkflowInstance,
)
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.workflow_instance import (
    WorkflowInstance as WorkflowInstanceModel,
)


class WorkflowInstanceMapper(
    BaseMapper[WorkflowInstance, WorkflowInstanceModel],
):
    """Workflow instance mapper."""

    def to_domain(
        self,
        model: WorkflowInstanceModel,
    ) -> WorkflowInstance:
        return WorkflowInstance(
            id=model.id,
            workflow_id=model.workflow_id,
            order_item_id=model.order_item_id,
            current_stage=model.current_stage,
            status=model.status,
        )

    def to_model(
        self,
        entity: WorkflowInstance,
        model: WorkflowInstanceModel,
    ) -> WorkflowInstanceModel:
        model.workflow_id = entity.workflow_id
        model.order_item_id = entity.order_item_id
        model.current_stage = entity.current_stage
        model.status = entity.status.value

        return model
