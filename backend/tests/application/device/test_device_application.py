"""
Application service tests for Device.
"""

from uuid import uuid4

import pytest

from app.application.device.commands.create_device import CreateDeviceCommand
from app.application.device.exceptions import InstrumentTypeNotFoundApplicationError
from app.application.device.services.device_application_service import DeviceApplicationService
from app.domains.device.entities.device import Device
from app.domains.device.enums.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber
from app.domains.instrument_type.entities.instrument_type import InstrumentType


class FakeDeviceRepository:
    """In-memory Device repository for application tests."""

    def __init__(self, device: Device):
        self.device = device

    def add(self, device: Device) -> None:
        self.device = device


class FakeInstrumentTypeRepository:
    """In-memory InstrumentType repository for application tests."""

    def __init__(self, instrument_type: InstrumentType):
        self.instrument_type = instrument_type

    def get_by_id(self, instrument_type_id):
        if self.instrument_type.id == instrument_type_id:
            return self.instrument_type
        return None


class FakeUnitOfWork:
    """In-memory UnitOfWork for application tests."""

    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


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
            serial_number=SerialNumber("SN-001"),
        ),
    )
    uow = FakeUnitOfWork()
    service = DeviceApplicationService(
        repository,
        instrument_type_repository,
        uow,
    )

    device = service.create(
        CreateDeviceCommand(
            instrument_type_id=instrument_type.id,
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
            serial_number=SerialNumber("SN-001"),
        ),
    )
    uow = FakeUnitOfWork()
    service = DeviceApplicationService(
        repository,
        instrument_type_repository,
        uow,
    )

    with pytest.raises(InstrumentTypeNotFoundApplicationError):
        service.create(
            CreateDeviceCommand(
                instrument_type_id=uuid4(),
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
    service = DeviceApplicationService(
        repository,
        instrument_type_repository,
        uow,
    )

    service.connect(device.id)
    assert device.status == DeviceStatus.IN_SERVICE

    service.disconnect(device.id)
    assert device.status == DeviceStatus.AVAILABLE
