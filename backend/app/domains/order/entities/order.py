"""
Order aggregate root.
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.domains.order.entities.order_item import OrderItem
from app.domains.order.events.order_registered import OrderRegistered
from app.domains.order.exceptions.order_exception import OrderException
from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.order.value_objects.order_status import OrderStatus
from app.shared.base.aggregate import AggregateRoot


@dataclass
class Order(AggregateRoot):
    """Order aggregate."""

    number: OrderNumber
    customer_id: UUID
    received_at: datetime

    planned_issue_at: datetime | None = None
    issued_at: datetime | None = None
    comment: str | None = None

    status: OrderStatus = OrderStatus.NEW
    archived: bool = False

    items: list[OrderItem] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        id: UUID,
        number: OrderNumber,
        customer_id: UUID,
        received_at: datetime,
        planned_issue_at: datetime | None = None,
        comment: str | None = None,
    ) -> "Order":
        """Create a new Order aggregate."""

        return cls(
            id=id,
            number=number,
            customer_id=customer_id,
            received_at=received_at,
            planned_issue_at=planned_issue_at,
            comment=comment,
        )

    def add_item(self, item: OrderItem) -> None:
        """Add item to a new order."""

        if self.status != OrderStatus.NEW:
            raise OrderException("Cannot add item to active order")

        if item.instrument_id is not None and any(
            existing.instrument_id == item.instrument_id
            for existing in self.items
        ):
            raise OrderException("Instrument already exists in order")

        self.items.append(item)

    def update_item(
        self,
        item_id: UUID,
        requested_operations: set[OrderItemOperation],
    ) -> None:
        """Update an order item while the order is new."""

        if self.status != OrderStatus.NEW:
            raise OrderException("Cannot update item in active order")

        for item in self.items:
            if item.id == item_id:
                item.requested_operations = requested_operations
                return

        raise OrderException("Order item not found")

    def remove_item(self, item_id: UUID) -> None:
        """Remove an order item while the order is new."""

        if self.status != OrderStatus.NEW:
            raise OrderException("Cannot remove item from active order")

        for index, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(index)
                return

        raise OrderException("Order item not found")

    def update_details(
        self,
        *,
        planned_issue_at: datetime | None = None,
        comment: str | None = None,
    ) -> None:
        """Update editable order details."""

        self.planned_issue_at = planned_issue_at
        self.comment = comment

    def register(self) -> None:
        """Register the order."""

        if not self.items:
            raise OrderException("Order must contain items")

        self.status = OrderStatus.REGISTERED
        self.add_event(OrderRegistered(order_id=self.id))
