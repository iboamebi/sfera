"""
SQLAlchemy implementation of InstrumentTypeRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.instrument_type.entities.instrument_type import InstrumentType
from app.domains.instrument_type.repositories.instrument_type_repository import (
    InstrumentTypeRepository,
)
from app.infrastructure.mappers.instrument_type_mapper import InstrumentTypeMapper
from app.models.instrument_type import InstrumentType as InstrumentTypeModel


class InstrumentTypeRepositorySQLAlchemy(InstrumentTypeRepository):
    """SQLAlchemy repository for InstrumentType."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._mapper = InstrumentTypeMapper()

    def get(
        self,
        instrument_type_id: UUID,
    ) -> InstrumentType | None:
        model = (
            self._session.query(InstrumentTypeModel)
            .filter(
                InstrumentTypeModel.id == instrument_type_id,
            )
            .first()
        )

        if model is None:
            return None

        return self._mapper.to_domain(model)

    def get_all(self) -> list[InstrumentType]:
        models = self._session.query(InstrumentTypeModel).all()

        return [self._mapper.to_domain(model) for model in models]

    def save(
        self,
        instrument_type: InstrumentType,
    ) -> InstrumentType:
        model = (
            self._session.query(InstrumentTypeModel)
            .filter(
                InstrumentTypeModel.id == instrument_type.id,
            )
            .first()
        )

        if model is None:
            model = InstrumentTypeModel(
                id=instrument_type.id,
            )
            self._session.add(model)

        self._mapper.to_model(
            instrument_type,
            model,
        )

        self._session.flush()

        return self._mapper.to_domain(model)
