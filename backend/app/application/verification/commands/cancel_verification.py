from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class CancelVerificationCommand:
    verification_id: UUID
    reason: str | None = None
