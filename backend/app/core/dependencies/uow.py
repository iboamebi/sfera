"""
Unit of Work dependency providers.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies.database import get_session
from app.infrastructure.database.unit_of_work import (
    SqlAlchemyUnitOfWork,
)


def get_unit_of_work(
    session: Session = Depends(get_session),
) -> SqlAlchemyUnitOfWork:
    """Provide SQLAlchemy Unit of Work."""

    return SqlAlchemyUnitOfWork(session)
