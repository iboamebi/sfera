"""
SQLAlchemy implementation of the Verification read repository.
"""

from sqlalchemy.orm import Session, joinedload

from app.domains.verification.read_models.verification_read_models import (
    VerificationListReadData,
)
from app.domains.verification.repositories.verification_read_repository import (
    VerificationReadRepository,
)
from app.models.instrument import Instrument
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.verification import Verification as VerificationModel


class VerificationReadRepositorySQLAlchemy(VerificationReadRepository):
    """SQLAlchemy read repository for the general Verification list."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[VerificationListReadData]:
        models = (
            self.session.query(VerificationModel)
            .join(VerificationModel.order_item)
            .join(OrderItem.order)
            .join(Order.customer)
            .options(
                joinedload(VerificationModel.order_item)
                .joinedload(OrderItem.order)
                .joinedload(Order.customer),
                joinedload(VerificationModel.order_item)
                .joinedload(OrderItem.instrument)
                .joinedload(Instrument.instrument_type),
                joinedload(VerificationModel.order_item).joinedload(
                    OrderItem.instrument_type,
                ),
            )
            .order_by(
                VerificationModel.created_at.desc(),
                VerificationModel.id.desc(),
            )
            .all()
        )

        return [
            VerificationListReadData(
                id=verification.id,
                order_item_id=verification.order_item_id,
                order_id=verification.order_item.order.id,
                order_number=verification.order_item.order.number,
                customer_id=verification.order_item.order.customer_id,
                customer_name=verification.order_item.order.customer.name,
                instrument_id=verification.instrument_id,
                instrument_name=(
                    verification.order_item.instrument.name
                    if verification.order_item.instrument
                    else None
                ),
                instrument_type_id=(
                    verification.order_item.instrument.instrument_type_id
                    if verification.order_item.instrument
                    else verification.order_item.instrument_type_id
                ),
                instrument_type_name=(
                    verification.order_item.instrument.instrument_type.name
                    if (
                        verification.order_item.instrument
                        and verification.order_item.instrument.instrument_type
                    )
                    else (
                        verification.order_item.instrument_type.name
                        if verification.order_item.instrument_type
                        else None
                    )
                ),
                serial_number=(
                    verification.order_item.instrument.serial_number
                    if verification.order_item.instrument
                    else None
                ),
                verification_date=verification.verification_date,
                verification_type=verification.verification_type,
                status=verification.status,
                result=verification.result,
                valid_until=verification.valid_until,
                created_at=verification.created_at,
                started_at=verification.started_at,
                decision_at=verification.decision_at,
                archived=verification.archived,
            )
            for verification in models
        ]
