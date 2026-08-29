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
    """Device aggregate."""

    instrument_type_id: UUID
    serial_number: SerialNumber
    status: DeviceStatus = DeviceStatus.AVAILABLE
    registry_number: str | None = None
    modification: str | None = None
    factory_number: str | None = None
    manufacture_year: int | None = None
    inventory_number: str | None = None
    comment: str | None = None

    def update_details(
        self,
        *,
        instrument_type_id: UUID | None = None,
        serial_number: str | None = None,
        registry_number: str | None = None,
        modification: str | None = None,
        factory_number: str | None = None,
        manufacture_year: int | None = None,
        inventory_number: str | None = None,
        comment: str | None = None,
    ) -> None:
        """Update supplied device card details."""

        if instrument_type_id is not None:
            self.instrument_type_id = instrument_type_id
        if serial_number is not None:
            self.serial_number = SerialNumber(serial_number)
        if registry_number is not None:
            self.registry_number = registry_number
        if modification is not None:
            self.modification = modification
        if factory_number is not None:
            self.factory_number = factory_number
        if manufacture_year is not None:
            self.manufacture_year = manufacture_year
        if inventory_number is not None:
            self.inventory_number = inventory_number
        if comment is not None:
            self.comment = comment

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
