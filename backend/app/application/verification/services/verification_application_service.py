"""
Application service for verification use cases.
"""

from datetime import date

from app.domains.verification.entities.verification import Verification
from app.domains.verification.services.verification_service import (
    VerificationService,
)


class VerificationApplicationService:
    """Coordinates verification use cases."""

    def __init__(self) -> None:
        self._service = VerificationService()

    def approve(
        self,
        verification: Verification,
        valid_until: date,
    ) -> None:
        self._service.approve(
            verification,
            valid_until,
        )

    def reject(
        self,
        verification: Verification,
        reason: str,
    ) -> None:
        self._service.reject(
            verification,
            reason,
        )
