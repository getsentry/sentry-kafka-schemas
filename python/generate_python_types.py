import os
import shutil
import subprocess

import sentry_kafka_schemas
import sentry_kafka_schemas.sentry_kafka_schemas


def run(target_folder: str = "python/sentry_kafka_schemas/schema_types/") -> None:
    shutil.rmtree(target_folder, ignore_errors=True)
    os.makedirs(target_folder)

    already_used_filenames = set()

    for topic_name in sentry_kafka_schemas.sentry_kafka_schemas.list_topics():
        print(f"generating schemas for {topic_name}")
        topic_meta = sentry_kafka_schemas.sentry_kafka_schemas.get_topic(topic_name)
        for schema_meta in topic_meta["schemas"]:
            version = schema_meta["version"]
            schema_data = sentry_kafka_schemas.sentry_kafka_schemas._get_schema(topic_name, version)

            if schema_data["type"] == "protobuf":
                print(
                    f"Skipping generating types for protobuf message {schema_data['schema_filepath']}"
                )
                continue

            schema_tmp_typename_base = f"{topic_name.replace('-', '_')}_v{version}"
            schema_tmp_module_name = schema_tmp_typename_base.lower()
            if schema_tmp_module_name in already_used_filenames:
                raise RuntimeError(
                    f"conflict: two schemas are ending up in module name {schema_tmp_module_name}"
                )

            already_used_filenames.add(schema_tmp_module_name)
            subprocess.check_call(
                [
                    "jsonschema-gentypes",
                    "--json-schema",
                    schema_data["schema_filepath"],
                    "--python",
                    os.path.join(target_folder, f"{schema_tmp_module_name}.py"),
                ]
            )

    index_code_path = os.path.join(target_folder, "__init__.py")
    with open(index_code_path, "w"):
        # just touch file so it exists
        pass


if __name__ == "__main__":
    run()
