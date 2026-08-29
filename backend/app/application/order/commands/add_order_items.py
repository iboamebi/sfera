"""
Add multiple order items to an order.
"""

from dataclasses import dataclass, field
from uuid import UUID

from app.domains.order.value_objects.order_item_operation import OrderItemOperation


@dataclass(frozen=True)
class AddOrderItemsCommand:
    """Command for mass intake of items known only by instrument type."""

    order_id: UUID
    instrument_type_id: UUID
    quantity: int
    requested_operations: frozenset[OrderItemOperation] = field(
        default_factory=frozenset,
    )
