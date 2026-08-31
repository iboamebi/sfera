from datetime import UTC, datetime
from uuid import uuid4

from app.api.routers.order import create_order
from app.api.routers.order import get_order
from app.domains.order.entities.order import Order
from app.domains.order.value_objects.order_number import OrderNumber
from app.schemas.order import OrderRead


def test_create_order_returns_api_contract() -> None:
    customer_id = uuid4()
    now = datetime.now(UTC)
    order = Order(
        id=uuid4(),
        number=OrderNumber("1001"),
        customer_id=customer_id,
        received_at=now,
        planned_issue_at=None,
        issued_at=None,
        comment="Test order",
    )

    class FakeOrderService:
        def create(self, command: object, received_user: object) -> Order:
            return order

    class FakeOrderReadService:
        def get(self, requested_id: object) -> OrderRead:
            assert requested_id == order.id
            return OrderRead(
                id=order.id,
                number="1001",
                customer_id=customer_id,
                status="NEW",
                received_at=now,
                created_at=now,
                updated_at=now,
                planned_issue_at=None,
                issued_at=None,
                comment="Test order",
                archived=False,
                items=[],
            )

    result = create_order(
        data=type(
            "OrderCreateData",
            (),
            {
                "number": "1001",
                "customer_id": customer_id,
                "planned_issue_at": None,
                "comment": "Test order",
            },
        )(),
        user=object(),
        service=FakeOrderService(),
        read_service=FakeOrderReadService(),
    )

    assert result.id == order.id
    assert result.number == "1001"
    assert result.customer_id == customer_id
    assert result.status.value == "NEW"
    assert result.archived is False
    assert result.created_at == now
    assert result.updated_at == now


def test_get_order_returns_api_contract() -> None:
    order_id = uuid4()
    now = datetime.now(UTC)

    class FakeOrderReadService:
        def get(self, requested_id: object) -> OrderRead:
            assert requested_id == order_id

            return OrderRead(
                id=order_id,
                number="1001",
                customer_id=uuid4(),
                status="NEW",
                received_at=now,
                created_at=now,
                updated_at=now,
                planned_issue_at=None,
                issued_at=None,
                comment="Test order",
                archived=False,
                items=[],
            )

    result = get_order(
        order_id=order_id,
        service=FakeOrderReadService(),
    )

    assert result.id == order_id
    assert result.number == "1001"
    assert result.archived is False
    assert result.created_at == now
    assert result.updated_at == now
