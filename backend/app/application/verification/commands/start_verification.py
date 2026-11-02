"""Start verification command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class StartVerificationCommand:
    """Start execution of a registered verification."""

    verification_id: UUID
