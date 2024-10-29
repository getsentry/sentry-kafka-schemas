from typing import TypeVar, cast


from google.protobuf.message import Message as ProtoMessage
from sentry_kafka_schemas.codecs import Codec, ValidationError

T = TypeVar("T", bound=ProtoMessage)


class ProtobufCodec(Codec[T]):
    """
    This codec assumes the payload is a protobuf payload.

    `resource` should be a module path to the message type
    in a protobuf generated module. For us this will most likely
    be message in `sentry-protos`.
    """

    def __init__(self, resource: str) -> None:
        self._resource = resource
        self._message_cls = self._import_resource()

    def _import_resource(self) -> type[T]:
        module_name, class_name = self._resource.rsplit(".", 1)

        module = __import__(module_name, {}, {}, [class_name])
        return getattr(module, class_name)

    def encode(self, data: T, validate: bool = True) -> bytes:
        # There isn't any validation logic as protobuf
        # does most of the type validation as messages are constructed.
        return data.SerializeToString()

    def decode(self, raw_data: bytes, validate: bool = True) -> T:
        # There isn't any validation logic as protobuf
        # does validation implicitly when deserializing.
        instance = self._message_cls()
        instance.ParseFromString(raw_data)
        return instance

    def validate(self, data: T) -> None:
        try:
            instance = self._message_cls()
            instance.ParseFromString(data)
        except Exception as exc:
            raise ValidationError from exc
