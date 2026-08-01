"""
Workflow mapper.
"""

from app.domains.workflow.entities.workflow import Workflow
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.workflow import Workflow as WorkflowModel


class WorkflowMapper(BaseMapper[Workflow, WorkflowModel]):
    """Workflow mapper."""

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
