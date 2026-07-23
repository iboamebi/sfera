"""
Approve verification command.
"""

from dataclasses import dataclass
from datetime import date

from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.domains.verification.entities.verification import Verification


@dataclass(frozen=True)
class ApproveVerificationCommand:
    verification: Verification
    valid_until: date


class ApproveVerificationHandler:
    """Approve verification."""

    def __init__(
        self,
        service: VerificationApplicationService | None = None,
    ) -> None:
        self.service = service or VerificationApplicationService()

    def handle(
        self,
        command: ApproveVerificationCommand,
    ) -> None:
        self.service.approve(
            command.verification,
            command.valid_until,
        )
