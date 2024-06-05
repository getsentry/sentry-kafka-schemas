import pytest
from sentry_kafka_schemas import SchemaNotFound, get_codec, get_topic


def test_get_topic() -> None:
    topic_name = "snuba-queries"
    topic_data = get_topic(topic_name)
    assert topic_data["topic_creation_config"] == {
        "compression.type": "lz4",
        "max.message.bytes": "50000000",
        "message.timestamp.type": "LogAppendTime",
        "retention.ms": "86400000",
    }

    assert topic_data["enforced_partition_count"] is None

    assert get_topic("snuba-commit-log")["enforced_partition_count"] == 1


def test_get_schema() -> None:
    topic_name = "snuba-queries"

    with pytest.raises(SchemaNotFound):
        get_codec("non_existent_topic")

    with pytest.raises(SchemaNotFound):
        get_codec(topic_name, 1000)

    assert get_codec(topic_name) is not None
    assert get_codec(topic_name, 1) is not None
    assert get_codec(topic_name, 1) == get_codec(topic_name, 1)
