from uuid import uuid4

from app.application.device.commands.connect_device import (
    ConnectDeviceCommand,
    ConnectDeviceHandler,
)

from app.application.device.commands.disconnect_device import (
    DisconnectDeviceCommand,
    DisconnectDeviceHandler,
)

from app.domains.device.entities.device import Device
from app.domains.device.value_objects.serial_number import SerialNumber
from app.domains.device.value_objects.device_status import DeviceStatus


def test_device_connect_disconnect_flow():

    device = Device(
        id=uuid4(),
        serial_number=SerialNumber("SN-001"),
    )

    connected_event = ConnectDeviceHandler().handle(
        ConnectDeviceCommand(device)
    )

#    assert device.connected is True
    assert device.status == DeviceStatus.IN_WORK
    assert connected_event.device_id == str(device.id)

    disconnected_event = DisconnectDeviceHandler().handle(
        DisconnectDeviceCommand(device)
    )

#    assert device.connected is False
    assert device.status == DeviceStatus.COMPLETED
    assert disconnected_event.device_id == str(device.id)
