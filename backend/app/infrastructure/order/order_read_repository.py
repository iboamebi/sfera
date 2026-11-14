"""
SQLAlchemy implementation of OrderReadRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.domains.order.read_models.order_read_models import (
    OrderItemReadData,
    OrderItemVerificationReadData,
    OrderReadData,
)
from app.domains.order.repositories.order_read_repository import OrderReadRepository
from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.domains.verification.value_objects.verification_type import VerificationType
from app.models.instrument import Instrument
from app.models.order import Order
from app.models.order_item import OrderItem


class OrderReadRepositorySQLAlchemy(OrderReadRepository):
    """SQLAlchemy read repository for orders."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_read_model(self, order: Order) -> OrderReadData:
        return OrderReadData(
            id=order.id,
            number=order.number,
            customer_id=order.customer_id,
            customer_name=order.customer.name,
            status=order.status,
            received_at=order.received_at,
            created_at=order.created_at,
            updated_at=order.updated_at,
            planned_issue_at=order.planned_issue_at,
            issued_at=order.issued_at,
            comment=order.comment,
            archived=order.archived,
            items=[
                OrderItemReadData(
                    id=item.id,
                    instrument_id=item.instrument_id,
                    instrument_type_id=item.instrument_type_id,
                    instrument_name=item.instrument.name if item.instrument else None,
                    instrument_type_name=(
                        item.instrument.instrument_type.name
                        if item.instrument and item.instrument.instrument_type
                        else item.instrument_type.name
                        if item.instrument_type
                        else None
                    ),
                    serial_number=item.instrument.serial_number
                    if item.instrument
                    else None,
                    modification=item.instrument.modification
                    if item.instrument
                    else None,
                    comment=item.customer_comment,
                    requested_operations={
                        OrderItemOperation(operation)
                        for operation in item.requested_operations
                    },
                    verification_ids=[
                        verification.id
                        for verification in sorted(
                            item.verifications,
                            key=lambda value: (value.created_at, value.id),
                        )
                    ],
                    verifications=[
                        OrderItemVerificationReadData(
                            id=verification.id,
                            created_at=verification.created_at,
                            verification_date=verification.verification_date,
                            verification_type=VerificationType(
                                verification.verification_type
                            ),
                            status=VerificationStatus(verification.status),
                            result=(
                                VerificationResult(verification.result)
                                if verification.result is not None
                                else None
                            ),
                            valid_until=verification.valid_until,
                            archived=verification.archived,
                        )
                        for verification in sorted(
                            item.verifications,
                            key=lambda value: (value.created_at, value.id),
                        )
                    ],
                )
                for item in order.order_items
            ],
        )

    def _query(self):
        return self.session.query(Order).options(
            joinedload(Order.customer),
            joinedload(Order.order_items)
            .joinedload(OrderItem.instrument)
            .joinedload(Instrument.instrument_type),
            joinedload(Order.order_items).joinedload(OrderItem.instrument_type),
            joinedload(Order.order_items).selectinload(OrderItem.verifications),
        )

    def get(self, order_id: UUID) -> OrderReadData | None:
        order = self._query().filter(Order.id == order_id).first()
        if order is None:
            return None
        return self._to_read_model(order)

    def list(self) -> list[OrderReadData]:
        """List orders as read models."""
        return [self._to_read_model(order) for order in self._query().all()]
