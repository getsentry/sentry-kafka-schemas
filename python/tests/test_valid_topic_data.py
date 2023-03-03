from pathlib import Path

from sentry_kafka_schemas import get_schema
from yaml import safe_load
import re


def test_all_topics() -> None:
    # `.` is technically also valid in Kafka but we don't allow it
    # at Sentry since it can collide with `_`
    valid_chars = re.compile("^[a-zA-Z0-9\-\_]+$")

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
        get_schema(filename.stem)
