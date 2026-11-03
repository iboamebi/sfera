"""
Tests for mapping order read models to API schemas.
"""

from datetime import UTC, datetime
from uuid import uuid4

from app.application.order.queries.order_read_mapper import OrderReadMapper
from app.domains.order.read_models.order_read_models import (
    OrderItemReadData,
    OrderReadData,
)
from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.domains.order.value_objects.order_status import OrderStatus


def test_to_schema_includes_item_verification_ids() -> None:
    now = datetime.now(UTC)
    verification_id = uuid4()
    item = OrderItemReadData(
        id=uuid4(),
        instrument_id=uuid4(),
        instrument_type_id=None,
        instrument_name="Thermometer",
        instrument_type_name=None,
        serial_number="SN-100",
        modification=None,
        comment=None,
        requested_operations={OrderItemOperation.VERIFICATION},
        verification_ids=[verification_id],
    )
    order = OrderReadData(
        id=uuid4(),
        number="1001",
        customer_id=uuid4(),
        customer_name="Test customer",
        status=OrderStatus.NEW,
        received_at=now,
        created_at=now,
        updated_at=now,
        planned_issue_at=None,
        issued_at=None,
        comment=None,
        archived=False,
        items=[item],
    )

    result = OrderReadMapper().to_schema(order)

    assert result.items[0].verification_ids == [verification_id]
