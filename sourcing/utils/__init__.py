from sourcing.utils.default import default
from sourcing.utils import serialize

serializer = serialize.JSON


def get_all_subclasses(cls, inclusive=False) -> list:
    all_subclasses = {cls, } if inclusive else set()
    for subclass in cls.__subclasses__():
        all_subclasses |= get_all_subclasses(subclass, inclusive=True)
    return all_subclasses
