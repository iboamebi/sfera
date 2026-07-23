"""
Infrastructure implementation of VerificationRepository.
"""

from uuid import UUID

from app.domains.verification.entities.verification import Verification
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)


class InfrastructureVerificationRepository(VerificationRepository):
    """SQLAlchemy implementation."""

    def get(
        self,
        verification_id: UUID,
    ) -> Verification | None:
        raise NotImplementedError

    def save(
        self,
        verification: Verification,
    ) -> None:
        raise NotImplementedError
