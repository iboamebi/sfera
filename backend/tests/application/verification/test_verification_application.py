from datetime import UTC, date, datetime
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.correct_verification_decision import (
    CorrectVerificationDecisionCommand,
)
from app.application.verification.commands.correct_verification_valid_until import (
    CorrectVerificationValidUntilCommand,
)
from app.application.verification.commands.create_verification import (
    CreateVerificationCommand,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
)
from app.application.verification.commands.start_verification import (
    StartVerificationCommand,
)
from app.application.verification.exceptions import (
    VerificationCannotBeStartedApplicationError,
    VerificationInstrumentRequiredApplicationError,
    VerificationNotFoundApplicationError,
    VerificationOrderItemNotFoundApplicationError,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.verification.entities.verification import Verification
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.domains.verification.value_objects.verification_type import (
    VerificationType,
)
from app.shared.audit.models import AuditOperation, AuditRecord
from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.shared.audit.repositories.audit_repository import AuditRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.registered_operation_ids: list[UUID | None] = []

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        self.registered_operation_ids.append(operation_id)


class FakeVerificationRepository(VerificationRepository):
    def __init__(self) -> None:
        self._items: dict[UUID, Verification] = {}

    def get(
        self,
        verification_id: UUID,
    ) -> Verification | None:
        return self._items.get(verification_id)

    def save(
        self,
        verification: Verification,
    ) -> None:
        self._items[verification.id] = verification


class FakeOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: dict[UUID, Order] = {}

    def get(self, order_id: UUID) -> Order | None:
        return self._orders.get(order_id)

    def get_by_order_item_id(self, order_item_id: UUID) -> Order | None:
        return next(
            (
                order
                for order in self._orders.values()
                if any(item.id == order_item_id for item in order.items)
            ),
            None,
        )

    def list(self) -> list[Order]:
        return list(self._orders.values())

    def has_conflicting_order_for_instrument(
        self,
        instrument_id: UUID,
        exclude_order_id: UUID,
    ) -> bool:
        return False

    def save(self, order: Order) -> None:
        self._orders[order.id] = order


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
        username="test-user",
        password_hash="test-hash",
        role=role,
    )


def make_service(
    repository: FakeVerificationRepository,
    order_repository: FakeOrderRepository | None = None,
) -> VerificationApplicationService:
    return VerificationApplicationService(
        repository,
        order_repository or FakeOrderRepository(),
        FakeUnitOfWork(),
        FakeAuditOperationRepository(),
        FakeAuditRepository(),
    )


def make_order_with_item(
    *,
    instrument_id: UUID | None,
) -> tuple[Order, OrderItem]:
    item = OrderItem(
        id=uuid4(),
        instrument_id=instrument_id,
    )
    order = Order(
        id=uuid4(),
        number=OrderNumber(f"TEST-{uuid4().hex[:8]}"),
        customer_id=uuid4(),
        received_at=date.today(),
        items=[item],
    )
    return order, item


def make_verification() -> Verification:
    """Create a verification in the active execution state."""
    verification = Verification.create(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=uuid4(),
        verification_date=date.today(),
        created_at=datetime(2026, 9, 5, 10, 0, tzinfo=UTC),
        verification_type=VerificationType.PERIODIC,
    )
    verification.start(started_at=datetime(2026, 9, 5, 11, 0, tzinfo=UTC))
    return verification


