from typing import Sequence, Tuple

from sentry_kafka_schemas.sentry_kafka_schemas import TopicData, get_topic, list_topics


def _name(name):
    return name.replace("getsentry/", "").replace("/", "_")


def print_graph(topics: Sequence[Tuple[str, TopicData]]) -> None:
    print()
    print(".. mermaid::")
    print()
    print("   flowchart TD")

    services = set()

    for topic_name, topic in topics:
        print(f"       {_name(topic_name)}[({topic_name})]")
        print(
            f'       click {_name(topic_name)} "https://github.com/getsentry/sentry-kafka-schemas/blob/main/topics/{topic_name}.yaml" _blank'
        )

        for consumer in topic["services"]["consumers"]:
            print(f"       {_name(topic_name)} --> {_name(consumer)}")

        for producer in topic["services"]["producers"]:
            print(f"       {_name(producer)} --> {_name(topic_name)}")

        services.update(topic["services"]["consumers"])
        services.update(topic["services"]["producers"])

    for service in services:
        print(f'       click {_name(service)} "https://github.com/{service}" _blank')

    print()


def main():
    pipelines = {}
    for topic_name in list_topics():
        topic = get_topic(topic_name)
        pipelines.setdefault(topic.get("pipeline", "default"), []).append(
            (topic_name, topic)
        )

    for pipeline, topics in sorted(pipelines.items()):
        if pipeline != "default":
            print(f"Pipeline: {pipeline}")
        else:
            print("Other topics")
        print("-" * 72)
        print_graph(topics)


if __name__ == "__main__":
    main()
