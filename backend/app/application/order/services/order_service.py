"""
Application service for Order.
"""

from uuid import UUID

from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.order.value_objects.order_number import OrderNumber
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class OrderService:
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
        order_id: UUID,
        customer_id: UUID,
        number: str,
    ) -> Order:
        with self._uow:
            order = Order(
                id=order_id,
                number=OrderNumber(number),
                customer_id=customer_id,
            )

            self._repository.save(order)

        return order

    def get(
        self,
        order_id: UUID,
    ) -> Order:
        order = self._repository.get(order_id)

        if order is None:
            raise ValueError("Order not found")

        return order

    def add_item(
        self,
        order_id: UUID,
        item_id: UUID,
        instrument_id: UUID | None = None,
    ) -> Order:
        with self._uow:
            order = self.get(order_id)

            order.add_item(
                OrderItem(
                    id=item_id,
                    instrument_id=instrument_id,
                )
            )

            self._repository.save(order)

        return order

    def register(
        self,
        order_id: UUID,
    ) -> Order:
        with self._uow:
            order = self.get(order_id)

            order.register()

            self._repository.save(order)

        return order
