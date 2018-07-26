from sourcing import Event, EventStorage, source_event
from sourcing.reactors import register, Reactor

foo_aggregate = []


class FooReactor(Reactor):

    def execute(self):
        if self.event.type == 'foo':
            foo_aggregate.append(self.event.serialized_data)


class ListEventStorage(EventStorage):

    def __init__(self):
        self.events = []

    def save(self, event: Event):
        self.events.append(event)

    def read_events(self):
        yield from self.events


def test_source_event():
    register(FooReactor)
    events = [
        ('foo', {'a': 'b'}),
        ('bar', {1: 'c'}),
        ('foo', {'d': 12.34})
    ]
    storage = ListEventStorage()
    for event_type, event_data in events:
        source_event(event_type=event_type, data=event_data, storage=storage)

    timestamp = 0
    for index, event in enumerate(storage.read_events()):
        assert isinstance(event, Event)
        assert (event.type, event.data) == events[index]
        assert event.timestamp >= timestamp
        timestamp = event.timestamp

    assert foo_aggregate == [
        '{"a": "b"}',
        '{"d": 12.34}'
    ]
