"""Command to correct a previously decided verification result."""

from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)


@dataclass(frozen=True)
class CorrectVerificationDecisionCommand:
    """Correct a final verification decision with an explicit reason."""

    verification_id: UUID
    result: VerificationResult
    valid_until: date | None
    unsuitable_reason: str | None
    reason: str
