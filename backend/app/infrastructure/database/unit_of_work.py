"""
SQLAlchemy Unit of Work implementation.
"""

from sqlalchemy.orm import Session

from app.shared.events.domain_event import DomainEvent
from app.shared.events.event_dispatcher import EventDispatcher
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    """Transaction boundary for SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self.session = session
        self._event_dispatcher = event_dispatcher
        self._aggregates: list[object] = []

    def commit(self) -> None:
        """Commit transaction and dispatch collected domain events."""
        self.session.commit()

        for aggregate in self._aggregates:
            events = aggregate.collect_events()

            for event in events:
                if isinstance(event, DomainEvent):
                    self._event_dispatcher.dispatch(event)

    def rollback(self) -> None:
        """Rollback transaction."""
        self.session.rollback()

    def register_aggregate(self, aggregate: object) -> None:
        """Register aggregate for domain event collection."""
        self._aggregates.append(aggregate)

    def __enter__(self):
        return self
