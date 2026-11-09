"""
Tests for User domain entity.
"""

from uuid import uuid4

from app.domains.user.entities.user import User


def test_user_defaults_to_active_without_forced_password_change():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed-password",
    )

    assert user.archived is False
    assert user.is_active is True
    assert user.must_change_password is False


def test_archive_user():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed-password",
    )

    user.archive()

    assert user.archived is True
    assert user.is_active is True


def test_restore_user():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed-password",
        archived=True,
    )

    user.restore()

    assert user.archived is False


def test_deactivate_and_activate_user_without_archiving():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed-password",
    )

    user.deactivate()

    assert user.is_active is False
    assert user.archived is False

    user.activate()

    assert user.is_active is True
    assert user.archived is False


def test_change_password_clears_first_login_requirement():
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="temporary-hash",
        must_change_password=True,
    )

    user.change_password("new-hash")

    assert user.password_hash == "new-hash"
    assert user.must_change_password is False
