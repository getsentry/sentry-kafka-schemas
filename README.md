# Kafka topic and schema registry for Sentry

Contains the Kafka topics and schema definitions used by the Sentry service.

## Defining schemas

Currently only jsonschema is supported. The jsonschema should be placed directly in the `schemas` directory, and then referenced from the relevant topic.

## Adding example messages

Example messages can be placed in the `examples` directory and referenced from the relevant topic/version.

## Defining topics

Each topic is a yaml file in the topics directory. This topic name is a "logical" topic name as many services in Sentry support overriding the default name to a different physical topic name if desired. Topic names must be unique in Sentry: the same name cannot be used for different types of data.

The yaml file of a topic has 2 keys:

1. `topic`. This is the logical topic name. It must match the filename.

2. `schemas`. Schemas is an array. The following should be provided for each schema:
   - `version`: Incrementing integer. Should start at 1.
   - `compatibility_mode`: `none` or `backward`.
   - `type`: Currently only `json` is supported
   - `resource`: Should match the file name in the `schemas` directory
   - `examples`: Should match the file names in the `examples` directory

## Using Python types

Python types are automatically generated under
`sentry_kafka_schemas.schema_types`. A schema for version 1 of the topic
`foo-bar` is exported under `sentry_kafka_schemas.schema_types.foo_bar_v1`.

Use `title` attribute on your JSON schema and the various definitions to assign them a stable name.

For example:

```javascript
{
    "title": "main_schema",
    "properties": {
        "subfield": {"$ref": "#/definitions/SubSchema"}
    },
    "definitions": {
        "SubSchema": {
            "type": "object",
            "title": "sub_schema"
        }
    }
}
```
