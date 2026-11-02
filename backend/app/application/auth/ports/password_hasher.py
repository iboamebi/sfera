"""
Password hashing port.
"""

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Abstract password hashing service."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Return a secure hash for a plaintext password."""

        raise NotImplementedError

    @abstractmethod
    def verify(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """Verify a plaintext password against a stored hash."""

        raise NotImplementedError
