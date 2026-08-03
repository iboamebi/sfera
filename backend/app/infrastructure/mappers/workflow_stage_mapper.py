"""
Workflow stage mapper.
"""

from app.domains.workflow.entities.workflow_stage import (
    WorkflowStage,
)
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.workflow_stage import (
    WorkflowStage as WorkflowStageModel,
)


class WorkflowStageMapper(
    BaseMapper[WorkflowStage, WorkflowStageModel],
):
    """Workflow stage mapper."""

    def to_domain(
        self,
        model: WorkflowStageModel,
    ) -> WorkflowStage:
        return WorkflowStage(
            id=model.id,
            workflow_id=model.workflow_id,
            order=model.order,
            code=model.code,
            name=model.name,
            performer_role=model.performer_role,
            required=model.required,
        )

    def to_model(
        self,
        entity: WorkflowStage,
        model: WorkflowStageModel,
    ) -> WorkflowStageModel:
        model.workflow_id = entity.workflow_id
        model.order = entity.order
        model.code = entity.code
        model.name = entity.name
        model.performer_role = entity.performer_role
        model.required = entity.required

        return model
