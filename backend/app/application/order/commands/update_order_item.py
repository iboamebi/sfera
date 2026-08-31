"""Command for updating an order item."""

from uuid import UUID

from app.domains.order.value_objects.order_item_operation import OrderItemOperation


class UpdateOrderItemCommand:
    """Describe editable fields of an order item."""

    def __init__(
        self,
        order_id: UUID,
        item_id: UUID,
        requested_operations: frozenset[OrderItemOperation],
    ) -> None:
        self.order_id = order_id
        self.item_id = item_id
        self.requested_operations = requested_operations
