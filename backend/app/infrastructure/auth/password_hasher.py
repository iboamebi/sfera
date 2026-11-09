"""
Argon2 password hashing adapter.
"""

from argon2 import PasswordHasher as Argon2PasswordHasherImpl
from argon2.exceptions import VerificationError

from app.shared.password_hasher import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    """Argon2 implementation of the password hasher port contract."""

    def __init__(self) -> None:
        self._hasher = Argon2PasswordHasherImpl()

    def hash(self, password: str) -> str:
        """Hash a plaintext password with Argon2id."""

        return self._hasher.hash(password)

    def verify(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """Verify a plaintext password against a stored hash."""

        try:
            return self._hasher.verify(password_hash, password)
        except VerificationError:
            return False
