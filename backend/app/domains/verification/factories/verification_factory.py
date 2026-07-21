from app.domains.verification.entities.verification import Verification
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.models.verification import Verification as VerificationModel


class VerificationFactory:
    @staticmethod
    def from_model(
        model: VerificationModel,
    ) -> Verification:
        return Verification(
            id=model.id,
            verification_date=model.verification_date,
            result=VerificationResult(model.result.value),
            valid_until=model.valid_until,
            unsuitable_reason=model.unsuitable_reason,
            methodology=model.methodology,
        )
