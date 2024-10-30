import re
from typing import Any, Iterator, Tuple

import pytest
from sentry_kafka_schemas.sentry_kafka_schemas import _get_schema, get_topic, list_topics
from sentry_kafka_schemas.types import is_json_schema, is_protobuf_schema


def get_all_json_schemas() -> Iterator[Tuple[str, int]]:
    for topic in list_topics():
        for schema_raw in get_topic(topic)["schemas"]:
            if schema_raw["type"] not in ("json", "msgpack"):
                continue
            version = schema_raw["version"]
            yield topic, version


def get_all_protobuf_schemas() -> Iterator[Tuple[str, int]]:
    for topic in list_topics():
        for schema_raw in get_topic(topic)["schemas"]:
            if schema_raw["type"] != "protobuf":
                continue
            version = schema_raw["version"]
            yield topic, version


_VALID_DEFINITION_NAMES = re.compile(r"^[A-Z]([a-zA-Z0-9]+)$")
_VALID_TITLE_NAMES = re.compile(r"^[a-z][a-z0-9_]+$")


@pytest.mark.parametrize("topic,version", get_all_protobuf_schemas())
def test_protobuf_schemas_valid(topic: str, version: int) -> None:
    schema_meta = _get_schema(topic, version=version)

    assert is_protobuf_schema(schema_meta["schema"])
    assert schema_meta["type"] == "protobuf"
    assert schema_meta["schema"]
    assert schema_meta["schema"]["resource"]
    assert schema_meta["schema_filepath"]


@pytest.mark.parametrize("topic,version", get_all_json_schemas())
def test_json_schemas_valid(topic: str, version: int) -> None:
    schema_meta = _get_schema(topic, version=version)
    assert schema_meta["type"] in {"json", "msgpack"}

    schema = schema_meta["schema"]
    assert is_json_schema(schema)
    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"

    used_titles = set()

    def _validate_title(obj: Any) -> None:
        if not isinstance(obj, dict):
            return

        if "title" in obj:
            title = obj["title"]
            assert _VALID_TITLE_NAMES.match(title), f"{title} is not snake_case"

            if title in used_titles:
                raise AssertionError(f"{title} duplicated")

            used_titles.add(title)

        if (
            "properties" in obj
            or "additionalProperites" in obj
            or "patternProperties" in obj
            or "required" in obj
        ) and "object" not in obj.get("type", ()):
            # Impose restriction so that types will be good:
            # https://github.com/sbrunner/jsonschema-gentypes/issues/469
            raise AssertionError(
                "type=object needs to be specified explicitly on all schemas, if properties are defined"
            )

        for value in obj.get("properties", {}).values():
            _validate_title(value)

        if isinstance(obj.get("items"), list):
            for value in obj["items"]:
                _validate_title(value)
        elif isinstance(obj.get("items"), dict):
            for value in obj["items"].values():
                _validate_title(value)

    _validate_title(schema)

    for definition_name, definition in schema.get("definitions", {}).items():  # type: ignore
        assert _VALID_DEFINITION_NAMES.match(definition_name), f"{definition_name} is not TitleCase"

        _validate_title(definition)
