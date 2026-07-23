"""
Domain service for creating Device from Instrument.
"""

from app.domains.device.entities.device import Device
from app.infrastructure.mappers.device_mapper import DeviceMapper
from app.models.instrument import Instrument


class OrderDeviceService:
    """Creates a domain Device from an Instrument."""

    def __init__(self) -> None:
        self._mapper = DeviceMapper()

    def get_device(
        self,
        instrument: Instrument,
    ) -> Device:
        return self._mapper.to_domain(instrument)
