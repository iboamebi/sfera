from dataclasses import dataclass

from app.domains.device.value_objects.serial_number import SerialNumber
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False)
class Device(AggregateRoot):
    serial_number: SerialNumber
    connected: bool = False

    def connect(self) -> None:
        if self.connected:
            raise ValueError("Device is already connected")

        self.connected = True

    def disconnect(self) -> None:
        if not self.connected:
            raise ValueError("Device is not connected")

        self.connected = False
