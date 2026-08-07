"""
Workflow mapper.
"""

from app.domains.workflow.entities.workflow import Workflow
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.infrastructure.mappers.workflow_stage_mapper import (
    WorkflowStageMapper,
)
from app.models.workflow import Workflow as WorkflowModel


class WorkflowMapper(BaseMapper[Workflow, WorkflowModel]):
    """Workflow mapper."""

    def __init__(self) -> None:
        self.stage_mapper = WorkflowStageMapper()

    def to_domain(
        self,
        model: WorkflowModel,
    ) -> Workflow:
        return Workflow(
            id=model.id,
            name=model.name,
            code=model.code,
            description=model.description,
            is_active=model.is_active,
            stages=[self.stage_mapper.to_domain(stage) for stage in model.stages],
        )

    def to_model(
        self,
        entity: Workflow,
        model: WorkflowModel,
    ) -> WorkflowModel:
        model.name = entity.name
        model.code = entity.code
        model.description = entity.description
        model.is_active = entity.is_active

        return model

    def create_model(
        self,
        entity: Workflow,
    ) -> WorkflowModel:
        """Create ORM model from domain entity."""

        return WorkflowModel(
            id=entity.id,
            name=entity.name,
            code=entity.code,
            description=entity.description,
            is_active=entity.is_active,
        )
