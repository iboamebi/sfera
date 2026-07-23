"""
Workflow stage entity.

Represents a single stage of a workflow.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class WorkflowStage:
    """Workflow stage."""

    workflow_id: UUID
    order: int
    code: str
    name: str

    performer_role: str | None = None
    required: bool = True

    id: UUID = field(default_factory=uuid4)

    def is_first(self) -> bool:
        """Return True if stage is the first in workflow."""
        return self.order == 1

    def is_after(self, stage: WorkflowStage) -> bool:
        """Return True if current stage follows the specified stage."""
        return self.order > stage.order
