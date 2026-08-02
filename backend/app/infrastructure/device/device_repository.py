"""
SQLAlchemy implementation of the DeviceRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
from app.infrastructure.mappers.device_mapper import DeviceMapper
from app.models.instrument import Instrument


class DeviceRepositorySQLAlchemy(DeviceRepository):
    """SQLAlchemy repository for Device."""

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db
        self._mapper = DeviceMapper()
        self._statuses: dict[UUID, object] = {}

    def get(
        self,
        device_id: UUID,
    ) -> Device | None:
        """Get device by identifier."""

        instrument = (
            self.db.query(Instrument).filter(Instrument.id == device_id).first()
        )

        if instrument is None:
            return None

        device = self._mapper.to_domain(instrument)

        if device.id in self._statuses:
            device.status = self._statuses[device.id]

        return device

    def save(
        self,
        device: Device,
    ) -> None:
        """Save device."""

        instrument = (
            self.db.query(Instrument).filter(Instrument.id == device.id).first()
        )

        if instrument is None:
            return

        self._mapper.to_model(
            device,
            instrument,
        )

        self.db.flush()
