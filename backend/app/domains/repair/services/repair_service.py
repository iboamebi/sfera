"""
Repair domain service.
"""

from app.domains.repair.entities.repair import Repair


class RepairService:
    """Contains repair business rules."""

    def start(
        self,
        repair: Repair,
    ) -> None:
        """Start repair."""

        repair.start()

    def wait(
        self,
        repair: Repair,
    ) -> None:
        """Put repair into waiting state."""

        repair.wait()

    def complete(
        self,
        repair: Repair,
        result: str,
    ) -> None:
        """Complete repair."""

        repair.complete(
            result,
        )

    def cancel(
        self,
        repair: Repair,
    ) -> None:
        """Cancel repair."""

        repair.cancel()
