"""
Device domain entity.
"""

from dataclasses import dataclass

from app.domains.device.exceptions import (
    DeviceNotAvailableDomainError,
    DeviceNotInWorkDomainError,
)
from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False)
class Device(AggregateRoot):
    """Device aggregate."""

    serial_number: SerialNumber
    status: DeviceStatus = DeviceStatus.AVAILABLE

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
