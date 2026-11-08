"""Reset an existing user's password command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ResetUserPasswordCommand:
    """Identify the account whose password must be reset."""

    user_id: UUID
