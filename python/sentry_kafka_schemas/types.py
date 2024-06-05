import dataclasses
from pathlib import Path
from typing import Any, Literal, Mapping, Sequence, TypedDict, Union

import msgpack
import rapidjson

__all__ = ["Schema"]

JsonSchema = TypedDict(
    "JsonSchema",
    {
        "$schema": str,
        "title": str,
        "description": str,
        "type": str,
        "properties": Mapping[str, Any],
        "required": Sequence[str],
        "additionalProperties": bool,
    },
    total=False,
)

Schema = TypedDict(
    "Schema",
    {
        "version": int,
        "type": Literal["json", "msgpack"],
        "compatibility_mode": Union[Literal["none"], Literal["backward"]],
        "schema": Union[JsonSchema],
        "schema_filepath": str,
        "examples": Sequence[str],
    },
)


@dataclasses.dataclass(frozen=True)
class Example:
    path: Path
    type: Literal["json", "msgpack"]

    _examples_basepath: Path

    def __repr__(self) -> str:
        relpath = str(self.path)[len(str(self._examples_basepath)) :]
        return f"<Example path=...{relpath}>"

    def load(self) -> Any:
        with open(self.path, "rb") as f:
            if self.type == "json":
                return rapidjson.load(f)
            elif self.type == "msgpack":
                return msgpack.unpackb(f.read())
