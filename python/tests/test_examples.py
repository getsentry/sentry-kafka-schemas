from typing import Iterator, Tuple, Any
import pytest
import rapidjson
import fastjsonschema
import jsonschema

from sentry_kafka_schemas.sentry_kafka_schemas import _list_topics, _get_topic
from sentry_kafka_schemas.types import Example
from sentry_kafka_schemas import get_schema, iter_examples


def get_all_examples() -> Iterator[Example]:
    for topic in _list_topics():
        for schema_raw in _get_topic(topic)["schemas"]:
            version = schema_raw["version"]
            schema = get_schema(topic, version=version)
            yield from iter_examples(topic, version=version)


def _get_most_specific_jsonschema_error(e: jsonschema.ValidationError) -> None:
    """
    Errors from the jsonschema library are often somewhat vague as the
    validator backs out of 10 nested anyOfs. Dive in and pick a random specific
    issue to fix.
    """
    for e2 in e.context:
        return _get_most_specific_jsonschema_error(e2)
    raise e


@pytest.mark.parametrize("example", get_all_examples(), ids=str)
@pytest.mark.parametrize("jsonschema_library", ["fastjsonschema", "jsonschema"])
def test_examples(example: Example, jsonschema_library: str) -> None:
    schema = example.schema["schema"]

    with open(example.path) as f:
        example_data = rapidjson.load(f)

    if jsonschema_library == "fastjsonschema":
        fastjsonschema.compile(schema)(example_data)
    elif jsonschema_library == "jsonschema":
        try:
            jsonschema.validate(example_data, schema)
        except jsonschema.ValidationError as e:
            _get_most_specific_jsonschema_error(e)
