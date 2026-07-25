"""
Reject verification command.
"""

from dataclasses import dataclass
from uuid import UUID

from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.domains.verification.entities.verification import Verification


@dataclass(frozen=True)
class RejectVerificationCommand:
    verification_id: UUID
    reason: str


class RejectVerificationHandler:
    """Reject verification."""

    def __init__(
        self,
        service: VerificationApplicationService,
    ) -> None:
        self._service = service

    def handle(
        self,
        command: RejectVerificationCommand,
    ) -> Verification:
        return self._service.reject(
            command.verification_id,
            command.reason,
        )
