"""Tests for the authenticated session domain entity."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.domains.auth.entities.session import Session


def test_session_is_valid_when_active_and_not_expired() -> None:
    now = datetime.now(UTC)
    session = Session(
        id=uuid4(),
        user_id=uuid4(),
        session_id="session-token",
        expires_at=now + timedelta(minutes=30),
    )

    assert session.is_valid(now)


def test_session_is_invalid_when_expired() -> None:
    now = datetime.now(UTC)
    session = Session(
        id=uuid4(),
        user_id=uuid4(),
        session_id="session-token",
        expires_at=now - timedelta(seconds=1),
    )

    assert not session.is_valid(now)


def test_revoke_invalidates_session() -> None:
    now = datetime.now(UTC)
    session = Session(
        id=uuid4(),
        user_id=uuid4(),
        session_id="session-token",
        expires_at=now + timedelta(minutes=30),
    )

    session.revoke()

    assert session.revoked
    assert not session.is_valid(now)
