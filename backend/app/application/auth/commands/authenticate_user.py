"""
Authenticate user command.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticateUserCommand:
    """Command for authenticating a user."""

    username: str
    password: str
