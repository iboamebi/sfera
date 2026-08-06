"""
Workflow aggregate root.

Defines a workflow consisting of ordered stages used to process an OrderItem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from app.domains.workflow.entities.workflow_stage import WorkflowStage
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False)
class Workflow(AggregateRoot):
    """Workflow aggregate."""

    name: str
    code: str
    description: str | None = None
    is_active: bool = True

    stages: list[WorkflowStage] = field(default_factory=list)

    def add_stage(
        self,
        stage: WorkflowStage,
    ) -> None:
        """Add stage to workflow."""

        self.stages.append(stage)
        self.stages.sort(key=lambda item: item.order)

    def remove_stage(
        self,
        stage_id: UUID,
    ) -> None:
        """Remove stage from workflow."""

        self.stages = [stage for stage in self.stages if stage.id != stage_id]

    def get_stage(
        self,
        order: int,
    ) -> WorkflowStage | None:
        """Return stage by order."""

        return next(
            (stage for stage in self.stages if stage.order == order),
            None,
        )

    def first_stage(self) -> WorkflowStage | None:
        """Return first workflow stage."""

        return self.get_stage(1)
