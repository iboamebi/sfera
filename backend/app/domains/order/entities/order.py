"""
Order aggregate root.
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.domains.order.entities.order_item import OrderItem
from app.domains.order.events.order_registered import OrderRegistered
from app.domains.order.exceptions.order_exception import OrderException
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
    def create(cls, *, id: UUID, number: OrderNumber, customer_id: UUID, received_at: datetime, planned_issue_at: datetime | None = None, comment: str | None = None) -> "Order":
        """Create a new Order aggregate."""
        return cls(id=id, number=number, customer_id=customer_id, received_at=received_at, planned_issue_at=planned_issue_at, comment=comment)

    def add_item(self, item: OrderItem) -> None:
        """Add item to a new order."""
        if self.status != OrderStatus.NEW:
            raise OrderException("Cannot add item to active order")
        if item.instrument_id is not None and any(existing.instrument_id == item.instrument_id for existing in self.items):
            raise OrderException("Instrument already exists in order")
        self.items.append(item)

    def assign_instrument(self, item_id: UUID, instrument_id: UUID) -> None:
        """Assign a concrete instrument to an order item."""
        if self.status != OrderStatus.NEW:
            raise OrderException("Cannot assign instrument to active order")
        for item in self.items:
            if item.id == item_id:
                if any(existing.id != item.id and existing.instrument_id == instrument_id for existing in self.items):
                    raise OrderException("Instrument already exists in order")
                item.instrument_id = instrument_id
                return
        raise OrderException("Order item not found")

    def remove_item(self, item_id: UUID) -> bool:
        """Remove an item from a new order."""
        if self.status != OrderStatus.NEW:
            raise OrderException("Cannot remove item from active order")
        for index, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[index]
                return True
        return False

    def update_details(self, *, planned_issue_at: datetime | None = None, comment: str | None = None) -> None:
        """Update editable order details."""
        self.planned_issue_at = planned_issue_at
        self.comment = comment

    def register(self) -> None:
        """Register the order."""
        if not self.items:
            raise OrderException("Order must contain items")
        self.status = OrderStatus.REGISTERED
        self.add_event(OrderRegistered(order_id=self.id))
