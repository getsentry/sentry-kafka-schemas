from typing import Any, Literal, Mapping, Sequence, TypedDict, Union

import rapidjson
import dataclasses
from pathlib import Path

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
        "type": Union[Literal["json"]],
        "compatibility_mode": Union[Literal["none"], Literal["backward"]],
        "schema": Union[JsonSchema],
        "schema_filepath": str,
        "examples": Sequence[str],
    },
)


@dataclasses.dataclass(frozen=True)
class Example:
    path: Path

    _examples_basepath: Path

    def __repr__(self) -> str:
        relpath = str(self.path)[len(str(self._examples_basepath)) :]
        return f"<Example path=...{relpath}>"

    def load(self) -> Any:
        with open(self.path) as f:
            return rapidjson.load(f)
