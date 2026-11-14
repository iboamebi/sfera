from uuid import UUID, uuid4

import pytest

from app.application.device.commands.connect_device import ConnectDeviceCommand
from app.application.device.commands.create_device import CreateDeviceCommand
from app.application.device.commands.disconnect_device import DisconnectDeviceCommand
from app.application.device.exceptions import (
    CustomerNotFoundApplicationError,
    DuplicateDeviceSerialNumberApplicationError,
    InstrumentTypeNotFoundApplicationError,
    SiteCustomerMismatchApplicationError,
    SiteNotFoundApplicationError,
)
from app.application.device.services.device_application_service import (
    DeviceApplicationService,
)
from app.domains.customer.entities.customer import Customer
from app.domains.customer.repositories.customer_repository import CustomerRepository
from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber
from app.domains.instrument_type.entities.instrument_type import InstrumentType
from app.domains.instrument_type.repositories.instrument_type_repository import (
    InstrumentTypeRepository,
)
from app.domains.site.entities.site import Site
from app.domains.site.repositories.site_repository import SiteRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeDeviceRepository(DeviceRepository):
    def __init__(
        self,
        device: Device,
    ):
        self.device = device

    def get(
        self,
        device_id,
    ):
        if device_id == self.device.id:
            return self.device

        return None

    def list(self):
        return [self.device]

    def exists_by_customer_type_and_serial_number(
        self,
        customer_id,
        instrument_type_id,
        serial_number,
        exclude_device_id=None,
    ):
        return (
            self.device.id != exclude_device_id
            and self.device.customer_id == customer_id
            and self.device.instrument_type_id == instrument_type_id
            and self.device.serial_number.value.strip().lower()
            == serial_number.strip().lower()
        )

    def save(
        self,
        device,
    ):
        self.device = device


class FakeInstrumentTypeRepository(InstrumentTypeRepository):
    def __init__(
        self,
        instrument_type: InstrumentType,
    ):
        self.instrument_type = instrument_type

    def get(
        self,
        instrument_type_id,
    ):
        if instrument_type_id == self.instrument_type.id:
            return self.instrument_type

        return None

    def get_all(self):
        return [self.instrument_type]

    def save(
        self,
        instrument_type,
    ):
        self.instrument_type = instrument_type


class FakeCustomerRepository(CustomerRepository):
    def __init__(self, customer: Customer):
        self.customer = customer

    def get(self, customer_id, include_archived=False):
        if customer_id == self.customer.id and (
            include_archived or not self.customer.archived
        ):
            return self.customer
        return None

    def get_all(self, include_archived=False):
        if include_archived or not self.customer.archived:
            return [self.customer]
        return []

    def save(self, customer):
        self.customer = customer
        return customer


class FakeSiteRepository(SiteRepository):
    def __init__(self, site: Site | None = None):
        self.site = site

    def get(self, site_id):
        if self.site is not None and site_id == self.site.id:
            return self.site
        return None

    def get_all(self):
        return [self.site] if self.site is not None else []

    def get_by_customer_id(self, customer_id):
        if self.site is not None and self.site.customer_id == customer_id:
            return [self.site]
        return []

    def save(self, site):
        self.site = site
        return site


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        pass


def test_device_create():
    instrument_type = InstrumentType(
        id=uuid4(),
        name="Pressure gauge",
    )
    instrument_type_repository = FakeInstrumentTypeRepository(
        instrument_type,
    )
    repository = FakeDeviceRepository(
        Device(
            id=uuid4(),
            instrument_type_id=instrument_type.id,
            customer_id=uuid4(),
            serial_number=SerialNumber("SN-001"),
        ),
    )
    customer = Customer(id=uuid4(), name="Test customer")
    customer_repository = FakeCustomerRepository(customer)
    site_repository = FakeSiteRepository()
    uow = FakeUnitOfWork()
    service = DeviceApplicationService(
        repository,
        instrument_type_repository,
        customer_repository,
        site_repository,
        uow,
    )

    device = service.create(
        CreateDeviceCommand(
            instrument_type_id=instrument_type.id,
            customer_id=customer.id,
            name="ВКТ-7",
            serial_number="SN-002",
        ),
    )

    assert device.instrument_type_id == instrument_type.id
    assert device.name == "ВКТ-7"
    assert device.serial_number.value == "SN-002"
    assert device.status == DeviceStatus.AVAILABLE
    assert repository.device.id == device.id
    assert uow.committed
    assert not uow.rolled_back


