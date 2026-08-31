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
        status = DeviceStatus.AVAILABLE

        if model.device_status:
            try:
                status = DeviceStatus(model.device_status)
            except ValueError:
                status = DeviceStatus.AVAILABLE

        return Device(
            id=model.id,
            instrument_type_id=model.instrument_type_id,
            name=model.name,
            serial_number=SerialNumber(model.serial_number),
            registry_number=model.registry_number,
            modification=model.modification,
            manufacture_year=model.manufacture_year,
            inventory_number=model.inventory_number,
            comment=model.comment,
            status=status,
        )

    def to_model(
        self,
        entity: Device,
        model: Instrument,
    ) -> Instrument:
        model.instrument_type_id = entity.instrument_type_id
        model.name = entity.name
        model.serial_number = entity.serial_number.value
        model.device_status = entity.status.value
        model.registry_number = entity.registry_number
        model.modification = entity.modification
        model.manufacture_year = entity.manufacture_year
        model.inventory_number = entity.inventory_number
        model.comment = entity.comment

        return model
