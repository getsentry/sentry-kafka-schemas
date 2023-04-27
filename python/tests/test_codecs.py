import pytest
import json
from pathlib import Path
from typing import TypedDict
from sentry_kafka_schemas.codecs import Codec

from sentry_kafka_schemas.codecs.json import JsonCodec
from sentry_kafka_schemas.codecs.msgpack import MsgpackCodec


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
def test_json_codec(codec_cls: Codec) -> None:
    schema_path = Path.joinpath(
        Path(__file__).parent, "test.schema.json"
    )
    with open(schema_path, mode="r") as f:
        schema = json.loads(f.read())

    codec: JsonCodec[Example] = JsonCodec(json_schema=schema)

    data = get_example_data()

    assert codec.decode(codec.encode(data, validate=False), validate=True) == data