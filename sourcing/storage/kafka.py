from typing import Generator

from kafka import KafkaProducer, KafkaConsumer

from sourcing import Event, EventStorage
from sourcing.utils import serializer


class KafkaEventStorage(EventStorage):

    def __init__(self, topic, bootstrap_servers):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=serializer.serialize
        )

    def save(self, event):
        self.producer.send(self.topic, event)

    def read_events(self) -> Generator[Event, None, None]:
        yield from KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=serializer.deserialize
        )
