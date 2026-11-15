"""Tests for the administrator audit read service."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.audit.queries.audit_read_service import AuditReadService
from app.application.authorization.authorization import AuthorizationError
from app.domains.audit.read_models.audit_read_models import AuditRecordReadData
from app.domains.audit.repositories.audit_read_repository import AuditReadRepository
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole


class FakeAuditReadRepository(AuditReadRepository):
    def __init__(self, records: list[AuditRecordReadData], total: int) -> None:
        self.records = records
        self.total = total
        self.filters = None

    def list(self, **filters):
        self.filters = filters
        return self.records, self.total


def make_user(role: UserRole) -> User:
    return User(
        id=uuid4(),
        username="test-user",
        password_hash="hash",
        role=role,
    )


def test_admin_can_list_audit_records_and_filters_are_forwarded() -> None:
    occurred_at = datetime(2026, 11, 15, 12, 0, tzinfo=UTC)
    record = AuditRecordReadData(
        id=uuid4(),
        operation_id=uuid4(),
        actor_id=uuid4(),
        actor_username="operator",
        actor_full_name="Operator",
        initiated_by=uuid4(),
        initiator_username="admin",
        initiator_full_name="Administrator",
        action="verification.approved",
        entity_type="Verification",
        entity_id=uuid4(),
        entity_display_name="Поверка · заказ № 42 · СИ № 123",
        changes={"result": {"old": None, "new": "SUITABLE"}},
        reason=None,
        related_record_id=None,
        occurred_at=occurred_at,
    )
    repository = FakeAuditReadRepository([record], total=17)
    service = AuditReadService(repository)
    occurred_from = datetime(2026, 11, 1, tzinfo=UTC)
    operation_id = uuid4()
    actor_id = uuid4()

    result = service.list(
        make_user(UserRole.ADMIN),
        occurred_from=occurred_from,
        actor_id=actor_id,
        actor_query="Operat",
        action="verification.approved",
        entity_type="Verification",
        operation_id=operation_id,
        limit=25,
        offset=5,
    )

    assert result.total == 17
    assert result.limit == 25
    assert result.offset == 5
    assert result.items[0].id == record.id
    assert result.items[0].actor_username == "operator"
    assert result.items[0].initiator_username == "admin"
    assert result.items[0].entity_display_name == record.entity_display_name
    assert result.items[0].changes == record.changes
    assert repository.filters == {
        "occurred_from": occurred_from,
        "occurred_to": None,
        "actor_id": actor_id,
        "actor_query": "Operat",
        "action": "verification.approved",
        "entity_type": "Verification",
        "operation_id": operation_id,
        "limit": 25,
        "offset": 5,
    }


def test_non_admin_cannot_read_audit_records() -> None:
    repository = FakeAuditReadRepository([], total=0)
    service = AuditReadService(repository)

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.list(make_user(UserRole.OPERATOR))

    assert repository.filters is None
