from typing import Optional, TypeVar, cast

import fastjsonschema
import msgpack
from sentry_kafka_schemas.codecs import Codec, ValidationError

T = TypeVar("T")


class MsgpackCodec(Codec[T]):
    """
    This codec assumes the payload is json.
    """

    def __init__(self, json_schema: Optional[object]) -> None:
        if json_schema is not None:
            self.__validate = fastjsonschema.compile(json_schema)
        else:
            self.__validate = lambda _: None

    def encode(self, data: T, validate: bool = True) -> bytes:
        if validate:
            self.validate(data)
        return cast(bytes, msgpack.packb(data))

    def decode(self, raw_data: bytes, validate: bool = True) -> T:
        decoded = msgpack.unpackb(raw_data)
        if validate:
            self.validate(decoded)
        return cast(T, decoded)

    def validate(self, data: T) -> None:
        try:
            self.__validate(data)
        except Exception as exc:
            raise ValidationError from exc
