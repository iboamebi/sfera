from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.device.entities.device import Device


class DeviceRepository(ABC):
    @abstractmethod
    def get(self, device_id: UUID) -> Device | None:
        pass

    @abstractmethod
    def list(self) -> list[Device]:
        pass

    @abstractmethod
    def exists_by_customer_type_and_serial_number(
        self,
        customer_id: UUID,
        instrument_type_id: UUID,
        serial_number: str,
        exclude_device_id: UUID | None = None,
    ) -> bool:
        pass

    @abstractmethod
    def save(self, device: Device) -> None:
        pass
