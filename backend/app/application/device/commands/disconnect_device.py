"""
Disconnect device command.
"""

from dataclasses import dataclass
from uuid import UUID

from app.application.device.services.device_application_service import (
    DeviceApplicationService,
)


@dataclass(frozen=True)
class DisconnectDeviceCommand:
    device_id: UUID


class DisconnectDeviceHandler:
    """Disconnect device."""

    def __init__(
        self,
        service: DeviceApplicationService,
    ) -> None:
        self.service = service

    def handle(
        self,
        command: DisconnectDeviceCommand,
    ):
        return self.service.disconnect(
            command.device_id,
        )
