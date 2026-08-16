"""
Create order command.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class CreateOrderCommand:
    """Command for creating an order."""

    customer_id: UUID
    number: str
    planned_issue_at: datetime | None = None
    comment: str | None = None
