from sentry_kafka_topics import get_topic_configuration


def test_get_topic_configuration() -> None:
    assert get_topic_configuration("a") is None
