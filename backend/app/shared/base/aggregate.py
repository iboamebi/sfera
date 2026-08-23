from .entity import Entity


class AggregateRoot(Entity):
    """Base class for aggregates with domain event collection."""

    def add_event(self, event: object) -> None:
        if not hasattr(self, "_events"):
            self._events: list[object] = []

        self._events.append(event)

    def collect_events(self) -> list[object]:
        if not hasattr(self, "_events"):
            self._events: list[object] = []

        events = list(self._events)
        self._events.clear()
        return events
