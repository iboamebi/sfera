from dataclasses import dataclass
from uuid import UUID

from app.application.order.services.order_service import OrderService
from app.domains.order.entities.order import Order


@dataclass(frozen=True)
class RegisterOrderCommand:
    order_id: UUID


class RegisterOrderHandler:
    def __init__(
        self,
        service: OrderService,
    ) -> None:
        self._service = service

    def handle(
        self,
        command: RegisterOrderCommand,
    ) -> Order:
        return self._service.register(
            command.order_id,
        )
