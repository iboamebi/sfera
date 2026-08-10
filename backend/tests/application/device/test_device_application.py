from uuid import uuid4

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


def test_device_connect_disconnect_flow():
    device = Device(
        id=uuid4(),
        serial_number=SerialNumber("SN-001"),
    )

    repository = FakeDeviceRepository(device)
    service = DeviceApplicationService(repository)

    connected_device = service.connect(
        device.id,
    )

    assert connected_device.status == DeviceStatus.IN_WORK

    disconnected_device = service.disconnect(
        device.id,
    )

    assert disconnected_device.status == DeviceStatus.COMPLETED
