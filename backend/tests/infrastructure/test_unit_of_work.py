from datetime import UTC, datetime
from unittest.mock import Mock
from uuid import uuid4

from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.events.order_registered import OrderRegistered
from app.domains.order.value_objects.order_number import OrderNumber
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


def test_commit_correlates_events_with_operation_id():
    session = Mock()
    dispatcher = Mock()

    aggregate = Mock()
    event = DomainEvent()
    aggregate.collect_events.return_value = [event]
    operation_id = uuid4()

    uow = SqlAlchemyUnitOfWork(session, dispatcher)
    uow.register_aggregate(aggregate, operation_id)

    uow.commit()

    dispatched_event = dispatcher.dispatch.call_args.args[0]

    assert dispatched_event.event_id == event.event_id
    assert dispatched_event.occurred_at == event.occurred_at
    assert dispatched_event.operation_id == operation_id


def test_commit_dispatches_order_registered_event():
    session = Mock()
    dispatcher = Mock()
    order = Order.create(
        id=uuid4(),
        number=OrderNumber("10011"),
        customer_id=uuid4(),
        received_at=datetime(2026, 8, 31, 15, 30, tzinfo=UTC),
    )
    order.add_item(OrderItem(id=uuid4()))
    order.register()

    uow = SqlAlchemyUnitOfWork(session, dispatcher)
    uow.register_aggregate(order)

    uow.commit()

    dispatched_event = dispatcher.dispatch.call_args.args[0]

    assert isinstance(dispatched_event, OrderRegistered)
    assert dispatched_event.order_id == order.id
