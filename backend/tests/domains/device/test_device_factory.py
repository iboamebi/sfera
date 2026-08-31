from uuid import uuid4

from app.domains.device.factories.device_factory import DeviceFactory


def test_device_factory_create():
    device_id = uuid4()
    instrument_type_id = uuid4()

    device = DeviceFactory.create(
        device_id=device_id,
        instrument_type_id=instrument_type_id,
        name="ВКТ-7",
        serial_number="SN-001",
    )

    assert device.id == device_id
    assert device.instrument_type_id == instrument_type_id
    assert device.name == "ВКТ-7"
    assert device.serial_number.value == "SN-001"
