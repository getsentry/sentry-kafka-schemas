from setuptools import setup

from typing import Sequence


def get_requirements() -> Sequence[str]:
    with open("requirements.txt") as fp:
        return [x.strip() for x in fp if not x.startswith("#")]


setup(
    name="sentry-kafka-topics",
    version="0.0.1",
    author="Sentry",
    author_email="oss@sentry.io",
    url="https://github.com/getsentry/sentry-kafka-schemas",
    description="Kafka topics and schemas for Sentry",
    zip_safe=False,
    install_requires=get_requirements()
)