def test_create_verification_copies_instrument_from_order_item():
    repository = FakeVerificationRepository()
    order_repository = FakeOrderRepository()
    audit_operation_repository = FakeAuditOperationRepository()
    audit_repository = FakeAuditRepository()
    order, item = make_order_with_item(instrument_id=uuid4())
    order_repository.save(order)
    service = VerificationApplicationService(
        repository,
        order_repository,
        FakeUnitOfWork(),
        audit_operation_repository,
        audit_repository,
    )

    verification = service.create(
        CreateVerificationCommand(
            order_item_id=item.id,
            verification_date=date(2026, 9, 4),
            verification_type=VerificationType.PERIODIC,
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert verification.order_item_id == item.id
    assert verification.instrument_id == item.instrument_id
    assert verification.status == VerificationStatus.CREATED
    assert verification.started_at is None
    assert verification.result is None
    assert verification.decision_at is None
    assert repository.get(verification.id) is verification
    assert len(audit_operation_repository.items) == 1
    assert len(audit_repository.items) == 1

    operation = audit_operation_repository.items[0]
    record = audit_repository.items[0]
    assert record.operation_id == operation.operation_id
    assert operation.initiated_by == record.actor_id
    assert record.actor_id is not None
    assert record.action == "verification.created"
    assert record.entity_type == "Verification"
    assert record.entity_id == verification.id
    assert record.changes["status"] == {
        "old": None,
        "new": VerificationStatus.CREATED.value,
    }
    assert record.changes["verification_type"] == {
        "old": None,
        "new": VerificationType.PERIODIC.value,
    }


def test_create_verification_requires_existing_order_item():
    service = make_service(FakeVerificationRepository())

    with pytest.raises(VerificationOrderItemNotFoundApplicationError):
        service.create(
            CreateVerificationCommand(
                order_item_id=uuid4(),
                verification_date=date.today(),
                verification_type=VerificationType.PERIODIC,
            ),
            make_user(UserRole.METROLOGIST),
        )


def test_create_verification_requires_concrete_instrument():
    repository = FakeVerificationRepository()
    order_repository = FakeOrderRepository()
    order, item = make_order_with_item(instrument_id=None)
    order_repository.save(order)
    service = make_service(repository, order_repository)

    with pytest.raises(VerificationInstrumentRequiredApplicationError):
        service.create(
            CreateVerificationCommand(
                order_item_id=item.id,
                verification_date=date.today(),
                verification_type=VerificationType.PERIODIC,
            ),
            make_user(UserRole.METROLOGIST),
        )

    assert repository._items == {}


def test_create_verification_requires_metrologist_or_admin():
    repository = FakeVerificationRepository()
    order_repository = FakeOrderRepository()
    order, item = make_order_with_item(instrument_id=uuid4())
    order_repository.save(order)
    service = make_service(repository, order_repository)

    with pytest.raises(AuthorizationError):
        service.create(
            CreateVerificationCommand(
                order_item_id=item.id,
                verification_date=date.today(),
                verification_type=VerificationType.PERIODIC,
            ),
            make_user(UserRole.OPERATOR),
        )


def test_start_verification_transitions_and_audits():
    repository = FakeVerificationRepository()
    order_repository = FakeOrderRepository()
    order, item = make_order_with_item(instrument_id=uuid4())
    order.register()
    order_repository.save(order)
    verification = Verification.create(
        id=uuid4(),
        order_item_id=item.id,
        instrument_id=item.instrument_id,
        verification_date=date.today(),
        created_at=datetime(2026, 9, 5, 10, 0, tzinfo=UTC),
        verification_type=VerificationType.PERIODIC,
    )
    repository.save(verification)
    audit_operations = FakeAuditOperationRepository()
    audit_records = FakeAuditRepository()
    service = VerificationApplicationService(
        repository,
        order_repository,
        FakeUnitOfWork(),
        audit_operations,
        audit_records,
    )
    result = service.start(
        StartVerificationCommand(verification_id=verification.id),
        make_user(UserRole.METROLOGIST),
    )
    assert result.status == VerificationStatus.IN_PROGRESS
    assert result.started_at is not None
    assert result.started_at.tzinfo is not None
    assert order.status.value == "IN_WORK"
    assert len(audit_operations.items) == 1
    assert len(audit_records.items) == 2
    record = audit_records.items[0]
    assert record.action == "verification.started"
    assert record.changes["status"] == {
        "old": VerificationStatus.CREATED.value,
        "new": VerificationStatus.IN_PROGRESS.value,
    }
    assert record.changes["started_at"]["old"] is None
    assert record.changes["started_at"]["new"] == result.started_at.isoformat()
    order_record = audit_records.items[1]
    assert order_record.action == "order.started_work"
    assert order_record.entity_type == "order"
    assert order_record.entity_id == order.id
    assert order_record.changes["status"] == {
        "old": "REGISTERED",
        "new": "IN_WORK",
    }


def test_start_verification_rejects_invalid_state():
    repository = FakeVerificationRepository()
    verification = make_verification()
    repository.save(verification)
    with pytest.raises(VerificationCannotBeStartedApplicationError):
        make_service(repository).start(
            StartVerificationCommand(verification_id=verification.id),
            make_user(UserRole.METROLOGIST),
        )


def test_start_verification_requires_metrologist_or_admin():
    repository = FakeVerificationRepository()
    verification = Verification.create(
        id=uuid4(),
        order_item_id=uuid4(),
        instrument_id=uuid4(),
        verification_date=date.today(),
        created_at=datetime(2026, 9, 5, 10, 0, tzinfo=UTC),
        verification_type=VerificationType.PERIODIC,
    )
    repository.save(verification)
    with pytest.raises(AuthorizationError):
        make_service(repository).start(
            StartVerificationCommand(verification_id=verification.id),
            make_user(UserRole.OPERATOR),
        )


def test_start_verification_raises_when_not_found():
    with pytest.raises(VerificationNotFoundApplicationError):
        make_service(FakeVerificationRepository()).start(
            StartVerificationCommand(verification_id=uuid4()),
            make_user(UserRole.METROLOGIST),
        )


def test_approve_verification():
    repository = FakeVerificationRepository()
    verification = make_verification()
    repository.save(verification)

    service = make_service(repository)

    service.approve(
        ApproveVerificationCommand(
            verification_id=verification.id,
            valid_until=date(2030, 1, 1),
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert verification.status == VerificationStatus.DECIDED
    assert verification.result == VerificationResult.SUITABLE
    assert verification.valid_until == date(2030, 1, 1)
    assert verification.unsuitable_reason is None
    assert verification.decision_at is not None


def test_reject_verification():
    repository = FakeVerificationRepository()
    verification = make_verification()
    repository.save(verification)

    service = make_service(repository)

    service.reject(
        RejectVerificationCommand(
            verification_id=verification.id,
            reason="Broken seal",
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert verification.status == VerificationStatus.DECIDED
    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Broken seal"
    assert verification.decision_at is not None


def test_verification_approval_requires_metrologist_or_admin():
    repository = FakeVerificationRepository()
    verification = make_verification()
    repository.save(verification)

    service = make_service(repository)

    with pytest.raises(AuthorizationError):
        service.approve(
            ApproveVerificationCommand(
                verification_id=verification.id,
                valid_until=date(2030, 1, 1),
            ),
            make_user(UserRole.OPERATOR),
        )


def test_verification_rejection_requires_metrologist_or_admin():
    repository = FakeVerificationRepository()
    verification = make_verification()
    repository.save(verification)

    service = make_service(repository)

    with pytest.raises(AuthorizationError):
        service.reject(
            RejectVerificationCommand(
                verification_id=verification.id,
                reason="Broken seal",
            ),
            make_user(UserRole.TECHNICIAN),
        )


def test_verification_approval_allows_admin():
    repository = FakeVerificationRepository()
    verification = make_verification()
    repository.save(verification)

    service = make_service(repository)

    service.approve(
        ApproveVerificationCommand(
            verification_id=verification.id,
            valid_until=date(2030, 1, 1),
        ),
        make_user(UserRole.ADMIN),
    )

    assert verification.status == VerificationStatus.DECIDED
    assert verification.result == VerificationResult.SUITABLE
    assert verification.decision_at is not None


def test_verification_rejection_allows_admin():
    repository = FakeVerificationRepository()
    verification = make_verification()
    repository.save(verification)

    service = make_service(repository)

    service.reject(
        RejectVerificationCommand(
            verification_id=verification.id,
            reason="Broken seal",
        ),
        make_user(UserRole.ADMIN),
    )

    assert verification.status == VerificationStatus.DECIDED
    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.decision_at is not None


def test_verification_approval_raises_when_not_found():
    service = make_service(FakeVerificationRepository())

    with pytest.raises(VerificationNotFoundApplicationError):
        service.approve(
            ApproveVerificationCommand(
                verification_id=uuid4(),
                valid_until=date(2030, 1, 1),
            ),
            make_user(UserRole.METROLOGIST),
        )


def test_verification_rejection_raises_when_not_found():
    service = make_service(FakeVerificationRepository())

    with pytest.raises(VerificationNotFoundApplicationError):
        service.reject(
            RejectVerificationCommand(
                verification_id=uuid4(),
                reason="Broken seal",
            ),
            make_user(UserRole.METROLOGIST),
        )


def test_approve_verification_calculates_validity_from_local_decision_date():
    repository = FakeVerificationRepository()
    verification = make_verification()
    repository.save(verification)
    service = make_service(repository)

    result = service.approve(
        ApproveVerificationCommand(
            verification_id=verification.id,
            duration_years=2,
            time_zone="Europe/Amsterdam",
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert result.decision_at is not None
    local_date = result.decision_at.astimezone(
        ZoneInfo("Europe/Amsterdam"),
    ).date()
    try:
        anniversary = local_date.replace(year=local_date.year + 2)
    except ValueError:
        anniversary = local_date.replace(year=local_date.year + 2, day=28)
    from datetime import timedelta

    assert result.valid_until == anniversary - timedelta(days=1)


def test_correct_valid_until_persists_and_writes_reasoned_audit():
    repository = FakeVerificationRepository()
    verification = make_verification()
    verification.mark_suitable(
        date(2030, 1, 1),
        decision_at=datetime(2026, 11, 14, 10, 0, tzinfo=UTC),
    )
    repository.save(verification)
    operations = FakeAuditOperationRepository()
    records = FakeAuditRepository()
    service = VerificationApplicationService(
        repository,
        FakeOrderRepository(),
        FakeUnitOfWork(),
        operations,
        records,
    )

    result = service.correct_valid_until(
        CorrectVerificationValidUntilCommand(
            verification_id=verification.id,
            valid_until=date(2029, 12, 31),
            reason="Исправлена ошибка ввода",
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert result.valid_until == date(2029, 12, 31)
    assert len(operations.items) == len(records.items) == 1
    assert records.items[0].action == "verification.valid_until_corrected"
    assert records.items[0].changes["valid_until"] == {
        "old": "2030-01-01",
        "new": "2029-12-31",
    }
    assert records.items[0].reason == "Исправлена ошибка ввода"


def test_correct_verification_decision_persists_and_audits_old_and_new_values():
    repository = FakeVerificationRepository()
    verification = make_verification()
    verification.mark_suitable(
        date(2030, 1, 1),
        decision_at=datetime(2026, 11, 14, 10, 0, tzinfo=UTC),
    )
    repository.save(verification)
    operations = FakeAuditOperationRepository()
    records = FakeAuditRepository()
    service = VerificationApplicationService(
        repository,
        FakeOrderRepository(),
        FakeUnitOfWork(),
        operations,
        records,
    )

    result = service.correct_decision(
        CorrectVerificationDecisionCommand(
            verification_id=verification.id,
            result=VerificationResult.UNSUITABLE,
            valid_until=None,
            unsuitable_reason="Повреждена пломба",
            reason="Исправлена ошибка первоначального решения",
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert result.result == VerificationResult.UNSUITABLE
    assert result.valid_until is None
    assert result.unsuitable_reason == "Повреждена пломба"
    assert result.decision_at is not None
    assert repository.get(verification.id) is result
    assert len(operations.items) == len(records.items) == 1
    record = records.items[0]
    assert record.action == "verification.decision_corrected"
    assert record.changes["result"] == {
        "old": VerificationResult.SUITABLE.value,
        "new": VerificationResult.UNSUITABLE.value,
    }
    assert record.changes["valid_until"] == {
        "old": "2030-01-01",
        "new": None,
    }
    assert record.changes["unsuitable_reason"] == {
        "old": None,
        "new": "Повреждена пломба",
    }
    assert record.changes["decision_at"]["old"] == "2026-11-14T10:00:00+00:00"
    assert record.changes["decision_at"]["new"] == result.decision_at.isoformat()
    assert record.reason == "Исправлена ошибка первоначального решения"


def test_correct_verification_decision_requires_metrologist_or_admin():
    repository = FakeVerificationRepository()
    verification = make_verification()
    verification.mark_suitable(
        date(2030, 1, 1),
        decision_at=datetime(2026, 11, 14, 10, 0, tzinfo=UTC),
    )
    repository.save(verification)

    with pytest.raises(AuthorizationError):
        make_service(repository).correct_decision(
            CorrectVerificationDecisionCommand(
                verification_id=verification.id,
                result=VerificationResult.UNSUITABLE,
                valid_until=None,
                unsuitable_reason="Повреждена пломба",
                reason="Исправление",
            ),
            make_user(UserRole.OPERATOR),
        )

def test_correct_verification_decision_rejects_unsuitable_to_suitable():
    from app.domains.verification.exceptions import (
        InvalidDecisionCorrectionDomainError,
    )

    repository = FakeVerificationRepository()
    verification = make_verification()
    verification.mark_unsuitable(
        "Повреждена пломба",
        decision_at=datetime(2026, 11, 14, 10, 0, tzinfo=UTC),
    )
    repository.save(verification)
    operations = FakeAuditOperationRepository()
    records = FakeAuditRepository()
    service = VerificationApplicationService(
        repository,
        FakeOrderRepository(),
        FakeUnitOfWork(),
        operations,
        records,
    )

    with pytest.raises(InvalidDecisionCorrectionDomainError):
        service.correct_decision(
            CorrectVerificationDecisionCommand(
                verification_id=verification.id,
                result=VerificationResult.SUITABLE,
                valid_until=date(2030, 1, 1),
                unsuitable_reason=None,
                reason="Нужно оформить как пригодное",
            ),
            make_user(UserRole.METROLOGIST),
        )

    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Повреждена пломба"
    assert operations.items == []
    assert records.items == []

