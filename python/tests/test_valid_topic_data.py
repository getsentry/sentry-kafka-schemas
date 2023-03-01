from pathlib import Path
from yaml import safe_load

from sentry_kafka_schemas import get_schema


def test_all_topics() -> None:
    topics_dir = Path.joinpath(Path(__file__).parents[2], "topics")
    for filename in topics_dir.iterdir():
        if filename.suffix != ".yaml":
            raise Exception(f"Invalid YAML file: {filename}")

        # The schema can be loaded
        schema = get_schema(filename.stem)
