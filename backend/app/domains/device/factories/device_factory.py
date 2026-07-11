from app.domains.device.entities.device import Device
from app.domains.device.value_objects.serial_number import SerialNumber
from app.models.instrument import Instrument


class DeviceFactory:

    @staticmethod
    def from_instrument(
        instrument: Instrument,
    ) -> Device:

        return Device(
            id=instrument.id,
            serial_number=SerialNumber(
                instrument.serial_number
            ),
        )
