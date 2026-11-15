"""Update employee profile command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateUserProfileCommand:
    """Employee profile fields managed by an administrator."""

    user_id: UUID
    full_name: str
    phone: str | None
    position: str | None
