from uuid import uuid4

from app.shared.base.aggregate import AggregateRoot


class TestEvent:
    pass


def test_collect_events_returns_added_events_and_clears_collection():
    aggregate = AggregateRoot(id=uuid4())

    event = TestEvent()

    aggregate.add_event(event)

    assert aggregate.collect_events() == [event]
    assert aggregate.collect_events() == []


def test_collect_events_preserves_order():
    aggregate = AggregateRoot(id=uuid4())

    first = TestEvent()
    second = TestEvent()

    aggregate.add_event(first)
    aggregate.add_event(second)

    assert aggregate.collect_events() == [first, second]
