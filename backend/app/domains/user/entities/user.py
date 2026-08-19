"""
Domain entity: User.
"""

from dataclasses import dataclass

from app.domains.user.value_objects.user_role import UserRole
from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class User(Entity):
    """User identity used by authentication flows."""

    username: str
    password_hash: str
    role: UserRole = UserRole.OPERATOR
    archived: bool = False

    def archive(self) -> None:
        """Archive user and prevent authentication."""

        self.archived = True

    def restore(self) -> None:
        """Restore archived user."""

        self.archived = False
