"""Create user command."""

from dataclasses import dataclass

from app.domains.user.value_objects.user_role import UserRole


@dataclass(frozen=True)
class CreateUserCommand:
    """Input required to create a user account."""

    username: str
    role: UserRole
