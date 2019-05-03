import json

import msgpack

from sourcing.utils.default import default


class MsgPack:
    @staticmethod
    def deserialize(value):
        if not isinstance(value, bytes):
            value = bytes.fromhex(value)
        return msgpack.unpackb(value, raw=False)

    @staticmethod
    def serialize(value):
        return msgpack.packb(value, default=default, use_bin_type=True).hex


class JSON:
    @staticmethod
    def deserialize(value):
        return json.loads(value)

    @staticmethod
    def serialize(value):
        return json.dumps(value, default=default)
