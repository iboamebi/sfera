"""
Add order item command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddOrderItemCommand:
    """Command for adding an item to an order."""

    order_id: UUID
    instrument_id: UUID | None = None
