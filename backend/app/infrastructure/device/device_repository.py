from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
#from app.domains.device.value_objects.serial_number import SerialNumber
from app.domains.device.factories.device_factory import DeviceFactory

from app.models.instrument import Instrument


class DeviceRepositorySQLAlchemy(DeviceRepository):

    def __init__(self, db: Session):
        self.db = db
        self._statuses = {}

    def get(self, device_id: UUID) -> Device | None:
        instrument = (
            self.db.query(Instrument)
            .filter(Instrument.id == device_id)
            .first()
        )

        if not instrument:
            return None

        device = DeviceFactory.from_instrument(
            instrument
        )

        if device.id in self._statuses:
            device.status = self._statuses[device.id]

        return device

    def save(self, device: Device) -> None:
        instrument = (
            self.db.query(Instrument)
            .filter(Instrument.id == device.id)
            .first()
        )

        if not instrument:
            raise ValueError(
                "Instrument not found"
            )

        instrument.serial_number = (
            device.serial_number.value
        )

        self.db.commit()
