from uuid import uuid4

from app.domains.order.services.order_device_service import (
    OrderDeviceService,
)
from app.models.instrument import Instrument


def test_order_device_service():
    instrument = Instrument(
        id=uuid4(),
        instrument_type_id=uuid4(),
        serial_number="SN-100",
    )

    device = OrderDeviceService().get_device(instrument)

    assert device.id == instrument.id
    assert device.serial_number.value == "SN-100"
