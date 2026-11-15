"""
Verification read mapper.
"""

from app.domains.verification.read_models.verification_read_models import (
    VerificationListReadData,
)
from app.schemas.verification import VerificationListRead


class VerificationReadMapper:
    """Maps Verification read models to API schemas."""

    def to_schema(self, model: VerificationListReadData) -> VerificationListRead:
        return VerificationListRead(
            id=model.id,
            order_item_id=model.order_item_id,
            order_id=model.order_id,
            order_number=model.order_number,
            customer_id=model.customer_id,
            customer_name=model.customer_name,
            instrument_id=model.instrument_id,
            instrument_name=model.instrument_name,
            instrument_type_id=model.instrument_type_id,
            instrument_type_name=model.instrument_type_name,
            serial_number=model.serial_number,
            verification_date=model.verification_date,
            verification_type=model.verification_type,
            status=model.status,
            result=model.result,
            valid_until=model.valid_until,
            created_at=model.created_at,
            started_at=model.started_at,
            decision_at=model.decision_at,
            archived=model.archived,
        )
