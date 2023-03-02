from typing import Any, Literal, Mapping, Sequence, TypedDict, Union

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
    },
)
