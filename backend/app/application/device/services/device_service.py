"""
Application service for Device.
"""

from uuid import UUID

from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.device.services.device_domain_service import (
    DeviceDomainService,
)


class DeviceService:
    """
    Coordinates Device use cases.
    """

    def __init__(
        self,
        repository: DeviceRepository,
    ) -> None:
        self._repository = repository
        self._domain_service = DeviceDomainService()

    def connect(
        self,
        device_id: UUID,
    ) -> Device:
        device = self._repository.get(device_id)

        if device is None:
            raise ValueError("Device not found")

        self._domain_service.connect(device)
        self._repository.save(device)

        return device

    def disconnect(
        self,
        device_id: UUID,
    ) -> Device:
        device = self._repository.get(device_id)

        if device is None:
            raise ValueError("Device not found")

        self._domain_service.disconnect(device)
        self._repository.save(device)

        return device
