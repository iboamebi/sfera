from datetime import date
from uuid import UUID, uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.create_verification import (
    CreateVerificationCommand,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
)
from app.application.verification.exceptions import (
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


def test_create_verification_copies_instrument_from_order_item():
    repository = FakeVerificationRepository()
    order_repository = FakeOrderRepository()
    order, item = make_order_with_item(instrument_id=uuid4())
    order_repository.save(order)
    service = make_service(repository, order_repository)

    verification = service.create(
        CreateVerificationCommand(
            order_item_id=item.id,
            verification_date=date(2026, 9, 4),
            result=VerificationResult.SUITABLE,
            valid_until=date(2030, 1, 1),
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert verification.order_item_id == item.id
    assert verification.instrument_id == item.instrument_id
    assert repository.get(verification.id) is verification


def test_create_verification_requires_existing_order_item():
    service = make_service(FakeVerificationRepository())

    with pytest.raises(VerificationOrderItemNotFoundApplicationError):
        service.create(
            CreateVerificationCommand(
                order_item_id=uuid4(),
                verification_date=date.today(),
                result=VerificationResult.SUITABLE,
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
                result=VerificationResult.SUITABLE,
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
                result=VerificationResult.SUITABLE,
            ),
            make_user(UserRole.OPERATOR),
        )


def test_approve_verification():
    repository = FakeVerificationRepository()

    verification = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.UNSUITABLE,
    )

    repository.save(verification)

    service = make_service(repository)

    service.approve(
        ApproveVerificationCommand(
            verification_id=verification.id,
            valid_until=date(2030, 1, 1),
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert verification.result == VerificationResult.SUITABLE
    assert verification.valid_until == date(2030, 1, 1)


def test_reject_verification():
    repository = FakeVerificationRepository()

    verification = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.SUITABLE,
    )

    repository.save(verification)

    service = make_service(repository)

    service.reject(
        RejectVerificationCommand(
            verification_id=verification.id,
            reason="Broken seal",
        ),
        make_user(UserRole.METROLOGIST),
    )

    assert verification.result == VerificationResult.UNSUITABLE
    assert verification.valid_until is None
    assert verification.unsuitable_reason == "Broken seal"


def test_verification_approval_requires_metrologist_or_admin():
    repository = FakeVerificationRepository()

    verification = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.UNSUITABLE,
    )

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

    verification = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.SUITABLE,
    )

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
    verification = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.UNSUITABLE,
    )
    repository.save(verification)

    service = make_service(repository)

    service.approve(
        ApproveVerificationCommand(
            verification_id=verification.id,
            valid_until=date(2030, 1, 1),
        ),
        make_user(UserRole.ADMIN),
    )

    assert verification.result == VerificationResult.SUITABLE


def test_verification_rejection_allows_admin():
    repository = FakeVerificationRepository()
    verification = Verification(
        id=uuid4(),
        order_item_id=uuid4(),
        verification_date=date.today(),
        result=VerificationResult.SUITABLE,
    )
    repository.save(verification)

    service = make_service(repository)

    service.reject(
        RejectVerificationCommand(
            verification_id=verification.id,
            reason="Broken seal",
        ),
        make_user(UserRole.ADMIN),
    )

    assert verification.result == VerificationResult.UNSUITABLE


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
