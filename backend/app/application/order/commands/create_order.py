from dataclasses import dataclass
from uuid import UUID

from app.application.order.services.order_service import OrderService
from app.domains.order.entities.order import Order


@dataclass(frozen=True)
class CreateOrderCommand:
    order_id: UUID
    customer_id: UUID
    number: str


class CreateOrderHandler:
    def __init__(
        self,
        service: OrderService,
    ) -> None:
        self._service = service

    def handle(
        self,
        command: CreateOrderCommand,
    ) -> Order:
        return self._service.create(
            order_id=command.order_id,
            customer_id=command.customer_id,
            number=command.number,
        )
