import os
from pathlib import Path

from sentry_kafka_schemas import get_schema
from yaml import safe_load
import re


def test_all_topics() -> None:
    # `.` is technically also valid in Kafka but we don't allow it
    # at Sentry since it can collide with `_`
    valid_chars = re.compile(r"^[a-zA-Z0-9\-\_]+$")

    used_schema_filepaths = set()

    topics_dir = Path.joinpath(Path(__file__).parents[2], "topics")
    for filename in topics_dir.iterdir():
        if filename.suffix != ".yaml":
            raise Exception(f"Invalid YAML file: {filename}")

        with open(filename) as f:
            topic_data = safe_load(f)

            # Check valid topic name
            topic_name = topic_data["topic"]
            assert topic_name == filename.stem
            assert valid_chars.match(topic_name)
            assert len(topic_name) <= 255

            # Check description provided for topic
            assert topic_data["description"]

            # Check valid schema versions
            topic_schemas = topic_data["schemas"]
            for i in range(0, len(topic_schemas)):
                assert topic_schemas[i]["version"] == i + 1

        # The schema can be loaded
        schema = get_schema(filename.stem)

        used_schema_filepaths.add(schema['schema_filepath'])

    existing_schema_filepaths = set()

    for entry in Path(__file__).parents[2].joinpath("python/sentry_kafka_schemas/schemas/").rglob("*"):
        if entry.is_file():
            existing_schema_filepaths.add(str(entry))

    unused_schema_filepaths = existing_schema_filepaths - used_schema_filepaths
    # Assert that every schema file in schemas/ is referenced by a topic.
    assert not unused_schema_filepaths
