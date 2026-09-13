"""
Verification mapper.
"""

from app.domains.verification.entities.verification import Verification
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.verification import Verification as VerificationModel


class VerificationMapper(
    BaseMapper[
        Verification,
        VerificationModel,
    ]
):
    """Verification mapper."""

    def to_domain(
        self,
        model: VerificationModel,
    ) -> Verification:
        return Verification(
            id=model.id,
            order_item_id=model.order_item_id,
            instrument_id=model.instrument_id,
            verification_date=model.verification_date,
            status=VerificationStatus(model.status),
            result=(
                VerificationResult(model.result)
                if model.result is not None
                else None
            ),
            valid_until=model.valid_until,
            unsuitable_reason=model.unsuitable_reason,
            methodology=model.methodology,
            decision_at=model.decision_at,
        )

    def to_model(
        self,
        entity: Verification,
        model: VerificationModel,
    ) -> VerificationModel:
        model.order_item_id = entity.order_item_id
        model.instrument_id = entity.instrument_id
        model.verification_date = entity.verification_date
        model.status = entity.status.value
        model.result = (
            entity.result.value
            if entity.result is not None
            else None
        )
        model.valid_until = entity.valid_until
        model.unsuitable_reason = entity.unsuitable_reason
        model.methodology = entity.methodology
        model.decision_at = entity.decision_at
        return model
