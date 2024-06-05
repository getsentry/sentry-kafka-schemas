from typing import Iterator, Tuple

import fastjsonschema
import jsonschema
import pytest
import rapidjson
from sentry_kafka_schemas import iter_examples
from sentry_kafka_schemas.sentry_kafka_schemas import _get_schema, get_topic, list_topics
from sentry_kafka_schemas.types import Example


def get_all_examples() -> Iterator[Tuple[str, int, Example]]:
    for topic in list_topics():
        for schema_raw in get_topic(topic)["schemas"]:
            version = schema_raw["version"]
            for x in iter_examples(topic, version=version):
                yield topic, version, x


def _get_most_specific_jsonschema_error(e: jsonschema.ValidationError) -> None:
    """
    Errors from the jsonschema library are often somewhat vague as the
    validator backs out of 10 nested anyOfs. Dive in and pick a random specific
    issue to fix.
    """
    for e2 in e.context:
        return _get_most_specific_jsonschema_error(e2)
    raise e


def test_file_extension() -> None:
    for example in get_all_examples():
        assert example[2].path.name.endswith((".msgpack", ".json"))


@pytest.mark.parametrize("topic,version,example", get_all_examples(), ids=str)
@pytest.mark.parametrize("jsonschema_library", ["fastjsonschema", "jsonschema", "rapidjson"])
def test_examples(
    topic: str,
    version: int,
    example: Example,
    jsonschema_library: str,
) -> None:
    schema = _get_schema(topic, version=version)["schema"]
    example_data = example.load()

    if jsonschema_library == "fastjsonschema":
        compiled = fastjsonschema.compile(schema)
        compiled(example_data)
    elif jsonschema_library == "jsonschema":
        try:
            jsonschema.validate(example_data, schema)
        except jsonschema.ValidationError as e:
            _get_most_specific_jsonschema_error(e)
    elif jsonschema_library == "rapidjson":
        compiled = rapidjson.Validator(rapidjson.dumps(schema))
        raw_example_data = rapidjson.dumps(example_data)
        compiled(raw_example_data)
