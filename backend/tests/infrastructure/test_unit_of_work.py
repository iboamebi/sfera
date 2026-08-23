from unittest.mock import Mock

from app.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from app.shared.events.domain_event import DomainEvent


def test_commit_dispatches_aggregate_events():
    session = Mock()
    dispatcher = Mock()

    aggregate = Mock()
    event = DomainEvent()
    aggregate.collect_events.return_value = [event]

    uow = SqlAlchemyUnitOfWork(session, dispatcher)
    uow.register_aggregate(aggregate)

    uow.commit()

    session.commit.assert_called_once_with()
    aggregate.collect_events.assert_called_once_with()
    dispatcher.dispatch.assert_called_once_with(event)
