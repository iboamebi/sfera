"""
Order aggregate root.
"""

from dataclasses import dataclass, field
from uuid import UUID

from app.domains.order.entities.order_item import OrderItem
from app.domains.order.exceptions.order_exception import OrderException
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.order.value_objects.order_status import OrderStatus
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False, kw_only=True)
class Order(AggregateRoot):
    """Order aggregate."""

    number: OrderNumber
    customer_id: UUID
    status: OrderStatus = OrderStatus.NEW

    items: list[OrderItem] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        id: UUID,
        number: OrderNumber,
        customer_id: UUID,
    ) -> "Order":
        """Create a new Order aggregate."""

        return cls(
            id=id,
            number=number,
            customer_id=customer_id,
        )

    def add_item(self, item: OrderItem) -> None:
        """Add item to a new order."""

        if self.status != OrderStatus.NEW:
            raise OrderException("Cannot add item to active order")

        self.items.append(item)

    def register(self) -> None:
        """Register the order."""

        if not self.items:
            raise OrderException("Order must contain items")

        self.status = OrderStatus.REGISTERED
