"""
SQLAlchemy implementation of the DeviceRepository.
"""

from uuid import UUID

from sqlalchemy import func
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

    def get(
        self,
        device_id: UUID,
    ) -> Device | None:
        """Get device by identifier."""

        instrument = (
            self.db.query(Instrument)
            .filter(
                Instrument.id == device_id,
            )
            .first()
        )

        if instrument is None:
            return None

        return self._mapper.to_domain(instrument)

    def list(self) -> list[Device]:
        """List devices."""

        instruments = self.db.query(Instrument).all()
        return [self._mapper.to_domain(instrument) for instrument in instruments]

    def exists_by_customer_type_and_serial_number(
        self,
        customer_id: UUID,
        instrument_type_id: UUID,
        serial_number: str,
        exclude_device_id: UUID | None = None,
    ) -> bool:
        """Check serial uniqueness within customer and instrument type."""
        query = self.db.query(Instrument.id).filter(
            Instrument.customer_id == customer_id,
            Instrument.instrument_type_id == instrument_type_id,
            func.lower(func.btrim(Instrument.serial_number))
            == serial_number.strip().lower(),
        )
        if exclude_device_id is not None:
            query = query.filter(Instrument.id != exclude_device_id)
        return query.first() is not None

    def save(
        self,
        device: Device,
    ) -> None:
        """Save device."""

        instrument = (
            self.db.query(Instrument)
            .filter(
                Instrument.id == device.id,
            )
            .first()
        )

        if instrument is None:
            instrument = Instrument(
                id=device.id,
            )
            self.db.add(instrument)

        self._mapper.to_model(
            device,
            instrument,
        )

        self.db.flush()
