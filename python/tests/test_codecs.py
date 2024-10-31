import json
import time
from pathlib import Path
from typing import Any, TypedDict

import pytest
from google.protobuf.timestamp_pb2 import Timestamp
from sentry_kafka_schemas.codecs import Codec
from sentry_kafka_schemas.codecs.json import JsonCodec
from sentry_kafka_schemas.codecs.msgpack import MsgpackCodec
from sentry_kafka_schemas.codecs.protobuf import ProtobufCodec
from sentry_protos.sentry.v1.taskworker_pb2 import TaskActivation


class Example(TypedDict):
    event_id: str
    project_id: int
    group_id: int


def get_example_data() -> Example:
    return {
        "event_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "project_id": 1,
        "group_id": 2,
    }


@pytest.mark.parametrize("codec_cls", [JsonCodec, MsgpackCodec])
def test_json_codec(codec_cls: Codec[Any]) -> None:
    schema_path = Path.joinpath(Path(__file__).parent, "test.schema.json")
    with open(schema_path, mode="rb") as f:
        schema = json.loads(f.read())

    codec: JsonCodec[Example] = JsonCodec(json_schema=schema)

    data = get_example_data()

    data_intermediate = codec.encode(data, validate=False)
    assert isinstance(data_intermediate, bytes)
    assert codec.decode(data_intermediate, validate=True) == data


def test_protobuf_codec() -> None:
    activation = TaskActivation(
        id="abc123",
        taskname="tests.do_things",
        namespace="tests",
        parameters='{"args":[],"kwargs":{}}',
        headers={},
        received_at=Timestamp(seconds=int(time.time())),
    )
    codec: ProtobufCodec[TaskActivation] = ProtobufCodec(
        resource="sentry_protos.sentry.v1.taskworker_pb2.TaskActivation"
    )
    serialized = codec.encode(activation)
    assert type(serialized) == bytes

    rebuild = codec.decode(serialized)
    assert rebuild
    assert rebuild.id == activation.id
    assert rebuild.taskname == activation.taskname
    assert rebuild.namespace == activation.namespace
    assert rebuild.parameters == activation.parameters
    assert rebuild.headers == activation.headers
    assert rebuild.received_at == activation.received_at
