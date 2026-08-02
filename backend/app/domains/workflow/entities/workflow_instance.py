"""
Workflow instance aggregate.

Represents execution of workflow for an OrderItem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domains.workflow.value_objects.workflow_status import (
    WorkflowStatus,
)


@dataclass(slots=True)
class WorkflowInstance:
    """Workflow execution instance."""

    workflow_id: UUID
    order_item_id: UUID

    current_stage: int = 1
    status: WorkflowStatus = WorkflowStatus.CREATED

    id: UUID = field(default_factory=uuid4)

    def start(self) -> None:
        """Start workflow."""
        self.status = WorkflowStatus.IN_PROGRESS

    def move_next(self, last_stage: int) -> None:
        """Move workflow to next stage."""
        if self.current_stage >= last_stage:
            self.status = WorkflowStatus.COMPLETED
            return

        self.current_stage += 1

    def complete(self) -> None:
        """Complete workflow."""
        self.status = WorkflowStatus.COMPLETED

    def cancel(self) -> None:
        """Cancel workflow."""
        self.status = WorkflowStatus.CANCELLED
