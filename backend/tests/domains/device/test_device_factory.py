from uuid import uuid4

from app.domains.device.factories.device_factory import DeviceFactory
from app.models.instrument import Instrument


def test_device_factory_from_instrument():

    instrument = Instrument(
        id=uuid4(),
        instrument_type_id=uuid4(),
        serial_number="SN-001",
    )

    device = DeviceFactory.from_instrument(
        instrument
    )

    assert device.id == instrument.id
    assert device.serial_number.value == "SN-001"
