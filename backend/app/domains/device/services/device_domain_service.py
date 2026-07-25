"""
Domain service for device business operations.
"""

from app.domains.device.entities.device import Device


class DeviceDomainService:
    """
    Domain service for device state transitions.
    """

    def connect(
        self,
        device: Device,
    ) -> None:
        device.connect()

    def disconnect(
        self,
        device: Device,
    ) -> None:
        device.disconnect()
