from uuid import uuid4

from app.application.device.commands.connect_device import ConnectDeviceCommand
from app.application.device.commands.create_device import CreateDeviceCommand
from app.application.device.commands.disconnect_device import DisconnectDeviceCommand
from app.application.device.services.device_application_service import (
    DeviceApplicationService,
)
from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber


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

    def save(
        self,
        device,
    ):
        self.device = device


def test_device_create():
    repository = FakeDeviceRepository(
        Device(
            id=uuid4(),
            instrument_type_id=uuid4(),
            serial_number=SerialNumber("SN-001"),
        ),
    )
    service = DeviceApplicationService(repository)

    instrument_type_id = uuid4()

    device = service.create(
        CreateDeviceCommand(
            instrument_type_id=instrument_type_id,
            serial_number="SN-002",
        ),
    )

    assert device.instrument_type_id == instrument_type_id
    assert device.serial_number.value == "SN-002"
    assert device.status == DeviceStatus.AVAILABLE
    assert repository.device.id == device.id


def test_device_connect_disconnect_flow():
    device = Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        serial_number=SerialNumber("SN-001"),
    )

    repository = FakeDeviceRepository(device)
    service = DeviceApplicationService(repository)

    connected_device = service.connect(
        ConnectDeviceCommand(device_id=device.id),
    )

    assert connected_device.status == DeviceStatus.IN_WORK

    disconnected_device = service.disconnect(
        DisconnectDeviceCommand(device_id=device.id),
    )

    assert disconnected_device.status == DeviceStatus.COMPLETED
