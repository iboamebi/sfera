"""Change an existing user's role."""

from dataclasses import dataclass
from uuid import UUID

from app.domains.user.value_objects.user_role import UserRole


@dataclass(frozen=True)
class ChangeUserRoleCommand:
    """Input required to change a user's role."""

    user_id: UUID
    role: UserRole