def test_device_create_fails_when_instrument_type_not_found():
    instrument_type_repository = FakeInstrumentTypeRepository(
        InstrumentType(
            id=uuid4(),
            name="Pressure gauge",
        ),
    )
    repository = FakeDeviceRepository(
        Device(
            id=uuid4(),
            instrument_type_id=uuid4(),
            customer_id=uuid4(),
            serial_number=SerialNumber("SN-001"),
        ),
    )
    customer = Customer(id=uuid4(), name="Test customer")
    customer_repository = FakeCustomerRepository(customer)
    site_repository = FakeSiteRepository()
    uow = FakeUnitOfWork()
    service = DeviceApplicationService(
        repository,
        instrument_type_repository,
        customer_repository,
        site_repository,
        uow,
    )

    with pytest.raises(InstrumentTypeNotFoundApplicationError):
        service.create(
            CreateDeviceCommand(
                instrument_type_id=uuid4(),
                customer_id=customer.id,
                name="ВКТ-7",
                serial_number="SN-002",
            ),
        )

    assert not uow.committed
    assert uow.rolled_back


def test_device_connect_disconnect_flow():
    device = Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        customer_id=uuid4(),
        serial_number=SerialNumber("SN-001"),
    )

    repository = FakeDeviceRepository(device)
    instrument_type_repository = FakeInstrumentTypeRepository(
        InstrumentType(
            id=device.instrument_type_id,
            name="Pressure gauge",
        ),
    )
    uow = FakeUnitOfWork()
    customer_repository = FakeCustomerRepository(
        Customer(id=device.customer_id, name="Test customer")
    )
    site_repository = FakeSiteRepository()
    service = DeviceApplicationService(
        repository,
        instrument_type_repository,
        customer_repository,
        site_repository,
        uow,
    )

    connected_device = service.connect(
        ConnectDeviceCommand(device_id=device.id),
    )

    assert connected_device.status == DeviceStatus.IN_WORK

    disconnected_device = service.disconnect(
        DisconnectDeviceCommand(device_id=device.id),
    )

    assert disconnected_device.status == DeviceStatus.COMPLETED
    assert uow.committed
    assert not uow.rolled_back


def test_device_create_fails_when_customer_not_found():
    instrument_type = InstrumentType(id=uuid4(), name="Pressure gauge")
    repository = FakeDeviceRepository(
        Device(
            id=uuid4(),
            instrument_type_id=instrument_type.id,
            customer_id=uuid4(),
            serial_number=SerialNumber("SN-001"),
        ),
    )
    instrument_type_repository = FakeInstrumentTypeRepository(instrument_type)
    customer_repository = FakeCustomerRepository(Customer(id=uuid4(), name="Other"))
    site_repository = FakeSiteRepository()
    uow = FakeUnitOfWork()
    service = DeviceApplicationService(
        repository,
        instrument_type_repository,
        customer_repository,
        site_repository,
        uow,
    )

    with pytest.raises(CustomerNotFoundApplicationError):
        service.create(
            CreateDeviceCommand(
                instrument_type_id=instrument_type.id,
                customer_id=uuid4(),
                name="ВКТ-7",
                serial_number="SN-002",
            ),
        )

    assert not uow.committed
    assert uow.rolled_back


