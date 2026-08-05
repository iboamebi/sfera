"""
Workflow stage entity.

Represents a single stage of a workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.shared.base.entity import Entity


@dataclass(eq=False, slots=True)
class WorkflowStage(Entity):
    """Workflow stage."""

    workflow_id: UUID
    order: int
    code: str
    name: str

    performer_role: str | None = None
    required: bool = True

    def is_first(self) -> bool:
        """Return True if stage is the first in workflow."""
        return self.order == 1

    def is_after(self, stage: WorkflowStage) -> bool:
        """Return True if current stage follows the specified stage."""
        return self.order > stage.order
