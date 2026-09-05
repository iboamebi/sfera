from datetime import date
from uuid import uuid4

from app.domains.verification.entities.verification import Verification
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.infrastructure.verification.verification_repository import (
    VerificationRepositorySQLAlchemy,
)
from app.models.verification import Verification as VerificationModel


class FakeQuery:
    """Minimal query double for repository tests."""

    def __init__(self, model: VerificationModel | None = None) -> None:
        self.model = model

    def filter(self, *conditions: object) -> "FakeQuery":
        return self

    def first(self) -> VerificationModel | None:
        return self.model


class FakeSession:
    """Minimal session double for repository tests."""

    def __init__(self, model: VerificationModel | None = None) -> None:
        self.model = model
        self.added: list[object] = []
        self.flushed = False

    def query(self, model: type[VerificationModel]) -> FakeQuery:
        return FakeQuery(self.model)

    def add(self, model: object) -> None:
        self.added.append(model)

    def flush(self) -> None:
        self.flushed = True


def make_verification(
    *,
    instrument_id: object | None = None,
) -> Verification:
    """Build a verification entity for repository tests."""
    return Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=instrument_id,
        verification_date=date(2026, 9, 5),
        result=VerificationResult.SUITABLE,
        valid_until=date(2027, 9, 5),
        unsuitable_reason=None,
        methodology="method-1",
    )


def test_get_maps_instrument_id() -> None:
    instrument_id = uuid4()
    model = VerificationModel(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=instrument_id,
        verification_date=date(2026, 9, 5),
        result="SUITABLE",
        valid_until=date(2027, 9, 5),
        unsuitable_reason=None,
        methodology="method-1",
    )
    session = FakeSession(model)

    result = VerificationRepositorySQLAlchemy(session).get(model.id)

    assert result is not None
    assert result.id == model.id
    assert result.instrument_id == instrument_id


def test_get_returns_none_without_model() -> None:
    session = FakeSession()

    result = VerificationRepositorySQLAlchemy(session).get(uuid4())

    assert result is None


def test_save_creates_model_with_instrument_id() -> None:
    instrument_id = uuid4()
    entity = make_verification(instrument_id=instrument_id)
    session = FakeSession()

    VerificationRepositorySQLAlchemy(session).save(entity)

    assert len(session.added) == 1
    model = session.added[0]
    assert isinstance(model, VerificationModel)
    assert model.id == entity.id
    assert model.order_item_id == entity.order_item_id
    assert model.instrument_id == instrument_id
    assert model.verification_date == entity.verification_date
    assert model.valid_until == entity.valid_until
    assert model.result == entity.result.value
    assert model.methodology == entity.methodology
    assert session.flushed is True


def test_save_preserves_none_instrument_id() -> None:
    entity = make_verification(instrument_id=None)
    session = FakeSession()

    VerificationRepositorySQLAlchemy(session).save(entity)

    model = session.added[0]
    assert isinstance(model, VerificationModel)
    assert model.instrument_id is None
    assert session.flushed is True


def test_save_updates_existing_model_instrument_id() -> None:
    instrument_id = uuid4()
    entity = make_verification(instrument_id=instrument_id)
    model = VerificationModel(
        id=entity.id,
        order_item_id=uuid4(),
        instrument_id=None,
        verification_date=date(2026, 1, 1),
        result="UNSUITABLE",
        valid_until=None,
        unsuitable_reason="old reason",
        methodology="old-method",
    )
    session = FakeSession(model)

    VerificationRepositorySQLAlchemy(session).save(entity)

    assert session.added == []
    assert model.instrument_id == instrument_id
    assert model.order_item_id == entity.order_item_id
    assert model.result == entity.result.value
    assert session.flushed is True
