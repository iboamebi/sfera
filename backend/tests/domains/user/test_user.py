"""
Tests for User domain entity.
"""

from uuid import uuid4

from app.domains.user.entities.user import User


def test_user_defaults_to_active():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed-password",
    )

    assert user.archived is False


def test_archive_user():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed-password",
    )

    user.archive()

    assert user.archived is True


def test_restore_user():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed-password",
        archived=True,
    )

    user.restore()

    assert user.archived is False
