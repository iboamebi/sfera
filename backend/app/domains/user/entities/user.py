"""
Domain entity: User.
"""

from dataclasses import dataclass

from app.domains.user.value_objects.user_role import UserRole
from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class User(Entity):
    """User identity used by authentication and administration flows."""

    username: str
    password_hash: str
    role: UserRole = UserRole.OPERATOR
    archived: bool = False
    is_active: bool = True
    must_change_password: bool = False

    def archive(self) -> None:
        """Archive user and prevent authentication."""

        self.archived = True

    def restore(self) -> None:
        """Restore archived user."""

        self.archived = False

    def deactivate(self) -> None:
        """Disable the user account without archiving its history."""

        self.is_active = False

    def activate(self) -> None:
        """Enable the user account."""

        self.is_active = True

    def change_role(self, role: UserRole) -> None:
        """Assign a role to the user."""

        self.role = role

    def change_password(self, password_hash: str) -> None:
        """Replace the password and clear the first-login requirement."""

        self.password_hash = password_hash
        self.must_change_password = False
