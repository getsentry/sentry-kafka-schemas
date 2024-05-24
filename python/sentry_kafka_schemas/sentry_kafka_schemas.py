from __future__ import annotations

import os

import rapidjson
from typing import (
    Any,
    Iterable,
    Optional,
    MutableMapping,
    Sequence,
    Tuple,
    TypedDict,
    cast,
    Literal,
    Mapping,
)
from typing_extensions import NotRequired

from sentry_kafka_schemas.types import Schema, Example
from sentry_kafka_schemas.codecs import Codec
from sentry_kafka_schemas.codecs.json import JsonCodec
from sentry_kafka_schemas.codecs.msgpack import MsgpackCodec
from pathlib import Path
from yaml import safe_load

__TOPIC_TO_CODEC: MutableMapping[Tuple[str, Optional[int]], Optional[Codec[Any]]] = {}


class SchemaNotFound(Exception):
    pass


class TopicSchema(TypedDict):
    version: int
    type: Literal["json", "msgpack"]
    compatibility_mode: Literal["none", "backward"]
    resource: str
    examples: Sequence[str]


class ServicesData(TypedDict):
    consumers: Sequence[str]
    producers: Sequence[str]


class TopicData(TypedDict):
    topic: str
    description: str
    services: ServicesData
    schemas: Sequence[TopicSchema]
    pipeline: NotRequired[str]
    topic_creation_config: Mapping[str, str]
    partitions: Optional[int]


_TOPICS_PATH = Path.joinpath(Path(__file__).parent, "topics")
_SCHEMAS_PATH = Path.joinpath(Path(__file__).parent, "schemas")
_EXAMPLES_PATH = Path.joinpath(Path(__file__).parent, "examples")


def list_topics() -> Iterable[str]:
    """
    List all defined topic names.
    """
    for file in os.listdir(_TOPICS_PATH):
        assert file.endswith(".yaml")
        yield file[: -len(".yaml")]


def get_topic(topic: str) -> TopicData:
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
    if "topic_creation_config" not in topic_data:
        topic_data["topic_creation_config"] = {}

    if "partitions" not in topic_data:
        topic_data["partitions"] = None

    return topic_data


def _get_schema(topic: str, version: Optional[int] = None) -> Schema:
    """
    Returns the schema for a topic. If version is passed, return the schema for
    the specified version, otherwise the latest version is returned.

    If a matching schema can't be found, raise SchemaNotFound.

    Only JSON schemas are currently supported.
    """
    topic_data = get_topic(topic)

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

    return schema


def get_codec(topic: str, version: Optional[int] = None) -> Codec[Any]:
    cache_key = (topic, version)
    if cache_key in __TOPIC_TO_CODEC:
        cache_value = __TOPIC_TO_CODEC[cache_key]
        if cache_value is None:
            raise SchemaNotFound
        return cache_value

    try:
        schema = _get_schema(topic, version=version)
    except SchemaNotFound:
        __TOPIC_TO_CODEC[cache_key] = None
        raise

    rv: Codec[Any]
    if schema["type"] == "json":
        rv = JsonCodec(json_schema=schema["schema"])
    elif schema["type"] == "msgpack":
        rv = MsgpackCodec(json_schema=schema["schema"])
    else:
        raise ValueError(schema["type"])
    __TOPIC_TO_CODEC[cache_key] = rv
    return rv


def iter_examples(topic: str, version: Optional[int] = None) -> Iterable[Example]:
    """
    Yield filepaths to all example payloads for a specific schema version, or
    the latest version if no version is provided.

    Parameters are the same as for `get_schema`. If a matching schema can't be
    found, raise `SchemaNotFound`.

    This is currently a separate function, not a method on a Schema class,
    because we might want to split out examples from this package at some point.
    """
    schema = _get_schema(topic, version)

    for example_entry in schema["examples"]:
        example_path = Path.joinpath(_EXAMPLES_PATH, example_entry)
        if os.path.isfile(example_path):
            yield Example(
                _examples_basepath=_EXAMPLES_PATH,
                path=example_path,
                type=schema["type"],
            )
        else:
            for example_subpath in os.listdir(example_path):
                yield Example(
                    _examples_basepath=_EXAMPLES_PATH,
                    path=Path.joinpath(example_path, example_subpath),
                    type=schema["type"],
                )
