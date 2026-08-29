"""
Remove order item command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RemoveOrderItemCommand:
    """Command for removing an item from an order."""

    order_id: UUID
    item_id: UUID
