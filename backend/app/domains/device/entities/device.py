"""
Device domain entity.
"""

from dataclasses import dataclass
from uuid import UUID

from app.domains.device.exceptions import (
    DeviceNotAvailableDomainError,
    DeviceNotInWorkDomainError,
)
from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False, kw_only=True)
class Device(AggregateRoot):
    """Device aggregate representing an instrument card."""

    instrument_type_id: UUID
    serial_number: SerialNumber
    name: str | None = None
    registry_number: str | None = None
    modification: str | None = None
    manufacture_year: int | None = None
    inventory_number: str | None = None
    comment: str | None = None
    status: DeviceStatus = DeviceStatus.AVAILABLE

    def change_name(self, name: str) -> None:
        """Change the instrument card name."""

        self.name = name

    def connect(self) -> None:
        """Connect device to work."""

        if self.status != DeviceStatus.AVAILABLE:
            raise DeviceNotAvailableDomainError

        self.status = DeviceStatus.IN_WORK

    def disconnect(self) -> None:
        """Disconnect device from work."""

        if self.status != DeviceStatus.IN_WORK:
            raise DeviceNotInWorkDomainError

        self.status = DeviceStatus.COMPLETED
