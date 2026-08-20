from datetime import UTC, datetime
from uuid import uuid4

from app.api.routers.order import create_order
from app.domains.order.entities.order import Order
from app.domains.order.value_objects.order_number import OrderNumber
from app.schemas.order import OrderRead


def test_create_order_returns_api_contract() -> None:
    customer_id = uuid4()
    order = Order(
        id=uuid4(),
        number=OrderNumber("1001"),
        customer_id=customer_id,
        received_at=datetime.now(UTC),
        planned_issue_at=None,
        issued_at=None,
        comment="Test order",
    )

    class FakeOrderService:
        def create(self, command: object, received_user: object) -> Order:
            return order

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
    )

    response = OrderRead.model_validate(result)

    assert response.id == order.id
    assert response.number == "1001"
    assert response.customer_id == customer_id
    assert response.status.value == "NEW"
    assert response.archived is False
