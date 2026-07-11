from uuid import uuid4

from app.application.order.commands.create_order import (
    CreateOrderCommand,
    CreateOrderHandler,
)

from app.application.order.commands.add_order_item import (
    AddOrderItemCommand,
    AddOrderItemHandler,
)

from app.application.order.commands.register_order import (
    RegisterOrderCommand,
    RegisterOrderHandler,
)


def test_create_register_order_flow():
    order_id = uuid4()
    customer_id = uuid4()

    order = CreateOrderHandler().handle(
        CreateOrderCommand(
            order_id=order_id,
            customer_id=customer_id,
            number="10001",
        )
    )

    AddOrderItemHandler().handle(
        AddOrderItemCommand(
            order=order,
            item_id=uuid4(),
        )
    )

    RegisterOrderHandler().handle(
        RegisterOrderCommand(order)
    )

    assert order.number.value == "10001"
    assert len(order.items) == 1
    assert order.status.value == "REGISTERED"
