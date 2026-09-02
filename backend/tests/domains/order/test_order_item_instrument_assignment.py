"""Tests for assigning concrete instruments to order items."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.exceptions.order_exception import OrderException
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.order.value_objects.order_status import OrderStatus


def make_order() -> Order:
    """Create a new order for domain tests."""
    return Order.create(
        id=uuid4(),
        number=OrderNumber("10020"),
        customer_id=uuid4(),
        received_at=datetime.now(UTC),
    )


def test_assign_instrument_to_group_order_item():
    order = make_order()
    item = OrderItem(
        id=uuid4(),
        instrument_type_id=uuid4(),
        quantity=1,
    )
    instrument_id = uuid4()
    order.add_item(item)

    order.assign_instrument(item.id, instrument_id)

    assert item.instrument_id == instrument_id


def test_assign_instrument_rejects_duplicate_instrument_in_order():
    order = make_order()
    instrument_id = uuid4()
    first_item = OrderItem(id=uuid4(), instrument_id=instrument_id, quantity=1)
    second_item = OrderItem(id=uuid4(), quantity=1)
    order.add_item(first_item)
    order.add_item(second_item)

    with pytest.raises(OrderException, match="Instrument already exists in order"):
        order.assign_instrument(second_item.id, instrument_id)

    assert second_item.instrument_id is None


def test_assign_instrument_rejects_active_order():
    order = make_order()
    item = OrderItem(id=uuid4(), quantity=1)
    order.add_item(item)
    order.status = OrderStatus.REGISTERED

    with pytest.raises(
        OrderException,
        match="Cannot assign instrument in active order",
    ):
        order.assign_instrument(item.id, uuid4())


def test_assign_instrument_rejects_unknown_item():
    order = make_order()

    with pytest.raises(OrderException, match="Order item not found"):
        order.assign_instrument(uuid4(), uuid4())
