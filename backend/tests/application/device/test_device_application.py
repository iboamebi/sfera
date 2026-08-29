from uuid import UUID, uuid4

import pytest

from app.application.device.commands.connect_device import ConnectDeviceCommand
from app.application.device.commands.create_device import CreateDeviceCommand
from app.application.device.commands.disconnect_device import DisconnectDeviceCommand
from app.application.device.exceptions import (
    InstrumentTypeNotFoundApplicationError,
)
from app.application.device.services.device_application_service import (
    DeviceApplicationService,
)
from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber
from app.domains.instrument_type.entities.instrument_type import InstrumentType
from app.domains.instrument_type.repositories.instrument_type_repository import (
    InstrumentTypeRepository,
)
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
            serial_number="SN-002",
        ),
    )

    assert device.instrument_type_id == instrument_type.id
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
