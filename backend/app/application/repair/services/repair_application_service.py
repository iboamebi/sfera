"""
Application service for repair use cases.
"""

from uuid import UUID, uuid4

from app.application.repair.commands.create_repair import (
    CreateRepairCommand,
)
from app.application.repair.exceptions import (
    RepairNotFoundApplicationError,
)
from app.domains.repair.entities.repair import Repair
from app.domains.repair.repositories.repair_repository import (
    RepairRepository,
)
from app.domains.repair.services.repair_service import RepairService
from app.domains.repair.value_objects.repair_status import (
    RepairStatus,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class RepairApplicationService:
    """Coordinates repair use cases."""

    def __init__(
        self,
        repository: RepairRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = unit_of_work
        self._service = RepairService()

    def get(
        self,
        repair_id: UUID,
    ) -> Repair:
        repair = self._repository.get(
            repair_id,
        )

        if repair is None:
            raise RepairNotFoundApplicationError

        return repair

    def create(
        self,
        command: CreateRepairCommand,
    ) -> Repair:
        repair = Repair(
            id=uuid4(),
            order_item_id=command.order_item_id,
            status=RepairStatus.NEW,
            description=command.description,
        )

        with self._uow:
            self._repository.save(
                repair,
            )

        return repair

    def start(
        self,
        repair_id: UUID,
    ) -> Repair:
        with self._uow:
            repair = self.get(
                repair_id,
            )

            self._service.start(
                repair,
            )

            self._repository.save(
                repair,
            )

        return repair

    def complete(
        self,
        repair_id: UUID,
        result: str,
    ) -> Repair:
        with self._uow:
            repair = self.get(
                repair_id,
            )

            self._service.complete(
                repair,
                result,
            )

            self._repository.save(
                repair,
            )

        return repair

    def cancel(
        self,
        repair_id: UUID,
    ) -> Repair:
        with self._uow:
            repair = self.get(
                repair_id,
            )

            self._service.cancel(
                repair,
            )

            self._repository.save(
                repair,
            )

        return repair
