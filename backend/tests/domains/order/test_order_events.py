from uuid import uuid4

from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.events.order_registered import OrderRegistered
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.order.value_objects.order_status import OrderStatus


def test_register_emits_order_registered_event():
    order = Order.create(
        id=uuid4(),
        number=OrderNumber("ORD-001"),
        customer_id=uuid4(),
        received_at=None,
    )

    order.items.append(
        OrderItem(
            id=uuid4(),
        )
    )

    order.register()

    events = order.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], OrderRegistered)
    assert events[0].order_id == order.id
    assert order.status == OrderStatus.REGISTERED
