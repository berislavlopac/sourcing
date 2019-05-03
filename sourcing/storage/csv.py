import csv
from pathlib import Path
from typing import Generator

from sourcing import Event, EventStorage


class CSVEventStorage(EventStorage):
    _fields = ["type", "timestamp", "data"]

    def __init__(self, path, **writer_specs):
        self.path = Path(path)
        self._writer_specs = writer_specs

    def save(self, event):
        with open(self.path, "a") as csv_file:
            writer = csv.DictWriter(csv_file, self._fields, **self._writer_specs)
            writer.writerow(event.as_dict())

    def read_events(self) -> Generator[Event, None, None]:
        with open(self.path) as csv_file:
            for event_data in csv.DictReader(csv_file, fieldnames=self._fields):
                event_data["timestamp"] = float(event_data["timestamp"])
                yield Event.from_dict(event_data)
