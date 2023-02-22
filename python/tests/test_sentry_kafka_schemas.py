from sentry_kafka_schemas import get_schema


def test_get_schema() -> None:
    assert get_schema("non_existent_topic") is None
