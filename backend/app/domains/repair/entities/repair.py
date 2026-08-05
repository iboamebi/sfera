"""
Repair domain entity.
"""

from dataclasses import dataclass
from uuid import UUID

from app.domains.repair.value_objects.repair_status import (
    RepairStatus,
)
from app.shared.base.entity import Entity


@dataclass(eq=False)
class Repair(Entity):
    """Represents repair process."""

    order_item_id: UUID
    status: RepairStatus = RepairStatus.NEW
    description: str | None = None
    result: str | None = None

    def start(self) -> None:
        """Start repair."""

        self.status = RepairStatus.IN_WORK

    def wait(self) -> None:
        """Put repair into waiting state."""

        self.status = RepairStatus.WAITING

    def complete(
        self,
        result: str,
    ) -> None:
        """Complete repair."""

        self.status = RepairStatus.COMPLETED
        self.result = result

    def cancel(self) -> None:
        """Cancel repair."""

        self.status = RepairStatus.CANCELLED
