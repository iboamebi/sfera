"""
Argon2 password hashing adapter.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from app.application.auth.ports.password_hasher import PasswordHasherPort


class Argon2PasswordHasher(PasswordHasherPort):
    """Argon2 implementation of the password hasher port."""

    def __init__(self) -> None:
        self._hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        """Hash a plaintext password."""

        return self._hasher.hash(password)

    def verify(self, password_hash: str, password: str) -> bool:
        """Verify a plaintext password against a hash."""

        try:
            return self._hasher.verify(password_hash, password)
        except VerificationError:
            return False
