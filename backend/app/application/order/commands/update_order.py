"""
Update order command.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class UpdateOrderCommand:
    """Command for updating an order."""

    order_id: UUID
    planned_issue_at: datetime | None = None
    comment: str | None = None
