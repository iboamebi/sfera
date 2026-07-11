from dataclasses import dataclass

from app.domains.device.entities.device import Device
from app.domains.device.events.device_connected import DeviceConnected


@dataclass(frozen=True)
class ConnectDeviceCommand:
    device: Device


class ConnectDeviceHandler:

    def handle(
        self,
        command: ConnectDeviceCommand,
    ) -> DeviceConnected:

        command.device.connect()

        return DeviceConnected(
            device_id=str(command.device.id)
        )
