"""
Move workflow stage command.
"""

from dataclasses import dataclass

from app.domains.workflow.entities.workflow import Workflow
from app.domains.workflow.entities.workflow_instance import (
    WorkflowInstance,
)
from app.domains.workflow.services.workflow_service import (
    WorkflowService,
)


@dataclass(frozen=True)
class MoveWorkflowStageCommand:
    """Move workflow to next stage."""

    instance: WorkflowInstance
    workflow: Workflow


class MoveWorkflowStageHandler:
    """Handles workflow stage transition."""

    def __init__(
        self,
        service: WorkflowService | None = None,
    ) -> None:
        self.service = service or WorkflowService()

    def handle(
        self,
        command: MoveWorkflowStageCommand,
    ) -> None:
        self.service.next_stage(
            command.instance,
            command.workflow,
        )
