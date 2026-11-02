"""Application service for user administration."""

from app.application.authorization.authorization import require_role
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository
from app.domains.user.value_objects.user_role import UserRole


class UserAdministrationApplicationService:
    """Coordinates administrator-only user management use cases."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def get_all(self, user: User, include_archived: bool = False) -> list[User]:
        """List users for an administrator."""
        require_role(user, UserRole.ADMIN)
        return self._repository.get_all(include_archived=include_archived)
