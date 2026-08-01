"""
SQLAlchemy implementation of WorkflowInstanceRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.workflow.entities.workflow_instance import (
    WorkflowInstance as DomainWorkflowInstance,
)
from app.domains.workflow.repositories.workflow_repository import (
    WorkflowInstanceRepository,
)
from app.infrastructure.mappers.workflow_instance_mapper import (
    WorkflowInstanceMapper,
)
from app.models.workflow_instance import (
    WorkflowInstance as ORMWorkflowInstance,
)


class WorkflowInstanceRepositorySQLAlchemy(
    WorkflowInstanceRepository,
):
    """SQLAlchemy workflow instance repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
        self.mapper = WorkflowInstanceMapper()

    def get_instance(
        self,
        instance_id: UUID,
    ) -> DomainWorkflowInstance | None:
        """Get workflow instance by identifier."""

        model = (
            self.session.query(ORMWorkflowInstance)
            .filter(ORMWorkflowInstance.id == instance_id)
            .first()
        )

        if model is None:
            return None

        return self.mapper.to_domain(model)

    def save_instance(
        self,
        instance: DomainWorkflowInstance,
    ) -> None:
        """Save workflow instance."""

        model = (
            self.session.query(ORMWorkflowInstance)
            .filter(ORMWorkflowInstance.id == instance.id)
            .first()
        )

        if model is None:
            model = ORMWorkflowInstance(
                id=instance.id,
                workflow_id=instance.workflow_id,
                order_item_id=instance.order_item_id,
                current_stage=instance.current_stage,
                status=instance.status.value,
            )

            self.session.add(model)

        else:
            self.mapper.to_model(
                instance,
                model,
            )

        self.session.flush()
