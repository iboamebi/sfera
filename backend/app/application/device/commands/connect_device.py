from dataclasses import dataclass
from uuid import UUID

from app.application.device.services.device_service import DeviceService
from app.domains.device.events.device_connected import DeviceConnected


@dataclass(frozen=True)
class ConnectDeviceCommand:
    device_id: UUID


class ConnectDeviceHandler:
    def __init__(
        self,
        service: DeviceService,
    ) -> None:
        self._service = service

    def handle(
        self,
        command: ConnectDeviceCommand,
    ) -> DeviceConnected:
        device = self._service.connect(command.device_id)

        return DeviceConnected(
            device_id=str(device.id),
        )
