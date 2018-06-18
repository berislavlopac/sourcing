from collections import defaultdict
from typing import Type

DEFAULT_EVENT_TYPE = '__all_events__'

_reactor_registry = defaultdict(set)


class Reactor:
    is_active = True

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

    def execute(self):
        raise NotImplementedError


def register(reactor: Type[Reactor], event_type: str=DEFAULT_EVENT_TYPE):
    if not issubclass(reactor, Reactor):
        raise TypeError('The class {} is not a subclass of Reactor.')
    _reactor_registry[event_type].add(reactor)


def get_registered(event_type: str=None) -> set:
    reactors = set(_reactor_registry[DEFAULT_EVENT_TYPE])
    if event_type is not None:
        reactors |= _reactor_registry[event_type]
    return reactors


def reset_registered():
    global _reactor_registry
    _reactor_registry = defaultdict(set)
