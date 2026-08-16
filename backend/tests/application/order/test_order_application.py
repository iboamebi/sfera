"""
Tests for Order application service.
"""

from datetime import UTC, datetime
from uuid import uuid4

from app.application.order.commands.add_order_item import (
    AddOrderItemCommand,
)
from app.application.order.commands.create_order import (
    CreateOrderCommand,
)
from app.application.order.commands.register_order import (
    RegisterOrderCommand,
)
from app.application.order.services.order_application_service import (
    OrderApplicationService,
)
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

    def list(self) -> list[Order]:
        return list(self._orders.values())

    def save(self, order: Order) -> None:
        self._orders[order.id] = order


def test_create_register_order_flow():
    repository = FakeOrderRepository()
    service = OrderApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    customer_id = uuid4()
    planned_issue_at = datetime(2026, 8, 20, 15, 30, tzinfo=UTC)
    comment = "Urgent order"

    order = service.create(
        CreateOrderCommand(
            customer_id=customer_id,
            number="10001",
            planned_issue_at=planned_issue_at,
            comment=comment,
        )
    )

    assert order.id is not None
    assert order.number.value == "10001"
    assert order.customer_id == customer_id
    assert order.received_at is not None
    assert order.planned_issue_at == planned_issue_at
    assert order.comment == comment

    service.add_item(
        AddOrderItemCommand(
            order_id=order.id,
        )
    )

    order = service.register(
        RegisterOrderCommand(order.id),
    )

    assert len(order.items) == 1
    assert order.items[0].id is not None
    assert order.status.value == "REGISTERED"
