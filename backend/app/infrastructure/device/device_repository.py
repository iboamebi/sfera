from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.device.value_objects.serial_number import SerialNumber

from app.models.instrument import Instrument


class DeviceRepositorySQLAlchemy(DeviceRepository):

    def __init__(self, db: Session):
        self.db = db

    def get(self, device_id: UUID) -> Device | None:
        instrument = (
            self.db.query(Instrument)
            .filter(Instrument.id == device_id)
            .first()
        )

        if not instrument:
            return None

        return Device(
            id=instrument.id,
            serial_number=SerialNumber(
                instrument.serial_number
            ),
        )

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
