from __future__ import annotations

import pathlib
from typing import Any, Optional, TypeVar, cast

import fastjsonschema
import rapidjson
from sentry_kafka_schemas.codecs import Codec, ValidationError

T = TypeVar("T")

BASE_DIR = pathlib.Path(__file__).parent.parent / "schemas"


def file_handler(uri: str) -> Any:
    absolute_path = BASE_DIR / uri[7:]
    if not absolute_path.exists():
        raise FileNotFoundError(f"Schema file not found: {absolute_path}")
    with open(absolute_path) as f:
        return rapidjson.load(f)


class JsonCodec(Codec[T]):
    def __init__(
        self,
        json_schema: Optional[object],
    ) -> None:
        if json_schema is not None:
            self.__validate = fastjsonschema.compile(json_schema, handlers={"file": file_handler})
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
