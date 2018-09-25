from time import time
from typing import Generator

from sourcing.reactors import get_registered
from sourcing.utils import default


class Event:

    def __init__(self, event_type: str, data: dict, timestamp: float=None):
        self.type = event_type
        self.data = data
        self.timestamp = timestamp or time()

    def as_dict(self):
        return {
            'type': self.type,
            'timestamp': self.timestamp,
            'data': self.data
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            event_type=data['type'],
            timestamp=data['timestamp'],
            data=data['data']
        )

    def react(self):
        for reactor_class in get_registered(self.type):
            reactor_class(self).execute()


class EventStorage:

    def save(self, event: Event):
        raise NotImplementedError

    def read_events(self) -> Generator[Event, None, None]:
        raise NotImplementedError


def source_event(storage: EventStorage, event_type: str, data: dict, timestamp: float = None):
    event = Event(event_type, data, timestamp=timestamp)
    storage.save(event)
    return event
