"""
User repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.user.entities.user import User


class UserRepository(ABC):
    """Abstract user repository."""

    @abstractmethod
    def get_by_id(
        self,
        user_id: UUID,
        include_archived: bool = False,
    ) -> User | None:
        """Get user by identifier."""

        raise NotImplementedError

    @abstractmethod
    def get_by_username(
        self,
        username: str,
        include_archived: bool = False,
    ) -> User | None:
        """Get user by username."""

        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        include_archived: bool = False,
    ) -> list[User]:
        """Get users, including inactive accounts and optionally archived users."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        user: User,
    ) -> User:
        """Save user."""

        raise NotImplementedError
