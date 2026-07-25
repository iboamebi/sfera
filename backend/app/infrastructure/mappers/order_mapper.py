"""
Order mapper.
"""

from app.domains.order.entities.order import Order
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
            status=model.status,
        )

    def to_model(
        self,
        entity: Order,
        model: OrderModel,
    ) -> OrderModel:
        model.number = entity.number.value
        model.customer_id = entity.customer_id
        model.status = entity.status.value
        return model
