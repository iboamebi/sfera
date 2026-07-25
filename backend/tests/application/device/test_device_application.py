from uuid import uuid4

from app.application.device.commands.connect_device import (
    ConnectDeviceCommand,
    ConnectDeviceHandler,
)
from app.application.device.commands.disconnect_device import (
    DisconnectDeviceCommand,
    DisconnectDeviceHandler,
)
from app.application.device.services.device_service import DeviceService
from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber


class FakeDeviceRepository(DeviceRepository):
    def __init__(self, device: Device):
        self.device = device

    def get(self, device_id):
        if device_id == self.device.id:
            return self.device
        return None

    def save(self, device):
        self.device = device


def test_device_connect_disconnect_flow():
    device = Device(
        id=uuid4(),
        serial_number=SerialNumber("SN-001"),
    )

    repository = FakeDeviceRepository(device)
    service = DeviceService(repository)

    connected_event = ConnectDeviceHandler(service).handle(
        ConnectDeviceCommand(device.id),
    )

    assert device.status == DeviceStatus.IN_WORK
    assert connected_event.device_id == str(device.id)

    disconnected_event = DisconnectDeviceHandler(service).handle(
        DisconnectDeviceCommand(device.id),
    )

    assert device.status == DeviceStatus.COMPLETED
    assert disconnected_event.device_id == str(device.id)
