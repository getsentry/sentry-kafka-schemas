import re
from pathlib import Path

import fastjsonschema
from sentry_kafka_schemas import get_codec, get_topic, list_topics
from yaml import safe_load

_SCHEMAS = Path(__file__).parents[2].joinpath("schemas/")
_EXAMPLES = Path(__file__).parents[2].joinpath("examples/")
_TOPICS = Path(__file__).parents[2].joinpath("topics/")

_TOPIC_SCHEMA = fastjsonschema.compile(
    {
        "properties": {
            "description": {"type": "string"},
            "pipeline": {"type": "string"},
            "services": {
                "properties": {
                    "consumers": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Repo"},
                    },
                    "producers": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Repo"},
                    },
                },
                "required": ["consumers", "producers"],
                "aditionalProperties": False,
            },
            "schemas": {
                "type": "array",
                "items": {
                    "properties": {
                        "version": {"type": "integer", "minimum": 1},
                        "type": {"enum": ["msgpack", "json", "protobuf"]},
                        "compatibility_mode": {"enum": ["none", "backward"]},
                        "resource": {"type": "string"},
                        "examples": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": [
                        "version",
                        "type",
                        "compatibility_mode",
                        "resource",
                        "examples",
                    ],
                },
            },
            "topic_creation_config": {
                "type": "object",
                "additionalProperties": {"type": "string"},
            },
        },
        "aditionalProperties": False,
        "required": ["description", "services"],
        "definitions": {
            "Repo": {
                "enum": [
                    # enumerate all repos here to avoid typos
                    "getsentry/relay",
                    "getsentry/sentry",
                    "getsentry/snuba",
                    "getsentry/vroom",
                    "getsentry/uptime-checker",
                    "getsentry/super-big-consumers",
                    "getsentry/taskbroker",
                    "getsentry/launchpad",
                ]
            }
        },
    }
)


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

            _TOPIC_SCHEMA(topic_data)

            # Check valid topic name
            topic_name = filename.stem
            assert valid_chars.match(topic_name)
            assert len(topic_name) <= 255

            # Check description provided for topic
            assert topic_data["description"]

            # Check every topic has an explicit, valid compression type
            # Today we use lz4 everywhere, this list can be extended if needed
            valid_types = ["lz4"]
            assert topic_data["topic_creation_config"]["compression.type"] in valid_types

            # Check valid schema versions
            topic_schemas = topic_data["schemas"]
            for i, schema_raw in enumerate(topic_schemas):
                if schema_raw["type"] != "protobuf":
                    used_schema_filepaths.add(_SCHEMAS.joinpath(schema_raw["resource"]))

                for example_path in schema_raw["examples"]:
                    for entry in _EXAMPLES.joinpath(example_path).rglob("*"):
                        if entry.is_file():
                            used_examples.add(entry)

                assert schema_raw["version"] == i + 1

        # The schema can be loaded
        get_codec(filename.stem)

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


def test_retention() -> None:
    # All topics at sentry have either 1 day or 7 day retention and this property is mandatory
    allowed_values = [
        str(1 * 1000 * 60 * 60 * 24),  # 1 day
        str(7 * 1000 * 60 * 60 * 24),  # 7 days
    ]

    for topic_name in list_topics():
        topic = get_topic(topic_name)

        retention = topic["topic_creation_config"]["retention.ms"]
        cleanup_policy = topic["topic_creation_config"].get("cleanup.policy")

        # infinite retntion (-1) is allowed only when the cleanup.policy is set
        # to log compaction mode
        if cleanup_policy == "compact":
            allowed = [*allowed_values, "-1"]
        else:
            allowed = allowed_values

        # Helpful error message if set to -1 but not using compact mode
        if retention == "-1" and cleanup_policy != "compact":
            error = "Cleanup policy should be set to compact when retention is set to -1"
        else:
            error = f"Invalid retention for topic {topic_name}: {retention}"

        assert retention in allowed, error


def test_dlq_configuration() -> None:
    # These topics do not match the naming conventions
    custom_dlq_mapping = {
        "ingest-generic-metrics-dlq": "ingest-performance-metrics",
        "snuba-dead-letter-replays": "ingest-replay-events",
        "snuba-dead-letter-metrics": "snuba-metrics",
        "snuba-dead-letter-querylog": "snuba-queries",
        "snuba-dead-letter-generic-metrics": "snuba-generic-metrics",
    }

    topics_dir = _TOPICS
    dlq_suffix = "-dlq"
    snuba_dlq_prefix = "snuba-dead-letter-"

    for filename in topics_dir.iterdir():
        if filename.stem.endswith(dlq_suffix):
            main_topic_name = custom_dlq_mapping.get(
                filename.stem, filename.stem[: -len(dlq_suffix)]
            )

        elif filename.stem.startswith(snuba_dlq_prefix):
            main_topic_name = custom_dlq_mapping.get(
                filename.stem, filename.stem[len(snuba_dlq_prefix) :]
            )
        else:
            continue

        with (
            open(filename) as dlq_file,
            open(f"{filename.parent}/{main_topic_name}.yaml") as main_topic_file,
        ):
            dlq_topic_data = safe_load(dlq_file)
            main_topic_data = safe_load(main_topic_file)

            # max.message.bytes matches
            assert dlq_topic_data["topic_creation_config"].get(
                "max.message.bytes"
            ) == main_topic_data["topic_creation_config"].get("max.message.bytes")

            # DLQ has 7 day retention
            assert dlq_topic_data["topic_creation_config"]["retention.ms"] == str(
                7 * 1000 * 60 * 60 * 24
            )
