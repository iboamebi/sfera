from uuid import uuid4

from app.domains.device.entities.device import Device
from app.domains.device.value_objects.serial_number import SerialNumber


def test_device_name_is_part_of_instrument_card() -> None:
    """Store the individual instrument name on the device."""

    device = Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        serial_number=SerialNumber("SN-001"),
        name="ВКТ-7",
    )

    assert device.name == "ВКТ-7"


def test_device_name_can_be_changed() -> None:
    """Change the individual instrument name through domain behavior."""

    device = Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        serial_number=SerialNumber("SN-001"),
        name="Старое имя",
    )

    device.change_name("ВКТ-7")

    assert device.name == "ВКТ-7"
