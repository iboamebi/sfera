"""
Workflow domain service.
"""

from app.domains.workflow.entities.workflow import Workflow
from app.domains.workflow.entities.workflow_instance import WorkflowInstance


class WorkflowService:
    """Workflow business rules."""

    def start(
        self,
        instance: WorkflowInstance,
    ) -> None:
        """Start workflow execution."""
        instance.start()

    def next_stage(
        self,
        instance: WorkflowInstance,
        workflow: Workflow,
    ) -> None:
        """Move workflow to next stage."""
        instance.move_next(
            last_stage=len(workflow.stages),
        )

    def complete(
        self,
        instance: WorkflowInstance,
    ) -> None:
        """Complete workflow."""
        instance.complete()
