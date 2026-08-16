from datetime import UTC, datetime
from uuid import uuid4

from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.exceptions.order_exception import OrderException
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.order.value_objects.order_status import OrderStatus


def create_order(
    number: str,
) -> Order:
    return Order(
        id=uuid4(),
        number=OrderNumber(number),
        customer_id=uuid4(),
        received_at=datetime.now(UTC),
    )


def test_order_register():
    order = create_order("1001")

    order.add_item(
        OrderItem(
            id=uuid4(),
        )
    )

    order.register()

    assert order.status == OrderStatus.REGISTERED


def test_empty_order_cannot_register():
    order = create_order("1002")

    try:
        order.register()
        raise AssertionError()
    except OrderException:
        assert True
