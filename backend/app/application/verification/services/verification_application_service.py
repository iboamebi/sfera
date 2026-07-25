"""
Application service for verification use cases.
"""

from datetime import date
from uuid import UUID

from app.domains.verification.entities.verification import Verification
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.domains.verification.services.verification_service import (
    VerificationService,
)


class VerificationApplicationService:
    """Coordinates verification use cases."""

    def __init__(
        self,
        repository: VerificationRepository,
    ) -> None:
        self._repository = repository
        self._service = VerificationService()

    def get(
        self,
        verification_id: UUID,
    ) -> Verification:
        verification = self._repository.get(verification_id)

        if verification is None:
            raise ValueError("Verification not found")

        return verification

    def approve(
        self,
        verification_id: UUID,
        valid_until: date,
    ) -> Verification:
        verification = self.get(verification_id)

        self._service.approve(
            verification,
            valid_until,
        )

        self._repository.save(verification)

        return verification

    def reject(
        self,
        verification_id: UUID,
        reason: str,
    ) -> Verification:
        verification = self.get(verification_id)

        self._service.reject(
            verification,
            reason,
        )

        self._repository.save(verification)

        return verification
