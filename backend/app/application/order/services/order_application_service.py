"""
Application service for Order.
"""

from uuid import UUID, uuid4

from app.application.order.commands.add_order_item import (
    AddOrderItemCommand,
)
from app.application.order.commands.create_order import (
    CreateOrderCommand,
)
from app.application.order.commands.register_order import (
    RegisterOrderCommand,
)
from app.application.order.exceptions import (
    OrderNotFoundApplicationError,
)
from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.order.value_objects.order_number import OrderNumber
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class OrderApplicationService:
    """Coordinates Order use cases."""

    def __init__(
        self,
        repository: OrderRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = unit_of_work

    def create(
        self,
        command: CreateOrderCommand,
    ) -> Order:
        with self._uow:
            order = Order.create(
                id=uuid4(),
                number=OrderNumber(command.number),
                customer_id=command.customer_id,
            )

            self._repository.save(order)

        return order

    def get(
        self,
        order_id: UUID,
    ) -> Order:
        """Get order."""

        order = self._repository.get(order_id)

        if order is None:
            raise OrderNotFoundApplicationError

        return order

    def add_item(
        self,
        command: AddOrderItemCommand,
    ) -> Order:
        with self._uow:
            order = self.get(command.order_id)

            order.add_item(
                OrderItem(
                    id=uuid4(),
                    instrument_id=command.instrument_id,
                )
            )

            self._repository.save(order)

        return order

    def register(
        self,
        command: RegisterOrderCommand,
    ) -> Order:
        with self._uow:
            order = self.get(command.order_id)

            order.register()

            self._repository.save(order)

        return order
