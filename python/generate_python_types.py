import os
import shutil
import sys
from typing import Any

import sentry_kafka_schemas
import sentry_kafka_schemas.sentry_kafka_schemas
from jsonschema_gentypes import BuiltinType, Type, api_draft_07, cli
from jsonschema_gentypes.jsonschema_draft_04 import JSONSchemaD4
from jsonschema_gentypes.jsonschema_draft_2020_12_applicator import JSONSchemaItemD2020
from jsonschema_gentypes.resolver import RefResolver, UnRedolvedException
from sentry_kafka_schemas.codecs.json import file_handler


class BytesExtensionForMypy(api_draft_07.APIv7):
    def build_type(
        self,
        schema: JSONSchemaD4 | JSONSchemaItemD2020,
        proposed_name: str,
    ) -> Type:
        if schema.get("$bytes"):
            return BuiltinType("bytes")
        else:
            return super().build_type(schema, proposed_name)


api_draft_07.APIv7 = BytesExtensionForMypy  # type: ignore[misc]


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

            cli.jsonschema_gentypes.resolver.RefResolver = FileRefResolver  # type: ignore[attr-defined]
            sys.argv = [
                "generate_python_types",
                "--json-schema",
                schema_data["schema_filepath"],
                "--python",
                os.path.join(target_folder, f"{schema_tmp_module_name}.py"),
            ]

            already_used_filenames.add(schema_tmp_module_name)
            cli.main()

    index_code_path = os.path.join(target_folder, "__init__.py")
    with open(index_code_path, "w"):
        # just touch file so it exists
        pass


class FileRefResolver(RefResolver):
    """Extended RefResolver that can handle file:// references"""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.loaded_schemas: dict[str, Any] = {}

    def lookup(self, uri: str) -> Any:
        if uri.startswith("#/"):
            fragment = uri[2:]
            # Try current schema first
            try:
                return self._resolve_internal_ref(fragment)
            except UnRedolvedException:
                # Try all loaded schemas
                for loaded_schema in self.loaded_schemas.values():
                    try:
                        return self._resolve_internal_ref(fragment, loaded_schema)
                    except UnRedolvedException:
                        continue

        if uri.startswith("file://"):
            filename, fragment = uri.split("#", 1) if "#" in uri else (uri, "")

            referenced_schema = file_handler(filename)
            self.loaded_schemas[filename] = referenced_schema

            if fragment:
                parts = fragment.split("/")
                current = referenced_schema
                for part in parts[1:]:
                    if not isinstance(current, dict) or part not in current:
                        raise UnRedolvedException(f"Invalid reference path: {fragment}")
                    current = current[part]
                return current
            return referenced_schema
        return super().lookup(uri)

    def _resolve_internal_ref(self, ref_path: str, schema: Any | None = None) -> Any:
        """Resolve internal references within a schema"""
        if schema is None:
            schema = self.schema

        parts = ref_path.split("/")
        current = schema

        for part in parts:
            if not isinstance(current, dict) or part not in current:
                raise UnRedolvedException(f"Reference not found: {ref_path}")
            current = current[part]  # type: ignore[literal-required]
        return current


if __name__ == "__main__":
    run()
