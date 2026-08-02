"""
Application service for Device.
"""

from uuid import UUID

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
from app.domains.device.repositories.device_repository import (
    DeviceRepository,
)


class DeviceApplicationService:
    """Coordinates Device use cases."""

    def __init__(
        self,
        repository: DeviceRepository,
    ) -> None:
        self._repository = repository

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
        device_id: UUID,
    ) -> Device:
        """Connect device."""

        device = self.get(device_id)

        try:
            device.connect()

        except DeviceNotAvailableDomainError:
            raise DeviceNotAvailableApplicationError from None

        self._repository.save(device)

        return device

    def disconnect(
        self,
        device_id: UUID,
    ) -> Device:
        """Disconnect device."""

        device = self.get(device_id)

        try:
            device.disconnect()

        except DeviceNotInWorkDomainError:
            raise DeviceNotInWorkApplicationError from None

        self._repository.save(device)

        return device
