"""
Application service for InstrumentType.
"""

from uuid import UUID, uuid4

from app.application.instrument_type.commands.archive_instrument_type import (
    ArchiveInstrumentTypeCommand,
)
from app.application.instrument_type.commands.create_instrument_type import (
    CreateInstrumentTypeCommand,
)
from app.application.instrument_type.commands.restore_instrument_type import (
    RestoreInstrumentTypeCommand,
)
from app.application.instrument_type.commands.update_instrument_type import (
    UpdateInstrumentTypeCommand,
)
from app.application.instrument_type.exceptions import (
    InstrumentTypeNotFoundApplicationError,
)
from app.domains.instrument_type.entities.instrument_type import InstrumentType
from app.domains.instrument_type.repositories.instrument_type_repository import (
    InstrumentTypeRepository,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class InstrumentTypeApplicationService:
    """Coordinates InstrumentType use cases."""

    def __init__(
        self,
        repository: InstrumentTypeRepository,
        uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = uow

    def create(
        self,
        command: CreateInstrumentTypeCommand,
    ) -> InstrumentType:
        """Create instrument type."""

        instrument_type = InstrumentType(
            id=uuid4(),
            name=command.name,
            manufacturer=command.manufacturer,
            model=command.model,
            measurement_type=command.measurement_type,
            accuracy_class=command.accuracy_class,
            verification_interval_months=command.verification_interval_months,
            description=command.description,
        )

        result = self._repository.save(instrument_type)
        self._uow.commit()
        return result

    def get(
        self,
        instrument_type_id: UUID,
    ) -> InstrumentType:
        """Get instrument type by identifier."""

        instrument_type = self._repository.get(instrument_type_id)

        if instrument_type is None:
            raise InstrumentTypeNotFoundApplicationError

        return instrument_type

    def get_all(self) -> list[InstrumentType]:
        """Get all instrument types."""

        return self._repository.get_all()

    def update(
        self,
        command: UpdateInstrumentTypeCommand,
    ) -> InstrumentType:
        """Update instrument type."""

        instrument_type = self.get(command.instrument_type_id)

        if command.name is not None:
            instrument_type.change_name(command.name)

        if command.manufacturer is not None:
            instrument_type.change_manufacturer(command.manufacturer)

        if command.model is not None:
            instrument_type.change_model(command.model)

        if command.measurement_type is not None:
            instrument_type.change_measurement_type(command.measurement_type)

        if command.accuracy_class is not None:
            instrument_type.change_accuracy_class(command.accuracy_class)

        if command.verification_interval_months is not None:
            instrument_type.change_verification_interval_months(
                command.verification_interval_months,
            )

        if command.description is not None:
            instrument_type.change_description(command.description)

        result = self._repository.save(instrument_type)
        self._uow.commit()
        return result

    def archive(
        self,
        command: ArchiveInstrumentTypeCommand,
    ) -> InstrumentType:
        """Archive instrument type."""

        instrument_type = self.get(command.instrument_type_id)

        instrument_type.archive()

        result = self._repository.save(instrument_type)
        self._uow.commit()
        return result

    def restore(
        self,
        command: RestoreInstrumentTypeCommand,
    ) -> InstrumentType:
        """Restore instrument type."""

        instrument_type = self.get(command.instrument_type_id)

        instrument_type.restore()

        result = self._repository.save(instrument_type)
        self._uow.commit()
        return result
