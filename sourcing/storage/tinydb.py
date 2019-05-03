from typing import Generator

from tinydb import TinyDB

from sourcing import Event, EventStorage


class TinyDBEventStorage(EventStorage):
    def __init__(self, path):
        self.db = TinyDB(path)

    def save(self, event: Event):
        self.db.insert(event.as_dict())

    def read_events(self) -> Generator[Event, None, None]:
        for event_data in self.db.all():
            yield Event.from_dict(event_data)
