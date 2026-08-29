"""
Add order item command.
"""

from dataclasses import dataclass, field
from uuid import UUID

from app.domains.order.value_objects.order_item_operation import OrderItemOperation


@dataclass(frozen=True)
class AddOrderItemCommand:
    """Command for adding an item and its requested operations to an order."""

    order_id: UUID
    instrument_id: UUID | None = None
    requested_operations: frozenset[OrderItemOperation] = field(
        default_factory=frozenset,
    )
