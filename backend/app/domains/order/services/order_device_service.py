from app.domains.device.entities.device import Device
from app.domains.device.factories.device_factory import DeviceFactory
from app.models.instrument import Instrument


class OrderDeviceService:

    def get_device(
        self,
        instrument: Instrument,
    ) -> Device:

        return DeviceFactory.from_instrument(
            instrument
        )
