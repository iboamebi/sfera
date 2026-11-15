from uuid import UUID, uuid4

import pytest

from app.application.device.commands.change_device_site import (
    ChangeDeviceSiteCommand,
)
from app.application.device.exceptions import (
    DeviceNotFoundApplicationError,
    DeviceSiteChangeReasonRequiredApplicationError,
    SiteCustomerMismatchApplicationError,
    SiteNotFoundApplicationError,
)
from app.application.device.services.device_site_assignment_application_service import (
    DeviceSiteAssignmentApplicationService,
)
from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.device.value_objects.serial_number import SerialNumber
from app.domains.site.entities.site import Site
from app.domains.site.repositories.site_repository import SiteRepository
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.audit.models import AuditOperation, AuditRecord
from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.shared.audit.repositories.audit_repository import AuditRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeDeviceRepository(DeviceRepository):
    def __init__(self, device: Device | None) -> None:
        self.device = device
        self.saved = False

    def get(self, device_id: UUID) -> Device | None:
        if self.device is not None and self.device.id == device_id:
            return self.device
        return None

    def list(self) -> list[Device]:
        return [self.device] if self.device is not None else []

    def exists_by_customer_type_and_serial_number(
        self,
        customer_id: UUID,
        instrument_type_id: UUID,
        serial_number: str,
        exclude_device_id: UUID | None = None,
    ) -> bool:
        return False

    def save(self, device: Device) -> None:
        self.device = device
        self.saved = True


class FakeSiteRepository(SiteRepository):
    def __init__(self, *sites: Site) -> None:
        self.sites = {site.id: site for site in sites}

    def get(self, site_id: UUID) -> Site | None:
        return self.sites.get(site_id)

    def get_all(self) -> list[Site]:
        return list(self.sites.values())

    def get_by_customer_id(self, customer_id: UUID) -> list[Site]:
        return [site for site in self.sites.values() if site.customer_id == customer_id]

    def save(self, site: Site) -> Site:
        self.sites[site.id] = site
        return site


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        pass


class FakeAuditOperationRepository(AuditOperationRepository):
    def __init__(self) -> None:
        self.operations: list[AuditOperation] = []

    def save(self, operation: AuditOperation) -> None:
        self.operations.append(operation)


class FakeAuditRepository(AuditRepository):
    def __init__(self) -> None:
        self.records: list[AuditRecord] = []

    def save(self, record: AuditRecord) -> None:
        self.records.append(record)


def make_service(
    device: Device | None,
    *sites: Site,
) -> tuple[
    DeviceSiteAssignmentApplicationService,
    FakeDeviceRepository,
    FakeUnitOfWork,
    FakeAuditOperationRepository,
    FakeAuditRepository,
]:
    device_repository = FakeDeviceRepository(device)
    uow = FakeUnitOfWork()
    audit_operations = FakeAuditOperationRepository()
    audit_records = FakeAuditRepository()
    service = DeviceSiteAssignmentApplicationService(
        device_repository,
        FakeSiteRepository(*sites),
        uow,
        audit_operations,
        audit_records,
    )
    return service, device_repository, uow, audit_operations, audit_records


def make_user() -> User:
    return User(
        id=uuid4(),
        username="site-operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )


def test_change_device_site_records_old_new_site_actor_and_reason() -> None:
    customer_id = uuid4()
    old_site = Site(
        id=uuid4(),
        customer_id=customer_id,
        name="Old site",
        address="Old address",
    )
    new_site = Site(
        id=uuid4(),
        customer_id=customer_id,
        name="New site",
        address="New address",
    )
    device = Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        customer_id=customer_id,
        site_id=old_site.id,
        serial_number=SerialNumber("SN-001"),
    )
    service, repository, uow, operations, records = make_service(
        device,
        old_site,
        new_site,
    )
    user = make_user()

    result = service.change_site(
        ChangeDeviceSiteCommand(
            device_id=device.id,
            site_id=new_site.id,
            reason="  Approved project change  ",
        ),
        user,
    )

    assert result.site_id == new_site.id
    assert repository.saved
    assert uow.committed
    assert not uow.rolled_back
    assert len(operations.operations) == 1
    assert len(records.records) == 1
    record = records.records[0]
    assert record.action == "instrument.site_changed"
    assert record.entity_type == "Instrument"
    assert record.entity_id == device.id
    assert record.actor_id == user.id
    assert record.reason == "Approved project change"
    assert record.changes == {
        "site": {
            "old": {"id": str(old_site.id), "name": "Old site"},
            "new": {"id": str(new_site.id), "name": "New site"},
        },
    }
    assert record.operation_id == operations.operations[0].operation_id


