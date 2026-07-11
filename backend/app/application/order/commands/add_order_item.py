from dataclasses import dataclass
from uuid import UUID

from app.domains.order.entities.order_item import OrderItem
from app.domains.order.entities.order import Order


@dataclass(frozen=True)
class AddOrderItemCommand:
    order: Order
    item_id: UUID
    instrument_id: UUID | None = None


class AddOrderItemHandler:

    def handle(
        self,
        command: AddOrderItemCommand,
    ) -> Order:

        command.order.add_item(
            OrderItem(
                id=command.item_id,
                instrument_id=command.instrument_id,
            )
        )

        return command.order
