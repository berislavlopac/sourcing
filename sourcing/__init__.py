import json
from time import time
from typing import Generator

from sourcing.reactors import get_registered
from sourcing.utils import default


class Event:

    def __init__(self, event_type: str, data: dict, timestamp: float=None):
        self.type = event_type
        self.data = data
        self.timestamp = timestamp or time()

    @property
    def serialized_data(self) -> str:
        return json.dumps(self.data, default=default)

    def as_dict(self):
        return {
            'type': self.type,
            'timestamp': self.timestamp,
            'data': self.serialized_data
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            event_type=data['type'],
            timestamp=data['timestamp'],
            data=json.loads(data['data'])
        )


class EventStorage:

    def save(self, event: Event):
        raise NotImplementedError

    def read_events(self) -> Generator[Event, None, None]:
        raise NotImplementedError


def source_event(event_type: str, data: dict, storage: EventStorage, timestamp: float=None):
    event = Event(event_type, data, timestamp)
    storage.save(event)
    for reactor_class in get_registered(event_type):
        reactor_class(event).execute()
