"""
Start workflow command.
"""

from dataclasses import dataclass

from app.domains.workflow.entities.workflow_instance import (
    WorkflowInstance,
)
from app.domains.workflow.services.workflow_service import (
    WorkflowService,
)


@dataclass(frozen=True)
class StartWorkflowCommand:
    """Start workflow command."""

    instance: WorkflowInstance


class StartWorkflowHandler:
    """Handles workflow start."""

    def __init__(
        self,
        service: WorkflowService | None = None,
    ) -> None:
        self.service = service or WorkflowService()

    def handle(
        self,
        command: StartWorkflowCommand,
    ) -> None:
        self.service.start(
            command.instance,
        )
