"""
SQLAlchemy implementation of WorkflowRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.domains.workflow.entities.workflow import Workflow as DomainWorkflow
from app.domains.workflow.repositories.workflow_repository import (
    WorkflowRepository,
)
from app.infrastructure.mappers.workflow_mapper import WorkflowMapper
from app.models.workflow import Workflow as ORMWorkflow


class WorkflowRepositorySQLAlchemy(
    WorkflowRepository,
):
    """SQLAlchemy workflow repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
        self.mapper = WorkflowMapper()

    def get(
        self,
        workflow_id: UUID,
    ) -> DomainWorkflow | None:
        """Get workflow by identifier."""

        model = (
            self.session.query(ORMWorkflow)
            .options(
                selectinload(
                    ORMWorkflow.stages,
                ),
            )
            .filter(
                ORMWorkflow.id == workflow_id,
            )
            .first()
        )

        if model is None:
            return None

        return self.mapper.to_domain(model)

    def save(
        self,
        workflow: DomainWorkflow,
    ) -> None:
        """Save workflow."""

        model = (
            self.session.query(ORMWorkflow)
            .filter(
                ORMWorkflow.id == workflow.id,
            )
            .first()
        )

        if model is None:
            model = self.mapper.create_model(
                workflow,
            )

            self.session.add(model)

        else:
            self.mapper.to_model(
                workflow,
                model,
            )

        self.session.flush()
