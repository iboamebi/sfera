"""
Complete workflow command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CompleteWorkflowCommand:
    """Complete workflow."""

    workflow_instance_id: UUID
