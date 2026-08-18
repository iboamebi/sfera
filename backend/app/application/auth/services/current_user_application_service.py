"""
Application service: Current authenticated user.
"""

from app.application.auth.commands.get_current_user import GetCurrentUserCommand
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.domains.auth.repositories.session_repository import SessionRepository
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository


class CurrentUserApplicationService:
    """Resolve the user associated with an authenticated session."""

    def __init__(
        self,
        session_repository: SessionRepository,
        user_repository: UserRepository,
    ) -> None:
        self._session_repository = session_repository
        self._user_repository = user_repository

    def get(
        self,
        command: GetCurrentUserCommand,
    ) -> User:
        """Return the current user or raise a generic authentication error."""

        session = self._session_repository.get_active(
            command.session_id,
            command.now,
        )
        if session is None:
            raise AuthenticationFailedApplicationError

        user = self._user_repository.get_by_id(session.user_id)
        if user is None or user.archived:
            raise AuthenticationFailedApplicationError

        return user
