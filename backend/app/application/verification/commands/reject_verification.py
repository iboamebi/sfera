from dataclasses import dataclass

from app.domains.verification.entities.verification import Verification
from app.domains.verification.services.verification_service import (
    VerificationService,
)


@dataclass(frozen=True)
class RejectVerificationCommand:
    verification: Verification
    reason: str


class RejectVerificationHandler:

    def handle(
        self,
        command: RejectVerificationCommand,
    ) -> None:

        VerificationService().reject(
            command.verification,
            command.reason,
        )
