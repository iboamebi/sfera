from uuid import UUID

from app.domains.device.entities.device import Device
from app.domains.device.value_objects.serial_number import SerialNumber


class DeviceFactory:
    """Creates Device domain entities."""

    @staticmethod
    def create(
        device_id: UUID,
        instrument_type_id: UUID,
        customer_id: UUID,
        serial_number: str,
        name: str,
        site_id: UUID | None = None,
    ) -> Device:
        """Create an instrument card with its name."""

        return Device(
            id=device_id,
            instrument_type_id=instrument_type_id,
            customer_id=customer_id,
            site_id=site_id,
            serial_number=SerialNumber(serial_number),
            name=name,
        )
