"""
Unit of Work dependency providers.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies.database import get_session
from app.core.dependencies.events import get_event_dispatcher
from app.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from app.shared.events.event_dispatcher import EventDispatcher
from app.shared.unit_of_work.unit_of_work import UnitOfWork


def get_unit_of_work(
    session: Session = Depends(get_session),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
) -> UnitOfWork:
    """Provide SQLAlchemy Unit of Work."""

    return SqlAlchemyUnitOfWork(session, event_dispatcher)
