import os

import rapidjson
from typing import (
    Iterable,
    Optional,
    MutableMapping,
    Sequence,
    Tuple,
    TypedDict,
    cast,
    Union,
    Literal,
)
from sentry_kafka_schemas.types import Schema, Example
from pathlib import Path
from yaml import safe_load

__TOPIC_TO_SCHEMA: MutableMapping[Tuple[str, Optional[int]], Optional[Schema]] = {}


class SchemaNotFound(Exception):
    pass


TopicSchema = TypedDict(
    "TopicSchema",
    {
        "topic": str,
        "version": int,
        "type": Union[Literal["json"]],
        "compatibility_mode": Union[Literal["none"], Literal["backward"]],
        "resource": str,
        "examples": Sequence[str],
    },
)

TopicData = TypedDict("TopicData", {"version": int, "schemas": Sequence[TopicSchema]})

_TOPICS_PATH = Path.joinpath(Path(__file__).parent, "topics")
_SCHEMAS_PATH = Path.joinpath(Path(__file__).parent, "schemas")
_EXAMPLES_PATH = Path.joinpath(Path(__file__).parent, "examples")


def _list_topics() -> Iterable[str]:
    """
    List all defined topic names.

    This is not yet stable API, just internally used by code generation.
    """
    for file in os.listdir(_TOPICS_PATH):
        assert file.endswith(".yaml")
        yield file[: -len(".yaml")]


def _get_topic(topic: str) -> TopicData:
    """
    Get metadata for a specific topic name.

    This is not yet stable API, just internally used by code generation.
    """
    topic_path = Path.joinpath(_TOPICS_PATH, f"{topic}.yaml")

    try:
        with open(topic_path) as f:
            topic_data = cast(TopicData, safe_load(f))
    except FileNotFoundError:
        raise SchemaNotFound

    return topic_data


def get_schema(topic: str, version: Optional[int] = None) -> Schema:
    """
    Returns the schema for a topic. If version is passed, return the schema for
    the specified version, otherwise the latest version is returned.

    If a matching schema can't be found, raise SchemaNotFound.

    Only JSON schemas are currently supported.
    """
    schema_key = (topic, version)

    if schema_key not in __TOPIC_TO_SCHEMA:
        try:
            topic_data = _get_topic(topic)

            topic_schemas = sorted(topic_data["schemas"], key=lambda x: x["version"])

            schema_metadata = None
            if version is None:
                schema_metadata = topic_schemas[-1]
            else:
                for s in topic_schemas:
                    if s["version"] == version:
                        schema_metadata = s
                        break

                if schema_metadata is None:
                    raise SchemaNotFound("Invalid version")

        except SchemaNotFound:
            __TOPIC_TO_SCHEMA[schema_key] = None
            raise

        resource_path = Path.joinpath(_SCHEMAS_PATH, schema_metadata["resource"])
        with open(resource_path) as f:
            json_schema = rapidjson.load(f)
        schema: Schema = {
            "version": schema_metadata["version"],
            "type": schema_metadata["type"],
            "compatibility_mode": schema_metadata["compatibility_mode"],
            "schema": json_schema,
            "schema_filepath": str(resource_path),
            "examples": schema_metadata["examples"],
        }

        __TOPIC_TO_SCHEMA[schema_key] = schema
        return schema

    elif __TOPIC_TO_SCHEMA[schema_key] is None:
        raise SchemaNotFound

    cached_schema = __TOPIC_TO_SCHEMA[schema_key]
    assert cached_schema is not None
    return cached_schema


def iter_examples(topic: str, version: Optional[int] = None) -> Iterable[Example]:
    """
    Yield filepaths to all example payloads for a specific schema version, or
    the latest version if no version is provided.

    Parameters are the same as for `get_schema`. If a matching schema can't be
    found, raise `SchemaNotFound`.

    This is currently a separate function, not a method on a Schema class,
    because we might want to split out examples from this package at some point.
    """
    schema = get_schema(topic, version)

    for example_entry in schema["examples"]:
        example_path = Path.joinpath(_EXAMPLES_PATH, example_entry)
        if os.path.isfile(example_path):
            yield Example(
                _examples_basepath=_EXAMPLES_PATH,
                path=example_path,
            )
        else:
            for example_subpath in os.listdir(example_path):
                yield Example(
                    _examples_basepath=_EXAMPLES_PATH,
                    path=Path.joinpath(example_path, example_subpath),
                )
