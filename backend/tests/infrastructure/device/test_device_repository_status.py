from uuid import uuid4

from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.entities.device import Device
from app.domains.device.value_objects.serial_number import SerialNumber


def test_device_status_lifecycle():

    device = Device(
        id=uuid4(),
        serial_number=SerialNumber("SN-001"),
    )

    device.connect()

    assert device.status == DeviceStatus.IN_WORK

    device.disconnect()

    assert device.status == DeviceStatus.COMPLETED
