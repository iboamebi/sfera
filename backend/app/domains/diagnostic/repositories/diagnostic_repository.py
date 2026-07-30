"""
Diagnostic repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.diagnostic.entities.diagnostic import Diagnostic


class DiagnosticRepository(ABC):
    """Repository contract for diagnostics."""

    @abstractmethod
    def get(
        self,
        diagnostic_id: UUID,
    ) -> Diagnostic | None:
        """Get diagnostic by id."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        diagnostic: Diagnostic,
    ) -> None:
        """Save diagnostic."""

        raise NotImplementedError
