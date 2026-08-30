"""
SQLAlchemy implementation of OrderReadRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.domains.order.read_models.order_read_models import (
    OrderItemReadData,
    OrderReadData,
)
from app.domains.order.repositories.order_read_repository import OrderReadRepository
from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.models.instrument import Instrument
from app.models.order import Order
from app.models.order_item import OrderItem


class OrderReadRepositorySQLAlchemy(OrderReadRepository):
    """SQLAlchemy read repository for orders."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, order_id: UUID) -> OrderReadData | None:
        order = (
            self.session.query(Order)
            .options(
                joinedload(Order.order_items)
                .joinedload(OrderItem.instrument)
                .joinedload(Instrument.instrument_type),
                joinedload(Order.order_items).joinedload(OrderItem.instrument_type),
            )
            .filter(Order.id == order_id)
            .first()
        )

        if order is None:
            return None

        return OrderReadData(
            id=order.id,
            number=order.number,
            customer_id=order.customer_id,
            status=order.status,
            received_at=order.received_at,
            planned_issue_at=order.planned_issue_at,
            issued_at=order.issued_at,
            comment=order.comment,
            archived=order.archived,
            items=[
                OrderItemReadData(
                    id=item.id,
                    instrument_id=item.instrument_id,
                    instrument_type_id=item.instrument_type_id,
                    instrument_type_name=(
                        item.instrument.instrument_type.name
                        if item.instrument
                        and item.instrument.instrument_type
                        else item.instrument_type.name
                        if item.instrument_type
                        else None
                    ),
                    instrument_type_model=(
                        item.instrument.instrument_type.model
                        if item.instrument
                        and item.instrument.instrument_type
                        else item.instrument_type.model
                        if item.instrument_type
                        else None
                    ),
                    instrument_type_measurement_type=(
                        item.instrument.instrument_type.measurement_type
                        if item.instrument
                        and item.instrument.instrument_type
                        else item.instrument_type.measurement_type
                        if item.instrument_type
                        else None
                    ),
                    serial_number=item.instrument.serial_number if item.instrument else None,
                    modification=item.instrument.modification if item.instrument else None,
                    comment=item.customer_comment,
                    requested_operations={
                        OrderItemOperation(operation)
                        for operation in item.requested_operations
                    },
                )
                for item in order.order_items
            ],
        )