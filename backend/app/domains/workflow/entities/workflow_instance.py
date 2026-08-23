"""
Workflow instance aggregate.

Represents execution of workflow for an OrderItem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.domains.workflow.value_objects.workflow_status import (
    WorkflowStatus,
)
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False, kw_only=True, slots=True)
class WorkflowInstance(AggregateRoot):
    """Workflow execution instance."""

    workflow_id: UUID
    order_item_id: UUID

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    completed_at: datetime | None = None

    current_stage: int = 1
    status: WorkflowStatus = WorkflowStatus.CREATED

    @classmethod
    def create(
        cls,
        *,
        id: UUID,
        workflow_id: UUID,
        order_item_id: UUID,
    ) -> WorkflowInstance:
        """Create a new workflow instance."""

        return cls(
            id=id,
            workflow_id=workflow_id,
            order_item_id=order_item_id,
            created_at=datetime.now(UTC),
        )

    def start(self) -> None:
        """Start workflow."""

        self.status = WorkflowStatus.IN_PROGRESS
        self.started_at = datetime.now(UTC)

    def move_next(
        self,
        last_stage: int,
    ) -> None:
        """Move workflow to next stage."""

        if self.current_stage >= last_stage:
            self.status = WorkflowStatus.COMPLETED
            self.completed_at = datetime.now(UTC)
            return

        self.current_stage += 1

    def complete(self) -> None:
        """Complete workflow."""

        self.status = WorkflowStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def cancel(self) -> None:
        """Cancel workflow."""

        self.status = WorkflowStatus.CANCELLED
