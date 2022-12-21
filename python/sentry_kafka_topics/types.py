from typing import Any, Literal, Mapping, Optional, Sequence, TypedDict, Union

__all__ = ["TopicConfig", "Schema"]

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
    "Schema", {"type": Union[Literal["json"]], "schema": Union[JsonSchema]}
)

TopicConfig = TypedDict(
    "TopicConfig",
    {"topic_creation_config": Mapping[str, Any], "schema": Optional[Schema]},
)
