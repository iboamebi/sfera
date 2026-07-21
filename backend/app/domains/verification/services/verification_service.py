from datetime import date

from app.domains.verification.entities.verification import Verification


class VerificationService:
    def approve(
        self,
        verification: Verification,
        valid_until: date,
    ) -> None:
        verification.mark_suitable(valid_until)

    def reject(
        self,
        verification: Verification,
        reason: str,
    ) -> None:
        verification.mark_unsuitable(reason)
