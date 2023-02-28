import os
import rapidjson
from typing import Optional, MutableMapping
from sentry_kafka_schemas.types import Schema
from pathlib import Path
from yaml import safe_load

__TOPIC_TO_SCHEMA: MutableMapping[str, Optional[Schema]] = {}


class SchemaNotFound(Exception):
    pass


def get_schema(topic: str, version: Optional[int] = None) -> Schema:
    """
    Returns the schema for a topic. If version is passed, return the schema for
    the specified version, otherwise the latest version is returned.

    If a matching schema can't be found, raise SchemaNotFound.

    Only JSON schemas are currently supported.
    """

    if topic not in __TOPIC_TO_SCHEMA:
        topic_path = Path.joinpath(Path(__file__).parent, "topics", f"{topic}.yaml")

        try:
            with open(topic_path) as f:
                topic_data = safe_load(f)

                # TODO: Actually respect the version number
                schema_metadata = topic_data["schemas"][-1]

        except FileNotFoundError:
            __TOPIC_TO_SCHEMA[topic] = None
            raise SchemaNotFound

        resource_path = Path.joinpath(Path(__file__).parent, "schemas", schema_metadata["resource"])
        with open(resource_path) as f:
            json_schema = rapidjson.load(f)
        schema: Schema = {
            "version": schema_metadata["version"],
            "type": schema_metadata["type"],
            "compatibility_mode": schema_metadata["compatibility_mode"],
            "schema": json_schema,
        }

        __TOPIC_TO_SCHEMA[topic] = schema
        return schema

    elif __TOPIC_TO_SCHEMA[topic] is None:
        raise SchemaNotFound

    cached_schema = __TOPIC_TO_SCHEMA[topic]
    assert cached_schema is not None
    return cached_schema
