"""
Application service for Workflow.
"""

from uuid import UUID, uuid4

from app.application.workflow.commands.complete_workflow import (
    CompleteWorkflowCommand,
)
from app.application.workflow.commands.move_workflow_stage import (
    MoveWorkflowStageCommand,
)
from app.application.workflow.commands.start_workflow import (
    StartWorkflowCommand,
)
from app.application.workflow.exceptions import (
    WorkflowInstanceNotFoundApplicationError,
    WorkflowNotFoundApplicationError,
)
from app.domains.workflow.entities.workflow_instance import (
    WorkflowInstance,
)
from app.domains.workflow.repositories.workflow_repository import (
    WorkflowInstanceRepository,
    WorkflowRepository,
)
from app.domains.workflow.services.workflow_service import (
    WorkflowService,
)


class WorkflowApplicationService:
    """Coordinates workflow use cases."""

    def __init__(
        self,
        workflow_repository: WorkflowRepository,
        instance_repository: WorkflowInstanceRepository,
        service: WorkflowService | None = None,
    ) -> None:
        self._workflow_repository = workflow_repository
        self._instance_repository = instance_repository
        self._service = service or WorkflowService()

    def start(
        self,
        command: StartWorkflowCommand,
    ) -> WorkflowInstance:
        """Start workflow."""

        instance = WorkflowInstance(
            id=uuid4(),
            workflow_id=command.workflow_id,
            order_item_id=command.order_item_id,
        )

        self._service.start(instance)

        self._instance_repository.save_instance(
            instance,
        )

        return instance

    def move_next(
        self,
        command: MoveWorkflowStageCommand,
    ) -> WorkflowInstance:
        """Move workflow to next stage."""

        instance = self.get_instance(
            command.workflow_instance_id,
        )

        workflow = self._workflow_repository.get(
            command.workflow_id,
        )

        if workflow is None:
            raise WorkflowNotFoundApplicationError

        self._service.next_stage(
            instance,
            workflow,
        )

        self._instance_repository.save_instance(
            instance,
        )

        return instance

    def complete(
        self,
        command: CompleteWorkflowCommand,
    ) -> WorkflowInstance:
        """Complete workflow."""

        instance = self.get_instance(
            command.workflow_instance_id,
        )

        self._service.complete(instance)

        self._instance_repository.save_instance(
            instance,
        )

        return instance

    def get_instance(
        self,
        instance_id: UUID,
    ) -> WorkflowInstance:
        """Get workflow instance."""

        instance = self._instance_repository.get_instance(
            instance_id,
        )

        if instance is None:
            raise WorkflowInstanceNotFoundApplicationError

        return instance
