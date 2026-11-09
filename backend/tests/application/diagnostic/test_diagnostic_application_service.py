from uuid import UUID, uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.diagnostic.commands.complete_diagnostic import (
    CompleteDiagnosticCommand,
)
from app.application.diagnostic.services.diagnostic_application_service import (
    DiagnosticApplicationService,
)
from app.domains.diagnostic.entities.diagnostic import Diagnostic
from app.domains.diagnostic.repositories.diagnostic_repository import (
    DiagnosticRepository,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.audit.models import AuditOperation, AuditRecord
from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.shared.audit.repositories.audit_repository import AuditRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        pass


class FakeDiagnosticRepository(DiagnosticRepository):
    def __init__(self) -> None:
        self.items: dict[UUID, Diagnostic] = {}

    def get(self, diagnostic_id: UUID) -> Diagnostic | None:
        return self.items.get(diagnostic_id)

    def save(self, diagnostic: Diagnostic) -> None:
        self.items[diagnostic.id] = diagnostic


class FakeAuditOperationRepository(AuditOperationRepository):
    def __init__(self) -> None:
        self.items: list[AuditOperation] = []

    def save(self, operation: AuditOperation) -> None:
        self.items.append(operation)


class FakeAuditRepository(AuditRepository):
    def __init__(self) -> None:
        self.items: list[AuditRecord] = []

    def save(self, record: AuditRecord) -> None:
        self.items.append(record)


def make_user(role: UserRole) -> User:
    return User(
        id=uuid4(),
        username="diagnostic-test-user",
        password_hash="test-hash",
        role=role,
    )


def make_service():
    repository = FakeDiagnosticRepository()
    audit_operations = FakeAuditOperationRepository()
    audit_records = FakeAuditRepository()
    service = DiagnosticApplicationService(
        repository,
        FakeUnitOfWork(),
        audit_operations,
        audit_records,
    )
    return service, repository, audit_operations, audit_records


def test_complete_diagnostic_persists_audit_record():
    service, repository, audit_operations, audit_records = make_service()
    diagnostic = Diagnostic(
        id=uuid4(),
        order_item_id=uuid4(),
    )
    repository.save(diagnostic)
    user = make_user(UserRole.TECHNICIAN)

    result = service.complete(
        CompleteDiagnosticCommand(
            diagnostic_id=diagnostic.id,
            conclusion="The instrument requires repair",
        ),
        user,
    )

    assert result.conclusion == "The instrument requires repair"
    assert len(audit_operations.items) == 1
    assert len(audit_records.items) == 1

    operation = audit_operations.items[0]
    record = audit_records.items[0]
    assert operation.initiated_by == user.id
    assert record.operation_id == operation.operation_id
    assert record.actor_id == user.id
    assert record.action == "diagnostic.completed"
    assert record.entity_type == "diagnostic"
    assert record.entity_id == diagnostic.id
    assert record.changes == {
        "conclusion": {
            "old": None,
            "new": "The instrument requires repair",
        },
    }


def test_complete_diagnostic_rejects_unauthorized_user():
    service, repository, audit_operations, audit_records = make_service()
    diagnostic = Diagnostic(
        id=uuid4(),
        order_item_id=uuid4(),
    )
    repository.save(diagnostic)

    with pytest.raises(AuthorizationError):
        service.complete(
            CompleteDiagnosticCommand(
                diagnostic_id=diagnostic.id,
                conclusion="Unauthorized conclusion",
            ),
            make_user(UserRole.OPERATOR),
        )

    assert diagnostic.conclusion is None
    assert audit_operations.items == []
    assert audit_records.items == []
