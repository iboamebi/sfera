from uuid import UUID

from app.domains.device.entities.device import Device
from app.domains.device.value_objects.serial_number import SerialNumber


class DeviceFactory:
    @staticmethod
    def create(
        device_id: UUID,
        serial_number: str,
    ) -> Device:
        return Device(
            id=device_id,
            serial_number=SerialNumber(serial_number),
        )
