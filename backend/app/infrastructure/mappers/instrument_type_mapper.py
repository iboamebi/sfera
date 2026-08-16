"""
InstrumentType domain/model mapper.
"""

from app.domains.instrument_type.entities.instrument_type import InstrumentType
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.instrument_type import InstrumentType as InstrumentTypeModel


class InstrumentTypeMapper(
    BaseMapper[
        InstrumentType,
        InstrumentTypeModel,
    ],
):
    """Maps InstrumentType between domain and SQLAlchemy model."""

    def to_domain(
        self,
        model: InstrumentTypeModel,
    ) -> InstrumentType:
        """Convert ORM model to domain entity."""

        return InstrumentType(
            id=model.id,
            name=model.name,
            manufacturer=model.manufacturer,
            model=model.model,
            measurement_type=model.measurement_type,
            accuracy_class=model.accuracy_class,
            verification_interval_months=model.verification_interval_months,
            description=model.description,
            archived=model.archived,
        )

    def to_model(
        self,
        entity: InstrumentType,
        model: InstrumentTypeModel,
    ) -> InstrumentTypeModel:
        """Convert domain entity to ORM model."""

        model.name = entity.name
        model.manufacturer = entity.manufacturer
        model.model = entity.model
        model.measurement_type = entity.measurement_type
        model.accuracy_class = entity.accuracy_class
        model.verification_interval_months = entity.verification_interval_months
        model.description = entity.description
        model.archived = entity.archived

        return model
