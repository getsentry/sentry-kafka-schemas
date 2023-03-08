from typing import Iterator, Tuple, Any
import pytest
import rapidjson
import fastjsonschema
import jsonschema

import sentry_kafka_schemas
import sentry_kafka_schemas.sentry_kafka_schemas


def get_all_schemas() -> Iterator[Tuple[Any, Any]]:
    for topic in sentry_kafka_schemas.sentry_kafka_schemas._list_topics():
        for schema_raw in sentry_kafka_schemas.sentry_kafka_schemas._get_topic(topic)[
            "schemas"
        ]:
            version = schema_raw["version"]
            schema = sentry_kafka_schemas.get_schema(topic, version=version)
            for x in sentry_kafka_schemas.iter_examples(topic, version=version):
                yield schema["schema_filepath"], x


def _get_most_specific_jsonschema_error(e: jsonschema.ValidationError) -> None:
    """
    Errors from the jsonschema library are often somewhat vague as the
    validator backs out of 10 nested anyOfs. Dive in and pick a random specific
    issue to fix.
    """
    for e2 in e.context:
        return _get_most_specific_jsonschema_error(e2)
    raise e


@pytest.mark.parametrize("jsonschema_path,example_path", get_all_schemas())
@pytest.mark.parametrize("jsonschema_library", ["fastjsonschema", "jsonschema"])
def test_examples(
    jsonschema_path: str, example_path: str, jsonschema_library: str
) -> None:
    with open(jsonschema_path) as f:
        schema = rapidjson.load(f)

    with open(example_path) as f:
        example = rapidjson.load(f)

    if jsonschema_library == "fastjsonschema":
        fastjsonschema.compile(schema)(example)
    elif jsonschema_library == "jsonschema":
        try:
            jsonschema.validate(example, schema)
        except jsonschema.ValidationError as e:
            _get_most_specific_jsonschema_error(e)
