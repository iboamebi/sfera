from uuid import uuid4

from app.application.order.commands.add_order_item import (
    AddOrderItemCommand,
    AddOrderItemHandler,
)
from app.application.order.commands.create_order import (
    CreateOrderCommand,
    CreateOrderHandler,
)
from app.application.order.commands.register_order import (
    RegisterOrderCommand,
    RegisterOrderHandler,
)
from app.application.order.services.order_service import OrderService
from app.domains.order.entities.order import Order
from app.domains.order.repositories.order_repository import OrderRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class FakeOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: dict = {}

    def get(self, order_id):
        return self._orders.get(order_id)

    def save(self, order: Order) -> None:
        self._orders[order.id] = order


def test_create_register_order_flow():
    repository = FakeOrderRepository()
    service = OrderService(
        repository,
        FakeUnitOfWork(),
    )

    order_id = uuid4()
    customer_id = uuid4()

    order = CreateOrderHandler(service).handle(
        CreateOrderCommand(
            order_id=order_id,
            customer_id=customer_id,
            number="10001",
        )
    )

    AddOrderItemHandler(service).handle(
        AddOrderItemCommand(
            order_id=order.id,
            item_id=uuid4(),
        )
    )

    order = RegisterOrderHandler(service).handle(
        RegisterOrderCommand(order.id),
    )

    assert order.number.value == "10001"
    assert len(order.items) == 1
    assert order.status.value == "REGISTERED"
