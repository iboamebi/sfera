"""Command for deleting an order item."""

from uuid import UUID


class DeleteOrderItemCommand:
    """Identify an order item to delete."""

    def __init__(self, order_id: UUID, item_id: UUID) -> None:
        self.order_id = order_id
        self.item_id = item_id
