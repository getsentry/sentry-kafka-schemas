import os
import shutil
import subprocess

import sentry_kafka_schemas
import sentry_kafka_schemas.sentry_kafka_schemas


def run(target_folder: str = "python/sentry_kafka_schemas/schema_types/") -> None:
    shutil.rmtree(target_folder, ignore_errors=True)
    os.makedirs(target_folder)

    module_index = {}

    for topic_name in sentry_kafka_schemas.sentry_kafka_schemas._list_topics():
        print(f"generating schemas for {topic_name}")
        topic_meta = sentry_kafka_schemas.sentry_kafka_schemas._get_topic(topic_name)
        for schema_meta in topic_meta["schemas"]:
            version = schema_meta["version"]
            schema_data = sentry_kafka_schemas.get_schema(topic_name, version)
            if schema_data["type"] != "json":
                continue

            schema_tmp_typename = f"{topic_name.title()}_v{version}"
            schema_tmp_module_name = schema_tmp_typename.lower()
            module_index[schema_tmp_typename] = schema_tmp_module_name, schema_data[
                "schema"
            ].get("title", "Main")
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
    with open(index_code_path, "w") as f:
        for type_name, (module_name, real_type_name) in module_index.items():
            f.write(f"from .{module_name} import {real_type_name} as {type_name}\n")

        f.write(f"__all__ = {repr(list(module_index))}\n")


if __name__ == "__main__":
    run()
