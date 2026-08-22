"""
SQLAlchemy implementation of OrderReadRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.domains.order.read_models.order_read_models import (
    OrderReadData,
)
from app.domains.order.repositories.order_read_repository import (
    OrderReadRepository,
)
from app.models.instrument import Instrument
from app.models.order import Order
from app.models.order_item import OrderItem


class OrderReadRepositorySQLAlchemy(OrderReadRepository):
    """SQLAlchemy read repository for orders."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def get(
        self,
        order_id: UUID,
    ) -> OrderReadData | None:
        return (
            self.session.query(Order)
            .options(
                joinedload(Order.order_items)
                .joinedload(OrderItem.instrument)
                .joinedload(Instrument.instrument_type)
            )
            .filter(Order.id == order_id)
            .first()
        )
