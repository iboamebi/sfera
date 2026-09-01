from unittest.mock import Mock

from app.core.dependencies.repositories import get_audit_operation_repository
from app.infrastructure.audit.audit_operation_repository import (
    AuditOperationRepositorySQLAlchemy,
)


def test_get_audit_operation_repository_returns_sqlalchemy_implementation():
    session = Mock()

    repository = get_audit_operation_repository(session)

    assert isinstance(repository, AuditOperationRepositorySQLAlchemy)
    assert repository.session is session
