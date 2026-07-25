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

    def commit(self) -> None:
        """Commit transaction."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback transaction."""
        self.session.rollback()

    def __enter__(self):
        return self
