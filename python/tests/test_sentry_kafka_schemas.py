import pytest
from sentry_kafka_schemas import get_schema, SchemaNotFound


def test_get_schema() -> None:
    with pytest.raises(SchemaNotFound):
        get_schema("non_existent_topic")

    with pytest.raises(SchemaNotFound):
        get_schema("querylog", 1000)

    assert get_schema("querylog") is not None
    assert get_schema("querylog", 1) is not None
    assert get_schema("querylog", 1) == get_schema("querylog", 1)
