"""
Application service: Authentication.
"""

from app.application.auth.commands.authenticate_user import (
    AuthenticateUserCommand,
)
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.application.auth.ports.password_hasher import PasswordHasher
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository


class AuthenticationApplicationService:
    """Authentication application service."""

    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher

    def authenticate(
        self,
        command: AuthenticateUserCommand,
    ) -> User:
        """Authenticate a user by username and password."""

        user = self._repository.get_by_username(command.username)

        if user is None or user.archived:
            raise AuthenticationFailedApplicationError

        if not self._password_hasher.verify(
            command.password,
            user.password_hash,
        ):
            raise AuthenticationFailedApplicationError

        return user
