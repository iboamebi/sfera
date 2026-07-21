from collections import defaultdict
from collections.abc import Callable

from app.shared.events.domain_event import DomainEvent


class EventDispatcher:
    def __init__(self):
        self._handlers = defaultdict(list)

    def register(
        self,
        event_type: type[DomainEvent],
        handler: Callable,
    ):
        self._handlers[event_type].append(handler)

    def dispatch(
        self,
        event: DomainEvent,
    ):
        handlers = self._handlers[type(event)]

        for handler in handlers:
            handler(event)
