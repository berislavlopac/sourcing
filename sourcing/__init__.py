import json
from datetime import datetime, timezone
from typing import Generator

from ciso8601 import parse_datetime

from sourcing.reactors import get_registered
from sourcing.utils import default


class Event:

    def __init__(self, event_type: str, data: dict, timestamp: datetime=None):
        if timestamp is None:
            timestamp = datetime.utcnow().astimezone(timezone.utc)
        self.type = event_type
        self.data = data
        self.timestamp = timestamp

    @property
    def serialized_data(self) -> str:
        return json.dumps(self.data, default=default)

    def serialize(self):
        return {
            'type': self.type,
            'timestamp': self.timestamp.isoformat(),
            'data': self.serialized_data
        }

    @classmethod
    def from_serialized(cls, serialized: dict):
        if isinstance(serialized['timestamp'], str):
            serialized['timestamp'] = parse_datetime(serialized['timestamp'])
        return cls(
            event_type=serialized['type'],
            timestamp=serialized['timestamp'],
            data=json.loads(serialized['data'])
        )


class EventStorage:

    def save(self, event: Event):
        raise NotImplementedError

    def read_events(self) -> Generator[Event, None, None]:
        raise NotImplementedError


def source_event(event_type: str, data: dict, storage: EventStorage, timestamp: datetime=None):
    event = Event(event_type, data, timestamp)
    storage.save(event)
    for reactor_class in get_registered(event_type):
        reactor_class(event).execute()
