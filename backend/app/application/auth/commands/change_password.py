"""Change the authenticated user's password command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangePasswordCommand:
    """Input required to change a user's own password."""

    user_id: UUID
    current_password: str
    new_password: str
