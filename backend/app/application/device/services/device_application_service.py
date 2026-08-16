"""
Application service for Device.
"""

from uuid import UUID, uuid4

from app.application.device.commands.connect_device import ConnectDeviceCommand
from app.application.device.commands.create_device import CreateDeviceCommand
from app.application.device.commands.disconnect_device import DisconnectDeviceCommand
from app.application.device.exceptions import (
    DeviceNotAvailableApplicationError,
    DeviceNotFoundApplicationError,
    DeviceNotInWorkApplicationError,
)
from app.domains.device.entities.device import Device
from app.domains.device.exceptions import (
    DeviceNotAvailableDomainError,
    DeviceNotInWorkDomainError,
)
from app.domains.device.factories.device_factory import DeviceFactory
from app.domains.device.repositories.device_repository import DeviceRepository


class DeviceApplicationService:
    """Coordinates Device use cases."""

    def __init__(
        self,
        repository: DeviceRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        command: CreateDeviceCommand,
    ) -> Device:
        """Create device."""

        device = DeviceFactory.create(
            device_id=uuid4(),
            instrument_type_id=command.instrument_type_id,
            serial_number=command.serial_number,
        )

        self._repository.save(device)

        return device

    def get(
        self,
        device_id: UUID,
    ) -> Device:
        """Get device."""

        device = self._repository.get(device_id)

        if device is None:
            raise DeviceNotFoundApplicationError

        return device

    def connect(
        self,
        command: ConnectDeviceCommand,
    ) -> Device:
        """Connect device."""

        device = self.get(command.device_id)

        try:
            device.connect()

        except DeviceNotAvailableDomainError:
            raise DeviceNotAvailableApplicationError from None

        self._repository.save(device)

        return device

    def disconnect(
        self,
        command: DisconnectDeviceCommand,
    ) -> Device:
        """Disconnect device."""

        device = self.get(command.device_id)

        try:
            device.disconnect()

        except DeviceNotInWorkDomainError:
            raise DeviceNotInWorkApplicationError from None

        self._repository.save(device)

        return device
