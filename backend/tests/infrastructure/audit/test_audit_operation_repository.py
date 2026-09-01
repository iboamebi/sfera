from unittest.mock import Mock
from uuid import uuid4

from app.application.audit.models import AuditOperation
from app.infrastructure.audit.audit_operation_repository import (
    AuditOperationRepositorySQLAlchemy,
)
from app.models.audit_operation import AuditOperationModel


def test_audit_operation_repository_class_exists():
    assert AuditOperationRepositorySQLAlchemy is not None


def test_audit_operation_repository_save_adds_and_flushes_operation():
    session = Mock()
    operation = AuditOperation(
        operation_id=uuid4(),
        initiated_by=uuid4(),
    )

    repository = AuditOperationRepositorySQLAlchemy(session)
    repository.save(operation)

    model = session.add.call_args.args[0]
    assert isinstance(model, AuditOperationModel)
    assert model.operation_id == operation.operation_id
    assert model.initiated_by == operation.initiated_by
    session.flush.assert_called_once_with()
