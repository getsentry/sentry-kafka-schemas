from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Codec(ABC, Generic[T]):
    @abstractmethod
    def encode(self, data: T, validate: bool = True) -> bytes:
        """
        Decode bytes from Kafka message.
        If validate is true, validation is performed.
        """
        raise NotImplementedError

    @abstractmethod
    def decode(self, raw_data: bytes, validate: bool = True) -> T:
        """
        Decode bytes from Kafka message.
        If validate is true, validation is performed.
        """
        raise NotImplementedError

    @abstractmethod
    def validate(self, data: T) -> None:
        """

        Validate a decoded Python object again.

        Calling `decode(validate=False)` and then `validate()` should be
        equivalent to `decode(validate=True)`.
        """
        raise NotImplementedError


class ValidationError(Exception):
    """
    Raised by the codec when a message fails validation.
    """

    pass
