from app.domains.device.entities.device import Device


class DeviceService:
    def connect(
        self,
        device: Device,
    ):
        device.connect()

    def disconnect(
        self,
        device: Device,
    ):
        device.disconnect()
