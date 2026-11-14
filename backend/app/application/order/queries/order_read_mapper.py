"""
Order read mapper.
"""

from app.domains.order.read_models.order_read_models import OrderReadData
from app.schemas.order import OrderItemRead, OrderItemVerificationRead, OrderRead


class OrderReadMapper:
    """Maps order read models to API read schemas."""

    def to_schema(self, model: OrderReadData) -> OrderRead:
        return OrderRead(
            id=model.id,
            number=model.number,
            customer_id=model.customer_id,
            customer_name=model.customer_name,
            status=model.status,
            received_at=model.received_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
            planned_issue_at=model.planned_issue_at,
            issued_at=model.issued_at,
            comment=model.comment,
            archived=model.archived,
            items=[
                OrderItemRead(
                    id=item.id,
                    instrument_id=item.instrument_id,
                    instrument_type_id=item.instrument_type_id,
                    instrument_name=item.instrument_name,
                    instrument_type_name=item.instrument_type_name,
                    serial_number=item.serial_number,
                    modification=item.modification,
                    comment=item.comment,
                    requested_operations=item.requested_operations,
                    verification_ids=item.verification_ids,
                    verifications=[
                        OrderItemVerificationRead(
                            id=verification.id,
                            created_at=verification.created_at,
                            verification_date=verification.verification_date,
                            verification_type=verification.verification_type,
                            status=verification.status,
                            result=verification.result,
                            valid_until=verification.valid_until,
                            archived=verification.archived,
                        )
                        for verification in item.verifications
                    ],
                )
                for item in model.items
            ],
        )
