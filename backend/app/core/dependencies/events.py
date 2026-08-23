from functools import lru_cache

from app.shared.events.event_dispatcher import EventDispatcher


@lru_cache
def get_event_dispatcher() -> EventDispatcher:
    return EventDispatcher()
