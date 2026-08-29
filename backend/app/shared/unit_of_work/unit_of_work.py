"""
Unit of Work abstraction.
"""

from abc import ABC, abstractmethod
from uuid import UUID


class UnitOfWork(ABC):
    """Transaction boundary abstraction."""

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self) -> None:
        """Commit transaction."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Rollback transaction."""
        pass

    @abstractmethod
    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        """Register aggregate and its operation correlation metadata."""
        pass
