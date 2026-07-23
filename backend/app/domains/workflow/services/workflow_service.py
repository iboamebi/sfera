"""
Workflow domain service.

Contains business operations for workflow processing.
"""

from __future__ import annotations

from app.domains.workflow.entities.workflow import Workflow
from app.domains.workflow.entities.workflow_stage import WorkflowStage


class WorkflowService:
    """Workflow business service."""

    def add_stage(
        self,
        workflow: Workflow,
        stage: WorkflowStage,
    ) -> Workflow:
        """Add stage to workflow."""

        workflow.add_stage(stage)

        return workflow

    def get_next_stage(
        self,
        workflow: Workflow,
        current_order: int,
    ) -> WorkflowStage | None:
        """Return next stage after current stage."""

        return next(
            (stage for stage in workflow.stages if stage.order > current_order),
            None,
        )

    def can_complete(
        self,
        workflow: Workflow,
        stage_order: int,
    ) -> bool:
        """Check if stage can be completed."""

        stage = workflow.get_stage(stage_order)

        if stage is None:
            return False

        if stage.required and stage_order != len(workflow.stages):
            return False

        return True
