"""
Application service for Workflow.
"""

from app.domains.workflow.entities.workflow import Workflow
from app.domains.workflow.entities.workflow_instance import (
    WorkflowInstance,
)
from app.domains.workflow.services.workflow_service import (
    WorkflowService,
)


class WorkflowApplicationService:
    """Coordinates workflow use cases."""

    def __init__(
        self,
        service: WorkflowService | None = None,
    ) -> None:
        self._service = service or WorkflowService()

    def start(
        self,
        instance: WorkflowInstance,
    ) -> WorkflowInstance:
        """Start workflow."""

        self._service.start(instance)

        return instance

    def move_next(
        self,
        instance: WorkflowInstance,
        workflow: Workflow,
    ) -> WorkflowInstance:
        """Move workflow to next stage."""

        self._service.next_stage(
            instance,
            workflow,
        )

        return instance

    def complete(
        self,
        instance: WorkflowInstance,
    ) -> WorkflowInstance:
        """Complete workflow."""

        self._service.complete(instance)

        return instance
