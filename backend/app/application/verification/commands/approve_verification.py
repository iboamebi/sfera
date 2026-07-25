"""
Approve verification command.
"""

from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.domains.verification.entities.verification import Verification


@dataclass(frozen=True)
class ApproveVerificationCommand:
    verification_id: UUID
    valid_until: date


class ApproveVerificationHandler:
    """Approve verification."""

    def __init__(
        self,
        service: VerificationApplicationService,
    ) -> None:
        self._service = service

    def handle(
        self,
        command: ApproveVerificationCommand,
    ) -> Verification:
        return self._service.approve(
            command.verification_id,
            command.valid_until,
        )
