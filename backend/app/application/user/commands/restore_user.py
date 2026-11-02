"""Command to restore a user account."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RestoreUserCommand:
    """Restore user command."""

    user_id: UUID
