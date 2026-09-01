from unittest.mock import Mock

from app.core.dependencies.repositories import get_audit_repository
from app.infrastructure.audit.audit_repository import AuditRepositorySQLAlchemy


def test_get_audit_repository_returns_sqlalchemy_implementation():
    session = Mock()

    repository = get_audit_repository(session)

    assert isinstance(repository, AuditRepositorySQLAlchemy)
    assert repository.session is session
