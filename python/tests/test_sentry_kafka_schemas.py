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


def test_bytes_in_ingest_monitors_codec() -> None:
    # preventing a regression since this msgpack contains `bytes` values
    payload = b'\x87\xa4type\xa8check_in\xacmessage_type\xa8check_in\xa7payload\xc4\xa9{"check_in_id":"cafecafecafecafe","monitor_slug":"some-monitor-slug","status":"in_progress","environment":"SANDBOX","contexts":{"trace":{"trace_id":"deadbeefdeadbeef"}}}\xaastart_time\xceg\x91(\xc0\xa3sdk\xb4sentry.python/2.19.0\xaaproject_id\xce\x00\x01\x86\x9f\xaeretention_days\x1e'
    codec = get_codec("ingest-monitors")
    # should not crash!
    codec.decode(payload)
