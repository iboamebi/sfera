from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.exceptions.order_exception import OrderException
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.order.value_objects.order_status import OrderStatus


def create_order(
    number: str,
    planned_issue_at: datetime | None = None,
    comment: str | None = None,
) -> Order:
    return Order(
        id=uuid4(),
        number=OrderNumber(number),
        customer_id=uuid4(),
        received_at=datetime.now(UTC),
        planned_issue_at=planned_issue_at,
        comment=comment,
    )


def test_order_create_with_planned_issue_at_and_comment():
    planned_issue_at = datetime(2026, 8, 20, 15, 30, tzinfo=UTC)
    comment = "Urgent order"

    order = create_order(
        "1001",
        planned_issue_at=planned_issue_at,
        comment=comment,
    )

    assert order.planned_issue_at == planned_issue_at
    assert order.comment == comment


def test_order_register():
    order = create_order("1002")

    order.add_item(
        OrderItem(
            id=uuid4(),
        )
    )

    order.register()

    assert order.status == OrderStatus.REGISTERED


def test_empty_order_cannot_register():
    order = create_order("1003")

    try:
        order.register()
        raise AssertionError()
    except OrderException:
        assert True


def test_order_rejects_duplicate_instrument():
    order = create_order("1004")
    instrument_id = uuid4()

    order.add_item(
        OrderItem(
            id=uuid4(),
            instrument_id=instrument_id,
        )
    )

    with pytest.raises(
        OrderException,
        match="Instrument already exists in order",
    ):
        order.add_item(
            OrderItem(
                id=uuid4(),
                instrument_id=instrument_id,
            )
        )


def test_order_removes_item():
    order = create_order("1005")
    item = OrderItem(id=uuid4(), instrument_id=uuid4())
    order.add_item(item)

    assert order.remove_item(item.id) is True
    assert order.items == []


def test_order_cannot_remove_item_from_registered_order():
    order = create_order("1006")
    item = OrderItem(id=uuid4())
    order.add_item(item)
    order.register()

    with pytest.raises(
        OrderException,
        match="Cannot remove item from active order",
    ):
        order.remove_item(item.id)
