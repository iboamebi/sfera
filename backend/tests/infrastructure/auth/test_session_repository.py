from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.domains.auth.entities.session import Session
from app.infrastructure.auth.session_repository import SessionRepositorySQLAlchemy


class FakeQuery:
    def __init__(self, models: list[object]) -> None:
        self.models = models
        self.filters = []

    def filter(self, *conditions: object) -> "FakeQuery":
        self.filters.extend(conditions)
        return self

    def first(self) -> object | None:
        return self.models[0] if self.models else None

    def update(self, values: dict[object, object], synchronize_session: bool) -> int:
        for model in self.models:
            for attribute, value in values.items():
                setattr(model, attribute.name, value)
        return len(self.models)


class FakeSession:
    def __init__(self, models: list[object] | None = None) -> None:
        self.models = models or []
        self.added: list[object] = []
        self.flushed = False

    def query(self, model: type[object]) -> FakeQuery:
        return FakeQuery(self.models)

    def add(self, model: object) -> None:
        self.added.append(model)

    def flush(self) -> None:
        self.flushed = True


def test_save_creates_model() -> None:
    user_id = uuid4()
    entity = Session(
        id=uuid4(),
        user_id=user_id,
        session_id="session-1",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    session = FakeSession()

    saved = SessionRepositorySQLAlchemy(session).save(entity)

    assert saved == entity
    assert len(session.added) == 1
    assert session.flushed is True


def test_get_active_returns_none_without_model() -> None:
    session = FakeSession()
    repository = SessionRepositorySQLAlchemy(session)

    result = repository.get_active(
        "missing",
        datetime.now(timezone.utc),
    )

    assert result is None


def test_revoke_is_idempotent_without_model() -> None:
    session = FakeSession()
    SessionRepositorySQLAlchemy(session).revoke("missing")

    assert session.flushed is False


def test_revoke_all_for_user_flushes() -> None:
    session = FakeSession()
    SessionRepositorySQLAlchemy(session).revoke_all_for_user(uuid4())

    assert session.flushed is True
