import pytest
from sentry_kafka_schemas import get_codec, SchemaNotFound, get_topic


def test_get_topic() -> None:
    topic_name = "snuba-queries"
    topic_data = get_topic(topic_name)
    assert topic_data["topic_creation_config"] == {
        "compression.type": "lz4",
        "max.message.bytes": "2000000",
    }

    assert topic_data["partitions"] is None

    assert get_topic("snuba-commit-log")["partitions"] == 1


def test_get_schema() -> None:
    topic_name = "snuba-queries"

    with pytest.raises(SchemaNotFound):
        get_codec("non_existent_topic")

    with pytest.raises(SchemaNotFound):
        get_codec(topic_name, 1000)

    assert get_codec(topic_name) is not None
    assert get_codec(topic_name, 1) is not None
    assert get_codec(topic_name, 1) == get_codec(topic_name, 1)
