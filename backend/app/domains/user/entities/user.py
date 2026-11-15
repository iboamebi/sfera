"""
Domain entity: User.
"""

from dataclasses import dataclass

from app.domains.user.value_objects.user_role import UserRole
from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class User(Entity):
    """User identity and employee profile used by administration flows."""

    username: str
    password_hash: str
    full_name: str | None = None
    phone: str | None = None
    position: str | None = None
    role: UserRole = UserRole.OPERATOR
    archived: bool = False
    is_active: bool = True
    must_change_password: bool = False

    def update_profile(
        self,
        *,
        full_name: str,
        phone: str | None,
        position: str | None,
    ) -> None:
        """Update employee contact and display information."""

        self.full_name = full_name
        self.phone = phone
        self.position = position

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

    def reset_password(self, password_hash: str) -> None:
        """Replace the password and require a change at next login."""

        self.password_hash = password_hash
        self.must_change_password = True
