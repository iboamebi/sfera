from dataclasses import dataclass

from app.domains.device.entities.device import Device
from app.domains.device.events.device_disconnected import DeviceDisconnected


@dataclass(frozen=True)
class DisconnectDeviceCommand:
    device: Device


class DisconnectDeviceHandler:

    def handle(
        self,
        command: DisconnectDeviceCommand,
    ) -> DeviceDisconnected:

        command.device.disconnect()

        return DeviceDisconnected(
            device_id=str(command.device.id)
        )
