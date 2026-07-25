from dataclasses import dataclass
from uuid import UUID

from app.application.order.services.order_service import OrderService
from app.domains.order.entities.order import Order


@dataclass(frozen=True)
class AddOrderItemCommand:
    order_id: UUID
    item_id: UUID
    instrument_id: UUID | None = None


class AddOrderItemHandler:
    def __init__(
        self,
        service: OrderService,
    ) -> None:
        self._service = service

    def handle(
        self,
        command: AddOrderItemCommand,
    ) -> Order:
        return self._service.add_item(
            order_id=command.order_id,
            item_id=command.item_id,
            instrument_id=command.instrument_id,
        )
