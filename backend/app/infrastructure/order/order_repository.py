"""
SQLAlchemy implementation of OrderRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.order.entities.order import Order as DomainOrder
from app.domains.order.repositories.order_repository import (
    OrderRepository,
)
from app.infrastructure.mappers.order_mapper import OrderMapper
from app.models.order import Order as ORMOrder


class OrderRepositorySQLAlchemy(OrderRepository):
    """SQLAlchemy order repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
        self.mapper = OrderMapper()

    def get(
        self,
        order_id: UUID,
    ) -> DomainOrder | None:
        """Get order by identifier."""

        model = self.session.query(ORMOrder).filter(ORMOrder.id == order_id).first()

        if model is None:
            return None

        return self.mapper.to_domain(model)

    def save(
        self,
        order: DomainOrder,
    ) -> None:
        """Save order."""

        model = self.session.query(ORMOrder).filter(ORMOrder.id == order.id).first()

        if model is None:
            model = ORMOrder(
                id=order.id,
            )

            self.session.add(model)

        self.mapper.to_model(
            order,
            model,
        )

        self.session.flush()
