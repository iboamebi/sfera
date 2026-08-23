"""
SQLAlchemy Unit of Work implementation.
"""

from sqlalchemy.orm import Session

from app.shared.unit_of_work.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    """Transaction boundary for SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
        self._aggregates: list[object] = []

    def commit(self) -> None:
        """Commit transaction."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback transaction."""
        self.session.rollback()

    def register_aggregate(self, aggregate: object) -> None:
        """Register aggregate for domain event collection."""
        self._aggregates.append(aggregate)

        def __enter__(self):
        return self
