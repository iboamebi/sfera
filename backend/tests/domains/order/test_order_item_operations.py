from uuid import uuid4

from app.domains.order.entities.order_item import OrderItem
from app.domains.order.value_objects.order_item_operation import OrderItemOperation


def test_order_item_keeps_requested_operations_as_a_set() -> None:
    """An order item may contain multiple requested operations."""
    item = OrderItem(
        id=uuid4(),
        instrument_id=uuid4(),
        requested_operations={
            OrderItemOperation.VERIFICATION,
            OrderItemOperation.REPAIR,
        },
    )

    assert item.requested_operations == {
        OrderItemOperation.VERIFICATION,
        OrderItemOperation.REPAIR,
    }


def test_order_item_does_not_require_verification() -> None:
    """Verification is a UI default, not a domain invariant."""
    item = OrderItem(
        id=uuid4(),
        instrument_id=uuid4(),
        requested_operations={OrderItemOperation.REPAIR},
    )

    assert item.requested_operations == {OrderItemOperation.REPAIR}
