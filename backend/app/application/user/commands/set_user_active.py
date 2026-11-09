"""Set whether a user account is active."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SetUserActiveCommand:
    """Input required to activate or deactivate an account."""

    user_id: UUID
    is_active: bool
