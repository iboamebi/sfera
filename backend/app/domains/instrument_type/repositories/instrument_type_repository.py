"""
InstrumentType repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.instrument_type.entities.instrument_type import InstrumentType


class InstrumentTypeRepository(ABC):
    """Abstract instrument type repository."""

    @abstractmethod
    def get(
        self,
        instrument_type_id: UUID,
    ) -> InstrumentType | None:
        """Get instrument type by identifier."""

        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[InstrumentType]:
        """Get all instrument types."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        instrument_type: InstrumentType,
    ) -> InstrumentType:
        """Save instrument type."""

        raise NotImplementedError
