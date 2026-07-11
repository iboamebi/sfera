from dataclasses import dataclass
from datetime import date

from app.domains.verification.entities.verification import Verification
from app.domains.verification.services.verification_service import (
    VerificationService,
)


@dataclass(frozen=True)
class ApproveVerificationCommand:
    verification: Verification
    valid_until: date


class ApproveVerificationHandler:

    def handle(
        self,
        command: ApproveVerificationCommand,
    ) -> None:

        VerificationService().approve(
            command.verification,
            command.valid_until,
        )
