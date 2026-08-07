"""
SQLAlchemy implementation of VerificationRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.verification.entities.verification import Verification
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.infrastructure.mappers.verification_mapper import VerificationMapper
from app.models.verification import Verification as VerificationModel


class VerificationRepositorySQLAlchemy(VerificationRepository):
    """SQLAlchemy implementation of VerificationRepository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
        self._mapper = VerificationMapper()

    def get(
        self,
        verification_id: UUID,
    ) -> Verification | None:
        """Get verification by identifier."""

        model = (
            self.session.query(VerificationModel)
            .filter(VerificationModel.id == verification_id)
            .first()
        )

        if model is None:
            return None

        return self._mapper.to_domain(model)

    def save(
        self,
        verification: Verification,
    ) -> None:
        """Save verification."""

        model = (
            self.session.query(VerificationModel)
            .filter(VerificationModel.id == verification.id)
            .first()
        )

        if model is None:
            model = VerificationModel(
                id=verification.id,
            )
            self.session.add(model)

        self._mapper.to_model(
            verification,
            model,
        )

        self.session.flush()
