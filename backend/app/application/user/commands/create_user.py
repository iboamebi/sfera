"""Create user command."""

from dataclasses import dataclass

from app.domains.user.value_objects.user_role import UserRole


@dataclass(frozen=True)
class CreateUserCommand:
    """Input required to create a user account and employee profile."""

    username: str
    full_name: str
    phone: str | None
    position: str | None
    role: UserRole
