from dataclasses import dataclass

from app.domains.device.entities.device import Device
from app.domains.device.events.device_disconnected import DeviceDisconnected
from app.domains.device.services.device_service import DeviceService


@dataclass(frozen=True)
class DisconnectDeviceCommand:
    device: Device


class DisconnectDeviceHandler:

    def handle(
        self,
        command: DisconnectDeviceCommand,
    ) -> DeviceDisconnected:

#        command.device.disconnect()
        DeviceService().disconnect(
            command.device
        )

        return DeviceDisconnected(
            device_id=str(command.device.id)
        )
