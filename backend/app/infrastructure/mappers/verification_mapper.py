"""
Verification mapper.
"""

from app.domains.verification.entities.verification import Verification
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
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
            verification_date=model.verification_date,
            result=VerificationResult(model.result),
            valid_until=model.valid_until,
            unsuitable_reason=model.unsuitable_reason,
            methodology=model.methodology,
        )

    def to_model(
        self,
        entity: Verification,
        model: VerificationModel,
    ) -> VerificationModel:
        model.verification_date = entity.verification_date
        model.result = entity.result.value
        model.valid_until = entity.valid_until
        model.unsuitable_reason = entity.unsuitable_reason
        model.methodology = entity.methodology
        return model
