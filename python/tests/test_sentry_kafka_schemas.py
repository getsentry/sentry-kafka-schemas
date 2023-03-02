import pytest
from sentry_kafka_schemas import get_schema, SchemaNotFound


def test_get_schema() -> None:
    topic_name = "snuba-queries"

    with pytest.raises(SchemaNotFound):
        get_schema("non_existent_topic")

    with pytest.raises(SchemaNotFound):
        get_schema(topic_name, 1000)

    assert get_schema(topic_name) is not None
    assert get_schema(topic_name, 1) is not None
    assert get_schema(topic_name, 1) == get_schema(topic_name, 1)
