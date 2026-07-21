from dataclasses import dataclass

from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False)
class Device(AggregateRoot):
    serial_number: SerialNumber
    status: DeviceStatus = DeviceStatus.AVAILABLE

    def connect(self) -> None:
        if self.status != DeviceStatus.AVAILABLE:
            raise ValueError("Device is not available")

        self.status = DeviceStatus.IN_WORK

    def disconnect(self) -> None:
        if self.status != DeviceStatus.IN_WORK:
            raise ValueError("Device is not in work")

        self.status = DeviceStatus.COMPLETED
