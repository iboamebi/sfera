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


def test_order_start_work_changes_status_from_registered():
    order = create_order("1003")
    order.add_item(OrderItem(id=uuid4()))
    order.register()

    order.start_work()

    assert order.status == OrderStatus.IN_WORK


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


def test_order_item_quantity_defaults_to_one():
    item = OrderItem(id=uuid4())

    assert item.quantity == 1


def test_order_item_accepts_positive_quantity():
    item = OrderItem(id=uuid4(), quantity=5)

    assert item.quantity == 5


@pytest.mark.parametrize("quantity", [0, -1])
def test_order_item_rejects_non_positive_quantity(quantity: int):
    with pytest.raises(
        OrderException,
        match="Order item quantity must be at least one",
    ):
        OrderItem(id=uuid4(), quantity=quantity)


def test_registered_order_allows_item_changes():
    order = create_order("1005")
    item = OrderItem(id=uuid4())
    order.add_item(item)
    order.register()

    order.update_item(item.id, set())
    order.add_item(OrderItem(id=uuid4()))
    order.remove_item(item.id)

    assert len(order.items) == 1


@pytest.mark.parametrize(
    "status",
    [
        OrderStatus.IN_WORK,
        OrderStatus.WAITING,
        OrderStatus.COMPLETED,
        OrderStatus.ISSUED,
        OrderStatus.CLOSED,
        OrderStatus.CANCELLED,
    ],
)
def test_order_rejects_item_changes_after_work_started(status):
    order = create_order("1006")
    item = OrderItem(id=uuid4())
    order.add_item(item)
    order.status = status

    with pytest.raises(
        OrderException,
        match="Cannot modify items after order work has started",
    ):
        order.add_item(OrderItem(id=uuid4()))

    with pytest.raises(
        OrderException,
        match="Cannot modify items after order work has started",
    ):
        order.update_item(item.id, set())

    with pytest.raises(
        OrderException,
        match="Cannot modify items after order work has started",
    ):
        order.remove_item(item.id)
