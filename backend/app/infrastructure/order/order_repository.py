"""
SQLAlchemy implementation of OrderRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.order.entities.order import Order as DomainOrder
from app.domains.order.repositories.order_repository import (
    OrderRepository,
)
from app.domains.order.value_objects.order_status import (
    CONFLICTING_INSTRUMENT_ORDER_STATUSES,
)
from app.infrastructure.mappers.order_mapper import OrderMapper
from app.models.order import Order as ORMOrder
from app.models.order_item import OrderItem as ORMOrderItem


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

    def get_by_order_item_id(
        self,
        order_item_id: UUID,
    ) -> DomainOrder | None:
        """Get the order containing an order item."""

        model = (
            self.session.query(ORMOrder)
            .join(ORMOrderItem, ORMOrderItem.order_id == ORMOrder.id)
            .filter(ORMOrderItem.id == order_item_id)
            .first()
        )

        if model is None:
            return None

        return self.mapper.to_domain(model)

    def list(
        self,
    ) -> list[DomainOrder]:
        """List orders."""

        models = self.session.query(ORMOrder).all()

        return [self.mapper.to_domain(model) for model in models]

    def has_conflicting_order_for_instrument(
        self,
        instrument_id: UUID,
        exclude_order_id: UUID,
    ) -> bool:
        """Check whether an instrument belongs to another active order."""

        return (
            self.session.query(ORMOrderItem)
            .join(ORMOrder)
            .filter(
                ORMOrderItem.instrument_id == instrument_id,
                ORMOrder.id != exclude_order_id,
                ORMOrder.status.in_(
                    [
                        status.value
                        for status in CONFLICTING_INSTRUMENT_ORDER_STATUSES
                    ]
                ),
            )
            .first()
            is not None
        )

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
