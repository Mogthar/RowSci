import enum
from typing import Callable


class Event(enum.Enum):
    CORTEX_DATA_LOADED = "CORTEX_DATA_LOADED"
    PADDLE_DATA_LOADED = "PADDLE_DATA_LOADED"
    POWERLINE_DATA_LOADED = "POWERLINE_DATA_LOADED"
    ARTINIS_DATA_LOADED = "ARTINIS_DATA_LOADED"

class EventManager:
    def __init__(self):
        self.events = {}

    def register_event_listener(self, event: Event, listener: Callable):
        if event not in self.events:
            self.events[event] = []
        self.events[event].append(listener)

    def unregister_event_listener(self, event: Event, listener: Callable):
        if event in self.events:
            self.events[event].remove(listener)

    def trigger_event(self, event: Event):
        if event in self.events:
            for listener in self.events[event]:
                listener()

event_manager = EventManager()

