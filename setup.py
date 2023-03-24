from setuptools import find_packages, setup

from typing import Sequence


def get_requirements() -> Sequence[str]:
    with open("python/requirements.txt") as fp:
        return [x.strip() for x in fp if not x.startswith("#")]

setup(
    name="sentry-kafka-schemas",
    version="0.0.10",
    author="Sentry",
    author_email="oss@sentry.io",
    url="https://github.com/getsentry/sentry-kafka-schemas",
    description="Kafka topics and schemas for Sentry",
    zip_safe=False,
    install_requires=get_requirements(),
    packages=["sentry_kafka_schemas", "sentry_kafka_schemas.schema_types"],
    package_dir={"": "python/"},
    package_data={"sentry_kafka_schemas": ["py.typed"]},
    include_package_data=True,
    options={"bdist_wheel": {"universal": "1"}},
)
