from dataclasses import dataclass
from uuid import UUID

from app.application.device.services.device_service import DeviceService
from app.domains.device.events.device_disconnected import DeviceDisconnected


@dataclass(frozen=True)
class DisconnectDeviceCommand:
    device_id: UUID


class DisconnectDeviceHandler:
    def __init__(
        self,
        service: DeviceService,
    ) -> None:
        self._service = service

    def handle(
        self,
        command: DisconnectDeviceCommand,
    ) -> DeviceDisconnected:
        device = self._service.disconnect(command.device_id)

        return DeviceDisconnected(
            device_id=str(device.id),
        )
