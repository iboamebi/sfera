from dataclasses import dataclass
from uuid import UUID

from app.domains.order.entities.order import Order
from app.domains.order.value_objects.order_number import OrderNumber


@dataclass(frozen=True)
class CreateOrderCommand:
    order_id: UUID
    customer_id: UUID
    number: str


class CreateOrderHandler:
    def handle(
        self,
        command: CreateOrderCommand,
    ) -> Order:
        return Order(
            id=command.order_id,
            number=OrderNumber(command.number),
            customer_id=command.customer_id,
        )
