"""Tests for the authenticated session domain entity."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.domains.auth.entities.session import Session


def make_session(now: datetime) -> Session:
    return Session(
        id=uuid4(),
        user_id=uuid4(),
        session_id="session-token",
        expires_at=now + timedelta(hours=12),
        last_activity_at=now,
    )


def test_session_is_valid_when_active_and_not_expired() -> None:
    now = datetime.now(UTC)
    assert make_session(now).is_valid(now)


def test_session_is_invalid_when_absolute_lifetime_expires() -> None:
    now = datetime.now(UTC)
    session = make_session(now)
    session.expires_at = now
    assert not session.is_valid(now)


def test_session_is_invalid_after_one_hour_of_inactivity() -> None:
    now = datetime.now(UTC)
    session = make_session(now)
    assert not session.is_valid(now + timedelta(hours=1))


def test_activity_updates_timestamp_without_changing_absolute_expiry() -> None:
    now = datetime.now(UTC)
    session = make_session(now)
    expires_at = session.expires_at

    session.record_activity(now + timedelta(minutes=30))

    assert session.last_activity_at == now + timedelta(minutes=30)
    assert session.expires_at == expires_at


def test_activity_cannot_move_timestamp_backwards() -> None:
    now = datetime.now(UTC)
    session = make_session(now)
    later = now + timedelta(minutes=10)
    session.record_activity(later)
    session.record_activity(now)

    assert session.last_activity_at == later


def test_revoke_invalidates_session() -> None:
    now = datetime.now(UTC)
    session = make_session(now)
    session.revoke()

    assert session.revoked
    assert not session.is_valid(now)
