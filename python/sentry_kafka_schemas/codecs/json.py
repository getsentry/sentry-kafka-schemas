from __future__ import annotations

from typing import Any, TypeVar, cast

import fastjsonschema
import rapidjson

from sentry_kafka_schemas.codecs import Codec, ValidationError

T = TypeVar("T")


class JsonCodec(Codec[T]):
    def __init__(
        self,
        json_schema: object,
    ) -> None:
        self.__validate = fastjsonschema.compile(json_schema)

    def encode(self, data: T, validate: bool) -> bytes:
        if validate:
            self.validate(data)
        return cast(bytes, rapidjson.dumps(data).encode("utf-8"))

    def decode(self, raw_data: bytes, validate: bool) -> Any:
        decoded = rapidjson.loads(raw_data)
        if validate:
            self.validate(decoded)
        return decoded

    def validate(self, data: T) -> None:
        try:
            self.__validate(data)
        except Exception as exc:
            raise ValidationError from exc
