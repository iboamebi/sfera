"""
Application authorization contract.
"""

from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole


class AuthorizationError(Exception):
    """Raised when a user is not authorized for an application action."""


def require_role(user: User, *allowed_roles: UserRole) -> None:
    """Require the authenticated user to have one of the allowed roles."""

    if user.role not in allowed_roles:
        raise AuthorizationError("User is not authorized for this action.")
