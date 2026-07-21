from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.verification.entities.verification import (
    Verification,
)
from app.domains.verification.factories.verification_factory import (
    VerificationFactory,
)
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.models.verification import Verification as VerificationModel


class VerificationRepositorySQLAlchemy(VerificationRepository):
    def __init__(
        self,
        session: Session,
    ):
        self.session = session

    def get(
        self,
        verification_id: UUID,
    ) -> Verification | None:
        model = (
            self.session.query(VerificationModel)
            .filter(VerificationModel.id == verification_id)
            .first()
        )

        if model is None:
            return None

        return VerificationFactory.from_model(model)

    def save(
        self,
        verification: Verification,
    ) -> None:
        model = (
            self.session.query(VerificationModel)
            .filter(VerificationModel.id == verification.id)
            .first()
        )

        if model is None:
            raise ValueError("Verification not found")

        model.result = verification.result
        model.valid_until = verification.valid_until
        model.unsuitable_reason = verification.unsuitable_reason

        self.session.commit()