def test_change_device_site_can_clear_site_with_reason() -> None:
    customer_id = uuid4()
    old_site = Site(
        id=uuid4(),
        customer_id=customer_id,
        name="Old site",
        address="Old address",
    )
    device = Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        customer_id=customer_id,
        site_id=old_site.id,
        serial_number=SerialNumber("SN-001"),
    )
    service, _, _, _, records = make_service(device, old_site)

    service.change_site(
        ChangeDeviceSiteCommand(
            device_id=device.id,
            site_id=None,
            reason="Site is no longer known",
        ),
        make_user(),
    )

    assert device.site_id is None
    assert records.records[0].changes["site"]["new"] == {
        "id": None,
        "name": None,
    }


def test_change_device_site_rejects_site_from_another_customer() -> None:
    device = Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        customer_id=uuid4(),
        serial_number=SerialNumber("SN-001"),
    )
    other_site = Site(
        id=uuid4(),
        customer_id=uuid4(),
        name="Other site",
        address="Other address",
    )
    service, repository, uow, operations, records = make_service(
        device,
        other_site,
    )

    with pytest.raises(SiteCustomerMismatchApplicationError):
        service.change_site(
            ChangeDeviceSiteCommand(
                device_id=device.id,
                site_id=other_site.id,
                reason="Invalid move",
            ),
            make_user(),
        )

    assert not repository.saved
    assert not uow.committed
    assert uow.rolled_back
    assert operations.operations == []
    assert records.records == []


def test_change_device_site_rejects_missing_device_or_site() -> None:
    service, _, uow, _, records = make_service(None)

    with pytest.raises(DeviceNotFoundApplicationError):
        service.change_site(
            ChangeDeviceSiteCommand(
                device_id=uuid4(),
                site_id=None,
                reason="Unassign",
            ),
            make_user(),
        )

    assert uow.rolled_back
    assert records.records == []

    customer_id = uuid4()
    device = Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        customer_id=customer_id,
        serial_number=SerialNumber("SN-002"),
    )
    service, _, uow, _, records = make_service(device)

    with pytest.raises(SiteNotFoundApplicationError):
        service.change_site(
            ChangeDeviceSiteCommand(
                device_id=device.id,
                site_id=uuid4(),
                reason="Move",
            ),
            make_user(),
        )

    assert uow.rolled_back
    assert records.records == []


def test_change_device_site_requires_nonblank_reason_and_skips_noop_audit() -> None:
    site = Site(
        id=uuid4(),
        customer_id=uuid4(),
        name="Current site",
        address="Current address",
    )
    device = Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        customer_id=site.customer_id,
        site_id=site.id,
        serial_number=SerialNumber("SN-001"),
    )
    service, repository, uow, operations, records = make_service(device, site)

    with pytest.raises(DeviceSiteChangeReasonRequiredApplicationError):
        service.change_site(
            ChangeDeviceSiteCommand(
                device_id=device.id,
                site_id=None,
                reason="   ",
            ),
            make_user(),
        )

    result = service.change_site(
        ChangeDeviceSiteCommand(
            device_id=device.id,
            site_id=site.id,
            reason="No actual change",
        ),
        make_user(),
    )

    assert result is device
    assert not repository.saved
    assert uow.committed
    assert operations.operations == []
    assert records.records == []
