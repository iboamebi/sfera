"""Tests for Order mapper."""

from datetime import UTC, date, datetime
from uuid import uuid4

from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.infrastructure.mappers.order_mapper import OrderMapper
from app.models.order import Order as OrderModel
from app.models.order import OrderStatus
from app.models.order_item import OrderItem as OrderItemModel
from app.models.verification import (
    Verification as VerificationModel,
)
from app.models.verification import (
    VerificationStatus,
    VerificationType,
)


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
        quantity=1,
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


def test_order_mapper_to_model_preserves_verifications_when_updating_order() -> None:
    order_id = uuid4()
    customer_id = uuid4()
    item_id = uuid4()
    verification_id = uuid4()
    received_at = datetime.now(UTC)
    item_model = OrderItemModel(
        id=item_id,
        order_id=order_id,
        instrument_id=uuid4(),
        line_number=1,
        quantity=1,
        requested_operations=[OrderItemOperation.VERIFICATION.value],
    )
    verification_model = VerificationModel(
        id=verification_id,
        order_item_id=item_id,
        instrument_id=item_model.instrument_id,
        verification_date=date.today(),
        verification_type=VerificationType.PRIMARY,
        status=VerificationStatus.CREATED,
    )
    item_model.verifications.append(verification_model)
    order_model = OrderModel(
        id=order_id,
        number="ORD-002",
        customer_id=customer_id,
        status=OrderStatus.REGISTERED,
        received_at=received_at,
        order_items=[item_model],
    )

    entity = OrderMapper().to_domain(order_model)
    entity.start_work()
    OrderMapper().to_model(entity, order_model)

    assert order_model.order_items == [item_model]
    assert item_model.verifications == [verification_model]
    assert verification_model.order_item is item_model
