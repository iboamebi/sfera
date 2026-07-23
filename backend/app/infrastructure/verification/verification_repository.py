"""
Infrastructure repository for Verification.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.verification.entities.verification import Verification
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.infrastructure.mappers.verification_mapper import (
    VerificationMapper,
)
from app.models.verification import Verification as VerificationModel


class VerificationRepositorySQLAlchemy(VerificationRepository):
    """SQLAlchemy implementation of VerificationRepository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
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

        # return VerificationFactory.from_model(model)
        return VerificationMapper().to_domain(model)

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
            model = VerificationModel(id=verification.id)
            self.session.add(model)

        # model.verification_date = verification.verification_date
        VerificationMapper().to_model(
            verification,
            model,
        )
        model.result = verification.result.value
        model.valid_until = verification.valid_until
        model.unsuitable_reason = verification.unsuitable_reason
        model.methodology = verification.methodology

        self.session.commit()
