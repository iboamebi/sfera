"""Tests for Order mapper."""

from datetime import UTC, datetime
from uuid import uuid4

from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.infrastructure.mappers.order_mapper import OrderMapper
from app.models.order import Order as OrderModel
from app.models.order import OrderStatus
from app.models.order_item import OrderItem as OrderItemModel


def test_order_mapper_to_domain_preserves_order_items() -> None:
    order_id = uuid4()
    customer_id = uuid4()
    item_id = uuid4()
    instrument_id = uuid4()
    received_at = datetime.now(UTC)

    item_model = OrderItemModel(
        id=item_id,
        order_id=order_id,
        instrument_id=instrument_id,
        line_number=1,
        customer_inventory_number="INV-001",
        customer_comment="Customer comment",
        requested_operations=[OrderItemOperation.VERIFICATION.value],
    )
    order_model = OrderModel(
        id=order_id,
        number="ORD-001",
        customer_id=customer_id,
        status=OrderStatus.NEW,
        received_at=received_at,
        order_items=[item_model],
    )

    entity = OrderMapper().to_domain(order_model)

    assert len(entity.items) == 1
    assert entity.items[0].id == item_id
    assert entity.items[0].instrument_id == instrument_id
    assert entity.items[0].customer_inventory_number == "INV-001"
    assert entity.items[0].comment == "Customer comment"
    assert entity.items[0].requested_operations == {OrderItemOperation.VERIFICATION}
