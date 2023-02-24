import pytest
from sentry_kafka_schemas import get_schema, SchemaNotFound


def test_get_schema() -> None:
    with pytest.raises(SchemaNotFound):
        get_schema("non_existent_topic")

    assert get_schema("querylog") is not None
