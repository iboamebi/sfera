from datetime import UTC, datetime
from uuid import uuid4

from app.infrastructure.integration.integration_log_repository import (
    IntegrationLogRepositorySQLAlchemy,
)
from app.models.integration_log import IntegrationLogModel, IntegrationLogStatus
from app.shared.integration.models import IntegrationLog
from app.shared.integration.models import IntegrationLogStatus as DomainStatus


class FakeSession:
    """Minimal SQLAlchemy session double for repository tests."""

    def __init__(self, model: IntegrationLogModel | None = None) -> None:
        self.model = model
        self.added: list[object] = []
        self.flushed = False

    def get(self, model_type: type[IntegrationLogModel], identifier: object):
        if self.model is not None and self.model.id == identifier:
            return self.model
        return None

    def add(self, model: object) -> None:
        self.added.append(model)

    def flush(self) -> None:
        self.flushed = True


def make_log() -> IntegrationLog:
    return IntegrationLog(
        id=uuid4(),
        integration_type="ARSHIN",
        operation="EXPORT",
        status=DomainStatus.SUCCESS,
        request_data={"verification_id": "1"},
        response_data={"file_name": "export.xlsm"},
        created_by=uuid4(),
        created_at=datetime(2026, 11, 17, tzinfo=UTC),
    )


def test_save_creates_model() -> None:
    entity = make_log()
    session = FakeSession()

    IntegrationLogRepositorySQLAlchemy(session).save(entity)

    assert len(session.added) == 1
    model = session.added[0]
    assert isinstance(model, IntegrationLogModel)
    assert model.id == entity.id
    assert model.integration_type == "ARSHIN"
    assert model.operation == "EXPORT"
    assert model.status == IntegrationLogStatus.SUCCESS
    assert model.request_data == entity.request_data
    assert model.response_data == entity.response_data
    assert model.created_by == entity.created_by
    assert model.created_at == entity.created_at
    assert session.flushed is True


def test_get_maps_model_to_domain() -> None:
    model = IntegrationLogModel(
        id=uuid4(),
        integration_type="ARSHIN",
        operation="EXPORT",
        status=IntegrationLogStatus.ERROR,
        request_data={"verification_id": "1"},
        response_data={"error": "invalid"},
        created_by=uuid4(),
        created_at=datetime(2026, 11, 17, tzinfo=UTC),
    )
    session = FakeSession(model)

    result = IntegrationLogRepositorySQLAlchemy(session).get(model.id)

    assert result is not None
    assert result.id == model.id
    assert result.status == DomainStatus.ERROR
    assert result.request_data == model.request_data
    assert result.response_data == model.response_data
