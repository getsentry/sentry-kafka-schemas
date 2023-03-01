from typing import Iterator, Tuple, Any
import pytest
import os
import rapidjson
import fastjsonschema
import jsonschema
from yaml import safe_load


def get_all_schemas() -> Iterator[Tuple[Any, Any]] :
    for topic in os.listdir("topics/"):
        assert topic.endswith(".yaml")
        with open(os.path.join("topics/", topic)) as f:
            topic_meta = safe_load(f)

            for schema in topic_meta['schemas']:
                assert isinstance(schema['version'], int)
                assert schema['type'] == 'json'

                jsonschema_path = os.path.join("schemas/", schema['resource'])

                for example in schema['examples']:
                    example_path = os.path.join("examples/", example)
                    if os.path.isfile(example_path):
                        yield jsonschema_path, example_path
                    else:
                        for example_subpath in os.listdir(example_path):
                            yield jsonschema_path, os.path.join(example_path, example_subpath)


@pytest.mark.parametrize("jsonschema_path,example_path", get_all_schemas())
@pytest.mark.parametrize("jsonschema_library", ['fastjsonschema', 'jsonschema'])
def test_examples(jsonschema_path: str, example_path: str, jsonschema_library: str) -> None:
    with open(jsonschema_path) as f:
        schema = rapidjson.load(f)

    with open(example_path) as f:
        example = rapidjson.load(f)

    if jsonschema_library == 'fastjsonschema':
        fastjsonschema.compile(schema)(example)
    elif jsonschema_library == 'jsonschema':
        jsonschema.validate(example, schema)
