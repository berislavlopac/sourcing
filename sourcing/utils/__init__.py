from datetime import date, time
from functools import singledispatch


def get_all_subclasses(cls, inclusive=False) -> list:
    all_subclasses = {cls, } if inclusive else set()
    for subclass in cls.__subclasses__():
        all_subclasses |= get_all_subclasses(subclass, inclusive=True)
    return all_subclasses


@singledispatch
def default(value):
    return str(value)


@default.register(date)
def default_datetime(value):
    return value.isoformat()


@default.register(time)
def default_datetime(value):
    return value.isoformat()
