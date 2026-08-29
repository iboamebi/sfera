from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.application.order.commands.add_order_items import AddOrderItemsCommand
from app.application.order.services.order_application_service import OrderApplicationService
from app.domains.order.entities.order import Order
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    """Minimal unit of work for application tests."""

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        pass


class FakeOrderRepository(OrderRepository):
    """In-memory order repository for application tests."""

    def __init__(self) -> None:
        self.order: Order | None = None

    def get(self, order_id: UUID) -> Order | None:
        return self.order if self.order and self.order.id == order_id else None

    def list(self) -> list[Order]:
        return [self.order] if self.order else []

    def has_conflicting_order_for_instrument(
        self,
        instrument_id: UUID,
        exclude_order_id: UUID,
    ) -> bool:
        return False

    def delete_item(self, order_id: UUID, item_id: UUID) -> None:
        pass

    def save(self, order: Order) -> None:
        self.order = order


def make_operator() -> User:
    """Create an authorized test operator."""

    return User(
        id=uuid4(),
        username="test-operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )


def test_add_items_creates_requested_quantity_without_instrument_cards():
    repository = FakeOrderRepository()
    service = OrderApplicationService(repository, FakeUnitOfWork())
    order = Order.create(
        id=uuid4(),
        number=OrderNumber("20001"),
        customer_id=uuid4(),
        received_at=datetime.now(UTC),
    )
    repository.save(order)
    instrument_type_id = uuid4()

    result = service.add_items(
        AddOrderItemsCommand(
            order_id=order.id,
            instrument_type_id=instrument_type_id,
            quantity=3,
        ),
        make_operator(),
    )

    assert len(result.items) == 3
    assert all(item.instrument_id is None for item in result.items)
    assert all(
        item.instrument_type_id == instrument_type_id for item in result.items
    )
