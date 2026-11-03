from uuid import UUID, uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.repair.services.repair_application_service import (
    RepairApplicationService,
)
from app.domains.repair.entities.repair import Repair
from app.domains.repair.repositories.repair_repository import RepairRepository
from app.domains.repair.value_objects.repair_status import RepairStatus
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


class FakeRepairRepository(RepairRepository):
    def __init__(self) -> None:
        self.items: dict[UUID, Repair] = {}

    def get(self, repair_id: UUID) -> Repair | None:
        return self.items.get(repair_id)

    def save(self, repair: Repair) -> None:
        self.items[repair.id] = repair


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
        username="repair-test-user",
        password_hash="test-hash",
        role=role,
    )


def make_service():
    repository = FakeRepairRepository()
    audit_operations = FakeAuditOperationRepository()
    audit_records = FakeAuditRepository()
    service = RepairApplicationService(
        repository,
        FakeUnitOfWork(),
        audit_operations,
        audit_records,
    )
    return service, repository, audit_operations, audit_records


def test_complete_repair_persists_audit_record():
    service, repository, audit_operations, audit_records = make_service()
    repair = Repair.create(
        id=uuid4(),
        order_item_id=uuid4(),
        description="Replace damaged component",
    )
    repair.start()
    repository.save(repair)
    user = make_user(UserRole.TECHNICIAN)

    result = service.complete(repair.id, "Component replaced", user)

    assert result.status == RepairStatus.COMPLETED
    assert result.result == "Component replaced"
    assert len(audit_operations.items) == 1
    assert len(audit_records.items) == 1

    operation = audit_operations.items[0]
    record = audit_records.items[0]
    assert operation.initiated_by == user.id
    assert record.operation_id == operation.operation_id
    assert record.actor_id == user.id
    assert record.action == "repair.completed"
    assert record.entity_type == "repair"
    assert record.entity_id == repair.id
    assert record.changes == {
        "status": {
            "old": RepairStatus.IN_WORK.value,
            "new": RepairStatus.COMPLETED.value,
        },
        "result": {
            "old": None,
            "new": "Component replaced",
        },
    }


def test_complete_repair_rejects_unauthorized_user():
    service, repository, audit_operations, audit_records = make_service()
    repair = Repair.create(
        id=uuid4(),
        order_item_id=uuid4(),
    )
    repair.start()
    repository.save(repair)

    with pytest.raises(AuthorizationError):
        service.complete(
            repair.id,
            "Unauthorized result",
            make_user(UserRole.OPERATOR),
        )

    assert repair.status == RepairStatus.IN_WORK
    assert audit_operations.items == []
    assert audit_records.items == []