def test_device_create_fails_when_site_not_found():
    customer = Customer(id=uuid4(), name="Test customer")
    instrument_type = InstrumentType(id=uuid4(), name="Pressure gauge")
    repository = FakeDeviceRepository(
        Device(
            id=uuid4(),
            instrument_type_id=instrument_type.id,
            customer_id=customer.id,
            serial_number=SerialNumber("SN-001"),
        ),
    )
    uow = FakeUnitOfWork()
    service = DeviceApplicationService(
        repository,
        FakeInstrumentTypeRepository(instrument_type),
        FakeCustomerRepository(customer),
        FakeSiteRepository(),
        uow,
    )

    with pytest.raises(SiteNotFoundApplicationError):
        service.create(
            CreateDeviceCommand(
                instrument_type_id=instrument_type.id,
                customer_id=customer.id,
                site_id=uuid4(),
                name="ВКТ-7",
                serial_number="SN-002",
            ),
        )

    assert not uow.committed
    assert uow.rolled_back


def test_device_create_fails_when_site_belongs_to_another_customer():
    customer = Customer(id=uuid4(), name="Test customer")
    other_customer_id = uuid4()
    site = Site(
        id=uuid4(),
        customer_id=other_customer_id,
        name="Other site",
        address="Other address",
    )
    instrument_type = InstrumentType(id=uuid4(), name="Pressure gauge")
    repository = FakeDeviceRepository(
        Device(
            id=uuid4(),
            instrument_type_id=instrument_type.id,
            customer_id=customer.id,
            serial_number=SerialNumber("SN-001"),
        ),
    )
    uow = FakeUnitOfWork()
    service = DeviceApplicationService(
        repository,
        FakeInstrumentTypeRepository(instrument_type),
        FakeCustomerRepository(customer),
        FakeSiteRepository(site),
        uow,
    )

    with pytest.raises(SiteCustomerMismatchApplicationError):
        service.create(
            CreateDeviceCommand(
                instrument_type_id=instrument_type.id,
                customer_id=customer.id,
                site_id=site.id,
                name="ВКТ-7",
                serial_number="SN-002",
            ),
        )

    assert not uow.committed
    assert uow.rolled_back


def test_device_create_rejects_duplicate_serial_for_same_customer_and_type():
    customer = Customer(id=uuid4(), name="Test customer")
    instrument_type = InstrumentType(id=uuid4(), name="Pressure gauge")
    existing = Device(
        id=uuid4(),
        instrument_type_id=instrument_type.id,
        customer_id=customer.id,
        serial_number=SerialNumber("SN-001"),
    )
    repository = FakeDeviceRepository(existing)
    uow = FakeUnitOfWork()
    service = DeviceApplicationService(
        repository,
        FakeInstrumentTypeRepository(instrument_type),
        FakeCustomerRepository(customer),
        FakeSiteRepository(),
        uow,
    )

    with pytest.raises(DuplicateDeviceSerialNumberApplicationError):
        service.create(
            CreateDeviceCommand(
                instrument_type_id=instrument_type.id,
                customer_id=customer.id,
                name="Other gauge",
                serial_number=" sn-001 ",
            ),
        )

    assert not uow.committed
    assert uow.rolled_back


def test_device_create_allows_same_serial_for_different_instrument_type():
    customer = Customer(id=uuid4(), name="Test customer")
    existing_type = InstrumentType(id=uuid4(), name="Flow meter")
    requested_type = InstrumentType(id=uuid4(), name="Pressure gauge")
    existing = Device(
        id=uuid4(),
        instrument_type_id=existing_type.id,
        customer_id=customer.id,
        serial_number=SerialNumber("SN-001"),
    )
    repository = FakeDeviceRepository(existing)
    uow = FakeUnitOfWork()
    service = DeviceApplicationService(
        repository,
        FakeInstrumentTypeRepository(requested_type),
        FakeCustomerRepository(customer),
        FakeSiteRepository(),
        uow,
    )

    created = service.create(
        CreateDeviceCommand(
            instrument_type_id=requested_type.id,
            customer_id=customer.id,
            name="Pressure gauge",
            serial_number="SN-001",
        ),
    )

    assert created.instrument_type_id == requested_type.id
    assert repository.device.id == created.id
    assert uow.committed
