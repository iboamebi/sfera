"""
SQLAlchemy Unit of Work implementation.
"""

from dataclasses import replace
from uuid import UUID

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
        self._aggregates: list[tuple[object, UUID | None]] = []

    def commit(self) -> None:
        """Commit transaction and dispatch collected domain events."""
        self.session.commit()

        for aggregate, operation_id in self._aggregates:
            events = aggregate.collect_events()

            for event in events:
                if isinstance(event, DomainEvent):
                    if operation_id is not None:
                        event = replace(event, operation_id=operation_id)

                    self._event_dispatcher.dispatch(event)

    def rollback(self) -> None:
        """Rollback transaction."""
        self.session.rollback()

    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        """Register aggregate for domain event collection."""
        self._aggregates.append((aggregate, operation_id))

    def __enter__(self):
        return self
