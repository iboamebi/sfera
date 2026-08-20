"""
Order mapper.
"""

from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.value_objects.order_number import OrderNumber
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.order import Order as OrderModel


class OrderMapper(BaseMapper[Order, OrderModel]):
    """Order mapper."""

    def to_domain(
        self,
        model: OrderModel,
    ) -> Order:
        return Order(
            id=model.id,
            number=OrderNumber(model.number),
            customer_id=model.customer_id,
            received_at=model.received_at,
            planned_issue_at=model.planned_issue_at,
            issued_at=model.issued_at,
            comment=model.comment,
            status=model.status,
            items=[
                OrderItem(
                    id=item.id,
                    instrument_id=item.instrument_id,
                    comment=item.customer_comment,
                )
                for item in model.order_items
            ],
        )

    def to_model(
        self,
        entity: Order,
        model: OrderModel,
    ) -> OrderModel:
        model.number = entity.number.value
        model.customer_id = entity.customer_id
        model.received_at = entity.received_at
        model.planned_issue_at = entity.planned_issue_at
        model.issued_at = entity.issued_at
        model.comment = entity.comment
        model.status = entity.status.value

        return model
