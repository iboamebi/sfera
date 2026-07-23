"""
Device mapper.
"""

from app.domains.device.entities.device import Device
from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.instrument import Instrument


class DeviceMapper(BaseMapper[Device, Instrument]):
    """Maps Instrument <-> Device."""

    def to_domain(
        self,
        model: Instrument,
    ) -> Device:
        return Device(
            id=model.id,
            serial_number=SerialNumber(model.serial_number),
            status=DeviceStatus.AVAILABLE,
        )

    def to_model(
        self,
        entity: Device,
        model: Instrument,
    ) -> Instrument:
        model.serial_number = entity.serial_number.value
        return model
