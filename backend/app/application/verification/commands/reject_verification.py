"""
Reject verification command.
"""

from dataclasses import dataclass

from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.domains.verification.entities.verification import Verification


@dataclass(frozen=True)
class RejectVerificationCommand:
    verification: Verification
    reason: str


class RejectVerificationHandler:
    """Reject verification."""

    def __init__(
        self,
        service: VerificationApplicationService | None = None,
    ) -> None:
        self.service = service or VerificationApplicationService()

    def handle(
        self,
        command: RejectVerificationCommand,
    ) -> None:
        self.service.reject(
            command.verification,
            command.reason,
        )
