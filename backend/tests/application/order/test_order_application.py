"""
Tests for Order application service.
"""

from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.order.commands.add_order_item import (
    AddOrderItemCommand,
)
from app.application.order.commands.create_order import (
    CreateOrderCommand,
)
from app.application.order.commands.register_order import (
    RegisterOrderCommand,
)
from app.application.order.commands.remove_order_item import (
    RemoveOrderItemCommand,
)
from app.application.order.commands.update_order import (
    UpdateOrderCommand,
)
from app.application.order.services.order_application_service import (
    OrderApplicationService,
)
from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.exceptions.order_exception import OrderException
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.registered_operation_ids: list[UUID | None] = []

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        self.registered_operation_ids.append(operation_id)


class FakeOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: dict = {}

    def get(self, order_id):
        return self._orders.get(order_id)

    def list(self) -> list[Order]:
        return list(self._orders.values())

    def save(self, order: Order) -> None:
        self._orders[order.id] = order


def make_operator() -> User:
    return User(
        id=uuid4(),
        username="test-operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )


def test_create_register_order_flow():
    repository = FakeOrderRepository()
    uow = FakeUnitOfWork()
    service = OrderApplicationService(
        repository,
        uow,
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
        ),
        make_operator(),
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
        ),
        make_operator(),
    )

    user = make_operator()

    order = service.register(
        RegisterOrderCommand(order.id),
        user,
    )

    assert len(order.items) == 1
    assert order.items[0].id is not None
    assert order.status.value == "REGISTERED"
    assert len(uow.registered_operation_ids) == 1
    assert isinstance(uow.registered_operation_ids[0], UUID)


def test_add_order_item_rejects_duplicate_instrument():
    repository = FakeOrderRepository()
    service = OrderApplicationService(repository, FakeUnitOfWork())
    order = service.create(
        CreateOrderCommand(customer_id=uuid4(), number="10007"),
        make_operator(),
    )
    instrument_id = uuid4()

    service.add_item(
        AddOrderItemCommand(order_id=order.id, instrument_id=instrument_id),
        make_operator(),
    )

    with pytest.raises(OrderException, match="already added"):
        service.add_item(
            AddOrderItemCommand(order_id=order.id, instrument_id=instrument_id),
            make_operator(),
        )

    assert len(order.items) == 1


def test_remove_order_item():
    repository = FakeOrderRepository()
    service = OrderApplicationService(repository, FakeUnitOfWork())
    order = service.create(
        CreateOrderCommand(customer_id=uuid4(), number="10008"),
        make_operator(),
    )
    service.add_item(
        AddOrderItemCommand(order_id=order.id, instrument_id=uuid4()),
        make_operator(),
    )
    item_id = order.items[0].id

    updated_order = service.remove_item(
        RemoveOrderItemCommand(order_id=order.id, item_id=item_id),
        make_operator(),
    )

    assert updated_order.items == []
    assert repository.get(order.id) is updated_order


def test_remove_order_item_rejects_missing_item():
    repository = FakeOrderRepository()
    service = OrderApplicationService(repository, FakeUnitOfWork())
    order = service.create(
        CreateOrderCommand(customer_id=uuid4(), number="10009"),
        make_operator(),
    )

    with pytest.raises(OrderException, match="Order item not found"):
        service.remove_item(
            RemoveOrderItemCommand(order_id=order.id, item_id=uuid4()),
            make_operator(),
        )


def test_create_order_rejects_unauthorized_user():
    repository = FakeOrderRepository()
    service = OrderApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.create(
            CreateOrderCommand(
                customer_id=uuid4(),
                number="10003",
            ),
            User(
                id=uuid4(),
                username="test-user",
                password_hash="hash",
                role=UserRole.WAREHOUSE,
            ),
        )

    assert repository.list() == []


def test_register_order_rejects_unauthorized_user():
    repository = FakeOrderRepository()
    service = OrderApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    order = service.create(
        CreateOrderCommand(
            customer_id=uuid4(),
            number="10004",
        ),
        make_operator(),
    )

    user = User(
        id=uuid4(),
        username="test-user",
        password_hash="hash",
        role=UserRole.WAREHOUSE,
    )

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.register(
            RegisterOrderCommand(order.id),
            user,
        )

    assert order.status.value == "NEW"
    assert repository.get(order.id) is order


def test_add_order_item_rejects_unauthorized_user():
    repository = FakeOrderRepository()
    service = OrderApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    order = service.create(
        CreateOrderCommand(
            customer_id=uuid4(),
            number="10005",
        ),
        make_operator(),
    )

    user = User(
        id=uuid4(),
        username="test-user",
        password_hash="hash",
        role=UserRole.WAREHOUSE,
    )

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.add_item(
            AddOrderItemCommand(
                order_id=order.id,
            ),
            user,
        )

    assert order.items == []
    assert repository.get(order.id) is order


def test_update_order_rejects_unauthorized_user():
    repository = FakeOrderRepository()
    service = OrderApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    order = service.create(
        CreateOrderCommand(
            customer_id=uuid4(),
            number="10006",
        ),
        make_operator(),
    )

    user = User(
        id=uuid4(),
        username="test-user",
        password_hash="hash",
        role=UserRole.WAREHOUSE,
    )

    planned_issue_at = datetime(2026, 8, 21, 10, 0, tzinfo=UTC)

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.update(
            UpdateOrderCommand(
                order_id=order.id,
                planned_issue_at=planned_issue_at,
                comment="Unauthorized update",
            ),
            user,
        )

    assert order.planned_issue_at is None
    assert order.comment is None
    assert repository.get(order.id) is order


def test_update_order_details():
    repository = FakeOrderRepository()
    service = OrderApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    order = service.create(
        CreateOrderCommand(
            customer_id=uuid4(),
            number="10002",
        ),
        make_operator(),
    )

    planned_issue_at = datetime(2026, 8, 21, 10, 0, tzinfo=UTC)
    comment = "Updated order"

    updated_order = service.update(
        UpdateOrderCommand(
            order_id=order.id,
            planned_issue_at=planned_issue_at,
            comment=comment,
        ),
        make_operator(),
    )

    assert updated_order.id == order.id
    assert updated_order.planned_issue_at == planned_issue_at
    assert updated_order.comment == comment
    assert repository.get(order.id) is updated_order
