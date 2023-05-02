import pytest
from sentry_kafka_schemas import get_codec, SchemaNotFound


def test_get_schema() -> None:
    topic_name = "snuba-queries"

    with pytest.raises(SchemaNotFound):
        get_codec("non_existent_topic")

    with pytest.raises(SchemaNotFound):
        get_codec(topic_name, 1000)

    assert get_codec(topic_name) is not None
    assert get_codec(topic_name, 1) is not None
    assert get_codec(topic_name, 1) == get_codec(topic_name, 1)
