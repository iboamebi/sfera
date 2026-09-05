"""
Tests for Order application service.
"""

from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.order.commands.add_order_item import AddOrderItemCommand
from app.application.order.commands.create_order import CreateOrderCommand
from app.application.order.commands.register_order import RegisterOrderCommand
from app.application.order.commands.update_order import UpdateOrderCommand
from app.application.order.exceptions import (
    InstrumentAlreadyInActiveOrderApplicationError,
)
from app.application.order.services.order_application_service import (
    OrderApplicationService,
)
from app.domains.customer.entities.customer import Customer
from app.domains.customer.repositories.customer_repository import CustomerRepository
from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.order.value_objects.order_status import (
    CONFLICTING_INSTRUMENT_ORDER_STATUSES,
    OrderStatus,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    """Fake unit of work for application-service tests."""

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


class FakeCustomerRepository(CustomerRepository):
    """Fake customer repository for application-service tests."""

    def __init__(self) -> None:
        self._customers: dict[UUID, Customer] = {}

    def get(
        self,
        customer_id: UUID,
        include_archived: bool = False,
    ) -> Customer | None:
        customer = self._customers.get(customer_id)
        if customer is None or (customer.archived and not include_archived):
            return None
        return customer

    def get_all(self, include_archived: bool = False) -> list[Customer]:
        return [
            customer
            for customer in self._customers.values()
            if include_archived or not customer.archived
        ]

    def save(self, customer: Customer) -> Customer:
        self._customers[customer.id] = customer
        return customer


class FakeOrderRepository(OrderRepository):
    """Fake order repository for application-service tests."""

    def __init__(self) -> None:
        self._orders: dict[UUID, Order] = {}

    def get(self, order_id: UUID) -> Order | None:
        return self._orders.get(order_id)

    def get_by_order_item_id(self, order_item_id: UUID) -> Order | None:
        """Get the order containing an order item."""
        return next(
            (
                order
                for order in self._orders.values()
                if any(item.id == order_item_id for item in order.items)
            ),
            None,
        )

    def list(self) -> list[Order]:
        return list(self._orders.values())

    def has_conflicting_order_for_instrument(
        self,
        instrument_id: UUID,
        exclude_order_id: UUID,
    ) -> bool:
        return any(
            order.id != exclude_order_id
            and order.status in CONFLICTING_INSTRUMENT_ORDER_STATUSES
            and any(
                item.instrument_id == instrument_id
                for item in order.items
            )
            for order in self._orders.values()
        )

    def save(self, order: Order) -> None:
        self._orders[order.id] = order


def make_operator() -> User:
    """Create an operator user for tests."""
    return User(
        id=uuid4(),
        username="test-operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )


def make_customer(customer_id: UUID) -> Customer:
    """Create a customer with a deterministic organization context."""
    return Customer(
        id=customer_id,
        organization_id=uuid4(),
        name="Test customer",
    )


def make_service() -> tuple[
    OrderApplicationService,
    FakeOrderRepository,
    FakeCustomerRepository,
    FakeUnitOfWork,
]:
    """Create an order service with all required fake dependencies."""
    repository = FakeOrderRepository()
    customer_repository = FakeCustomerRepository()
    uow = FakeUnitOfWork()
    service = OrderApplicationService(
        repository,
        customer_repository,
        uow,
    )
    return service, repository, customer_repository, uow


def create_order(
    service: OrderApplicationService,
    customer_repository: FakeCustomerRepository,
    number: str,
) -> Order:
    """Create an order with a registered customer fixture."""
    customer_id = uuid4()
    customer_repository.save(make_customer(customer_id))
    return service.create(
        CreateOrderCommand(
            customer_id=customer_id,
            number=number,
        ),
        make_operator(),
    )


def test_create_register_order_flow():
    service, _, customer_repository, uow = make_service()
    customer_id = uuid4()
    customer_repository.save(make_customer(customer_id))

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
    assert order.organization_id == customer_repository.get(customer_id).organization_id
    assert order.received_at is not None
    assert order.planned_issue_at == planned_issue_at
    assert order.comment == comment

    service.add_item(
        AddOrderItemCommand(order_id=order.id),
        make_operator(),
    )

    order = service.register(
        RegisterOrderCommand(order.id),
        make_operator(),
    )

    assert len(order.items) == 1
    assert order.items[0].id is not None
    assert order.status.value == "REGISTERED"
    assert len(uow.registered_operation_ids) == 1
    assert isinstance(uow.registered_operation_ids[0], UUID)


def test_create_order_rejects_unauthorized_user():
    service, repository, _, _ = make_service()

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
    service, repository, customer_repository, _ = make_service()
    customer_id = uuid4()
    customer_repository.save(make_customer(customer_id))
    order = service.create(
        CreateOrderCommand(customer_id=customer_id, number="10004"),
        make_operator(),
    )

    user = User(
        id=uuid4(),
        username="test-user",
        password_hash="hash",
        role=UserRole.WAREHOUSE,
    )

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.register(RegisterOrderCommand(order.id), user)

    assert order.status.value == "NEW"
    assert repository.get(order.id) is order


def test_add_order_item_rejects_unauthorized_user():
    service, repository, customer_repository, _ = make_service()
    customer_id = uuid4()
    customer_repository.save(make_customer(customer_id))
    order = service.create(
        CreateOrderCommand(customer_id=customer_id, number="10005"),
        make_operator(),
    )

    user = User(
        id=uuid4(),
        username="test-user",
        password_hash="hash",
        role=UserRole.WAREHOUSE,
    )

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.add_item(AddOrderItemCommand(order_id=order.id), user)

    assert order.items == []
    assert repository.get(order.id) is order


def test_update_order_rejects_unauthorized_user():
    service, repository, customer_repository, _ = make_service()
    customer_id = uuid4()
    customer_repository.save(make_customer(customer_id))
    order = service.create(
        CreateOrderCommand(customer_id=customer_id, number="10006"),
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
    service, repository, customer_repository, _ = make_service()
    customer_id = uuid4()
    customer_repository.save(make_customer(customer_id))
    order = service.create(
        CreateOrderCommand(customer_id=customer_id, number="10002"),
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


def test_add_order_item_rejects_instrument_in_another_active_order():
    service, repository, customer_repository, _ = make_service()
    instrument_id = uuid4()

    existing_order = create_order(service, customer_repository, "10007")
    existing_order.add_item(
        OrderItem(id=uuid4(), instrument_id=instrument_id)
    )
    existing_order.status = OrderStatus.REGISTERED
    repository.save(existing_order)

    order = create_order(service, customer_repository, "10008")

    with pytest.raises(InstrumentAlreadyInActiveOrderApplicationError):
        service.add_item(
            AddOrderItemCommand(
                order_id=order.id,
                instrument_id=instrument_id,
            ),
            make_operator(),
        )


def test_add_order_item_creates_separate_items_for_group_quantity():
    service, _, customer_repository, _ = make_service()
    order = create_order(service, customer_repository, "10011")
    instrument_type_id = uuid4()

    service.add_item(
        AddOrderItemCommand(
            order_id=order.id,
            instrument_type_id=instrument_type_id,
            quantity=3,
        ),
        make_operator(),
    )

    assert len(order.items) == 3
    assert all(item.quantity == 1 for item in order.items)
    assert all(
        item.instrument_type_id == instrument_type_id
        for item in order.items
    )
    assert all(item.instrument_id is None for item in order.items)
    assert len({item.id for item in order.items}) == 3


def test_add_order_item_allows_instrument_after_order_completed():
    service, repository, customer_repository, _ = make_service()
    instrument_id = uuid4()

    completed_order = create_order(service, customer_repository, "10009")
    completed_order.add_item(
        OrderItem(id=uuid4(), instrument_id=instrument_id)
    )
    completed_order.status = OrderStatus.COMPLETED
    repository.save(completed_order)

    order = create_order(service, customer_repository, "10010")

    service.add_item(
        AddOrderItemCommand(
            order_id=order.id,
            instrument_id=instrument_id,
        ),
        make_operator(),
    )

    assert len(order.items) == 1
    assert order.items[0].instrument_id == instrument_id
