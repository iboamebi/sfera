"""
Tests for the Argon2 password hasher adapter.
"""

from argon2 import PasswordHasher as Argon2PasswordHasherImpl

from app.infrastructure.auth.password_hasher import Argon2PasswordHasher


def test_verify_password():
    password = "correct-password"
    password_hash = Argon2PasswordHasherImpl().hash(password)
    hasher = Argon2PasswordHasher()

    assert hasher.verify(password, password_hash) is True
    assert hasher.verify("wrong-password", password_hash) is False
