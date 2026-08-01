"""
Start workflow command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class StartWorkflowCommand:
    """Start workflow command."""

    workflow_id: UUID
    order_item_id: UUID
