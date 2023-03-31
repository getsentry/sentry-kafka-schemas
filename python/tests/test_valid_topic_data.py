from pathlib import Path

from sentry_kafka_schemas import get_schema
from yaml import safe_load
import re

_SCHEMAS = Path(__file__).parents[2].joinpath("schemas/")
_EXAMPLES= Path(__file__).parents[2].joinpath("examples/")
_TOPICS = Path(__file__).parents[2].joinpath("topics/")


def test_all_topics() -> None:
    # `.` is technically also valid in Kafka but we don't allow it
    # at Sentry since it can collide with `_`
    valid_chars = re.compile(r"^[a-zA-Z0-9\-\_]+$")

    used_schema_filepaths = set()
    used_examples = set()

    topics_dir = _TOPICS
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
            for i, schema_raw in enumerate(topic_schemas):
                used_schema_filepaths.add(_SCHEMAS.joinpath(schema_raw['resource']))
                for example_path in schema_raw['examples']:
                    for entry in _EXAMPLES.joinpath(example_path).rglob("*"):
                        if entry.is_file():
                            used_examples.add(entry)

                assert schema_raw["version"] == i + 1

        # The schema can be loaded
        schema = get_schema(filename.stem)

        used_schema_filepaths.add(schema['schema_filepath'])

    existing_schema_filepaths = set()

    for entry in _SCHEMAS.rglob("*"):
        if entry.is_file():
            existing_schema_filepaths.add(entry)

    unused_schema_filepaths = existing_schema_filepaths - used_schema_filepaths
    # Assert that every schema file in schemas/ is referenced by a topic.
    assert not unused_schema_filepaths

    existing_examples = set()
    for entry in _EXAMPLES.rglob("*"):
        if entry.is_file():
            existing_examples.add(entry)

    # Assert that every example file in examples/ is referenced by a topic.
    unused_examples = existing_examples - used_examples
    assert not unused_examples
