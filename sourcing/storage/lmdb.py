import json
from typing import Generator

import lmdb

from sourcing import Event, EventStorage
from sourcing.utils import default


class LMDBEventStorage(EventStorage):

    def __init__(self, path: str, db_name=None, **kwargs):
        self.db_name = db_name
        self.env = lmdb.open(str(path), **kwargs)

    def save(self, event: Event):
        with self.env.begin(db=self.db_name, write=True) as transaction:
            transaction.put(
                key=str(event.timestamp).encode(),
                value=json.dumps(event.as_dict(), default=default).encode()
            )

    def read_events(self) -> Generator[Event, None, None]:
        with self.env.begin(db=self.db_name) as transaction:
            yield from (
                Event.from_dict(json.loads(data.decode()))
                for timestamp, data in transaction.cursor()
            )
