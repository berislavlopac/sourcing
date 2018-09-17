from datetime import date, time
from functools import singledispatch


@singledispatch
def default(value):
    return str(value)


@default.register(date)
def default_datetime(value):
    return value.isoformat()


@default.register(time)
def default_datetime(value):
    return value.isoformat()
