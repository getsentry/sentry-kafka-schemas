from __future__ import annotations

from typing import Any, Optional, TypeVar, cast

import fastjsonschema
import rapidjson
from sentry_kafka_schemas.codecs import Codec, ValidationError

T = TypeVar("T")


class JsonCodec(Codec[T]):
    def __init__(
        self,
        json_schema: Optional[object],
    ) -> None:
        if json_schema is not None:
            self.__validate = fastjsonschema.compile(json_schema)
        else:
            self.__validate = lambda _: None

    def encode(self, data: T, validate: bool = True) -> bytes:
        if validate:
            self.validate(data)
        return cast(bytes, rapidjson.dumps(data).encode("utf-8"))

    def decode(self, raw_data: bytes, validate: bool = True) -> Any:
        decoded = rapidjson.loads(raw_data)
        if validate:
            self.validate(decoded)
        return decoded

    def validate(self, data: T) -> None:
        try:
            self.__validate(data)
        except Exception as exc:
            raise ValidationError from exc
