from uuid import UUID

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
from app.application.instrument_type.services.instrument_type_application_service import (  # noqa: E501
    InstrumentTypeApplicationService,
)
from app.domains.instrument_type.entities.instrument_type import InstrumentType
from app.domains.instrument_type.repositories.instrument_type_repository import (
    InstrumentTypeRepository,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeInstrumentTypeRepository(InstrumentTypeRepository):
    def __init__(self) -> None:
        self.instrument_types: dict[UUID, InstrumentType] = {}

    def get(
        self,
        instrument_type_id: UUID,
    ) -> InstrumentType | None:
        return self.instrument_types.get(instrument_type_id)

    def get_all(self) -> list[InstrumentType]:
        return list(self.instrument_types.values())

    def save(
        self,
        instrument_type: InstrumentType,
    ) -> InstrumentType:
        self.instrument_types[instrument_type.id] = instrument_type
        return instrument_type


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        self.commit_count += 1

    def rollback(self) -> None:
        self.rollback_count += 1


def test_instrument_type_application_lifecycle():
    repository = FakeInstrumentTypeRepository()
    uow = FakeUnitOfWork()
    service = InstrumentTypeApplicationService(repository, uow)

    instrument_type = service.create(
        CreateInstrumentTypeCommand(
            name="Pressure gauge",
            manufacturer="ACME",
            model="PG-100",
            measurement_type="Pressure",
            accuracy_class="0.5",
            verification_interval_months=12,
            description="Initial description",
        ),
    )

    assert instrument_type.id in repository.instrument_types
    assert instrument_type.name == "Pressure gauge"
    assert uow.commit_count == 1

    loaded = service.get(instrument_type.id)

    assert loaded == instrument_type

    updated = service.update(
        UpdateInstrumentTypeCommand(
            instrument_type_id=instrument_type.id,
            name="Digital pressure gauge",
            manufacturer="New ACME",
            model="PG-200",
            measurement_type="Pressure",
            accuracy_class="0.2",
            verification_interval_months=24,
            description="Updated description",
        ),
    )

    assert updated.name == "Digital pressure gauge"
    assert updated.manufacturer == "New ACME"
    assert updated.model == "PG-200"
    assert updated.accuracy_class == "0.2"
    assert updated.verification_interval_months == 24
    assert updated.description == "Updated description"
    assert uow.commit_count == 2

    archived = service.archive(
        ArchiveInstrumentTypeCommand(
            instrument_type_id=instrument_type.id,
        ),
    )

    assert archived.archived is True
    assert uow.commit_count == 3

    restored = service.restore(
        RestoreInstrumentTypeCommand(
            instrument_type_id=instrument_type.id,
        ),
    )

    assert restored.archived is False
    assert uow.commit_count == 4
