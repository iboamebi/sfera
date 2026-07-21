from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.device.entities.device import Device


class DeviceRepository(ABC):
    @abstractmethod
    def get(self, device_id: UUID) -> Device | None:
        pass

    @abstractmethod
    def save(self, device: Device) -> None:
        pass
