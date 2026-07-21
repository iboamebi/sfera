from uuid import uuid4

from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.exceptions.order_exception import OrderException
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.order.value_objects.order_status import OrderStatus


def test_order_register():
    order = Order(
        id=uuid4(),
        number=OrderNumber("1001"),
        customer_id=uuid4(),
    )

    order.add_item(OrderItem(id=uuid4()))

    order.register()

    assert order.status == OrderStatus.REGISTERED


def test_empty_order_cannot_register():
    order = Order(
        id=uuid4(),
        number=OrderNumber("1002"),
        customer_id=uuid4(),
    )

    try:
        order.register()
        assert False
    except OrderException:
        assert True
