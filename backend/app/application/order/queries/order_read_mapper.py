"""
Order read mapper.
"""

from app.domains.order.read_models.order_read_models import (
    OrderReadData,
)
from app.schemas.order import OrderItemRead, OrderRead


class OrderReadMapper:
    """Maps ORM order models to API read schemas."""

    def to_schema(
        self,
        model: OrderReadData,
    ) -> OrderRead:
        return OrderRead(
            id=model.id,
            number=model.number,
            customer_id=model.customer_id,
            status=model.status,
            received_at=model.received_at,
            planned_issue_at=model.planned_issue_at,
            issued_at=model.issued_at,
            comment=model.comment,
            archived=model.archived,
            items=[
                OrderItemRead(
                    id=item.id,
                    instrument_id=item.instrument_id,
                    instrument_type_name=(
                        item.instrument.instrument_type.name
                        if item.instrument
                        and item.instrument.instrument_type
                        else None
                    ),
                    serial_number=(
                        item.instrument.serial_number
                        if item.instrument
                        else None
                    ),
                    comment=item.customer_comment,
                )
                for item in model.items
            ],
        )
