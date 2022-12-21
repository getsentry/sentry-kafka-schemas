from typing import Optional

from sentry_kafka_topics.types import TopicConfig


def get_topic_configuration(topic: str) -> Optional[TopicConfig]:
    """
    Placeholder.

    This function should return a TopicConfig object for the specified
    topic. This includes the schema if one is defined for that topic.
    If the topic itself is not defined, it returns None.
    """

    return None
