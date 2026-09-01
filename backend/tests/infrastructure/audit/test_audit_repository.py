from unittest.mock import Mock
from uuid import uuid4

from app.infrastructure.audit.audit_repository import AuditRepositorySQLAlchemy
from app.models.audit_record import AuditRecordModel
from app.shared.audit.models import AuditRecord


def test_audit_repository_class_exists():
    assert AuditRepositorySQLAlchemy is not None


def test_audit_repository_save_adds_and_flushes_record():
    session = Mock()
    record = AuditRecord(
        id=uuid4(),
        operation_id=uuid4(),
        actor_id=uuid4(),
        action="order.updated",
        entity_type="Order",
        entity_id=uuid4(),
        changes={"status": {"old": "draft", "new": "registered"}},
        reason="registration",
        related_record_id=None,
    )

    repository = AuditRepositorySQLAlchemy(session)
    repository.save(record)

    model = session.add.call_args.args[0]
    assert isinstance(model, AuditRecordModel)
    assert model.id == record.id
    assert model.operation_id == record.operation_id
    assert model.actor_id == record.actor_id
    assert model.action == record.action
    assert model.entity_type == record.entity_type
    assert model.entity_id == record.entity_id
    assert model.changes == record.changes
    assert model.reason == record.reason
    assert model.related_record_id == record.related_record_id
    assert model.occurred_at is None
    session.flush.assert_called_once_with()
