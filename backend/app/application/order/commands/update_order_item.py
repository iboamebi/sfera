"""Update order item command."""

from dataclasses import dataclass
from uuid import UUID

from app.domains.order.value_objects.order_item_operation import OrderItemOperation


@dataclass(frozen=True)
class UpdateOrderItemCommand:
    """Command for updating requested operations of an order item."""

    order_id: UUID
    item_id: UUID
    requested_operations: frozenset[OrderItemOperation]
