"""Command to archive a user account."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ArchiveUserCommand:
    """Archive user command."""

    user_id: UUID
