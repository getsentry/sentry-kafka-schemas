import re
import pytest

from sentry_kafka_schemas.sentry_kafka_schemas import _list_topics, _get_topic, get_schema

def get_all_schemas():
    for topic in _list_topics():
        for schema_raw in _get_topic(topic)['schemas']:
            version = schema_raw['version']
            yield topic, version


_VALID_DEFINITION_NAMES = re.compile(r"^[A-Z]([a-zA-Z]+)$")
_VALID_TITLE_NAMES = re.compile(r"^[a-z][a-z_]+$")


@pytest.mark.parametrize("topic,version", get_all_schemas())
def test_schemas_valid(topic, version):
    schema = get_schema(topic, version=version)['schema']

    assert schema['$schema'] == "http://json-schema.org/draft-07/schema#"

    used_titles = set()

    def _validate_title(obj):
        if 'title' in obj:
            title = obj['title']
            assert _VALID_TITLE_NAMES.match(title), f"{title} is not snake_case"

            if title in used_titles:
                raise AssertionError(f"{title} duplicated")

            used_titles.add(title)

        if isinstance(obj, dict):
            for value in obj.get("properties", {}).values():
                _validate_title(value)

            if isinstance(obj.get("items"), list):
                for value in obj['items']:
                    _validate_title(value)
            elif isinstance(obj.get("items"), dict):
                for value in obj["items"].values():
                    _validate_title(value)


    _validate_title(schema)

    for definition_name, definition in schema.get('definitions', {}).items():
        assert _VALID_DEFINITION_NAMES.match(definition_name), f"{definition_name} is not TitleCase"

        _validate_title(definition)
