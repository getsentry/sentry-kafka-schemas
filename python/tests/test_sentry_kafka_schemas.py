import pytest
from sentry_kafka_schemas import get_codec, SchemaNotFound, get_topic


def test_get_topic() -> None:
    # Topic with creation config
    topic_name = "snuba-queries"
    topic_data = get_topic(topic_name)
    assert topic_data["topic_creation_config"] == {"max.message.bytes": "2000000"}

    # Topic without creation config
    topic_name_no_config = "snuba-dead-letter-replays"
    topic_data = get_topic(topic_name_no_config)
    assert topic_data["topic_creation_config"] == {}


def test_get_schema() -> None:
    topic_name = "snuba-queries"

    with pytest.raises(SchemaNotFound):
        get_codec("non_existent_topic")

    with pytest.raises(SchemaNotFound):
        get_codec(topic_name, 1000)

    assert get_codec(topic_name) is not None
    assert get_codec(topic_name, 1) is not None
    assert get_codec(topic_name, 1) == get_codec(topic_name, 1)
