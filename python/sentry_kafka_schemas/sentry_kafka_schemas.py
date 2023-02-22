from typing import Optional
from sentry_kafka_schemas.types import Schema


def get_schema(topic: str, version: Optional[int] = None) -> Optional[Schema]:
    """
    Returns the schema for a topic. If version is passed, return the schema for
    the specified version, otherwise the latest version is returned.

    If a matching schema can't be found, return None.
    """

    # TODO: Implement this
    return None
