"""
Connect device command.
"""

from dataclasses import dataclass
from uuid import UUID

from app.application.device.services.device_application_service import (
    DeviceApplicationService,
)


@dataclass(frozen=True)
class ConnectDeviceCommand:
    device_id: UUID


class ConnectDeviceHandler:
    """Connect device."""

    def __init__(
        self,
        service: DeviceApplicationService,
    ) -> None:
        self.service = service

    def handle(
        self,
        command: ConnectDeviceCommand,
    ):
        return self.service.connect(
            command.device_id,
        )
