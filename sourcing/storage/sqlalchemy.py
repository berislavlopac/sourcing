from typing import Generator

from sqlalchemy import Column, String, Float, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

from sourcing import Event, EventStorage
from sourcing.utils import serializer

Base = declarative_base()


class EventModel(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    timestamp = Column(Float)
    type = Column(String(256))
    data = Column(Text)

    def as_dict(self):
        data = vars(self)
        data['data'] = serializer.deserialize(self.data)
        return data


class SQLAlchemyEventStorage(EventStorage):

    def __init__(self, db_session):
        self.session = db_session

    def save(self, event: Event):
        event_instance = EventModel(
            timestamp=event.timestamp,
            type=event.type,
            data=serializer.serialize(event.data)
        )
        self.session.add(event_instance)
        self.session.commit()

    def read_events(self) -> Generator[Event, None, None]:
        for event_model in self.session.query(EventModel):
            yield Event.from_dict(event_model.as_dict())
