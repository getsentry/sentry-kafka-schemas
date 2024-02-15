import re
from typing import Any, Iterator, Tuple
import pytest

from sentry_kafka_schemas.sentry_kafka_schemas import (
    list_topics,
    get_topic,
    _get_schema,
)


def get_all_schemas() -> Iterator[Tuple[str, int]]:
    for topic in list_topics():
        for schema_raw in get_topic(topic)["schemas"]:
            version = schema_raw["version"]
            yield topic, version


_VALID_DEFINITION_NAMES = re.compile(r"^[A-Z]([a-zA-Z0-9]+)$")
_VALID_TITLE_NAMES = re.compile(r"^[a-z][a-z0-9_]+$")


@pytest.mark.parametrize("topic,version", get_all_schemas())
def test_schemas_valid(topic: str, version: int) -> None:
    schema = _get_schema(topic, version=version)["schema"]

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
        assert _VALID_DEFINITION_NAMES.match(
            definition_name
        ), f"{definition_name} is not TitleCase"

        _validate_title(definition)
