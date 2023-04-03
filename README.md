# Kafka topic and schema registry for Sentry

Contains the Kafka topics and schema definitions used by the Sentry service.

## Defining schemas

Currently only jsonschema is supported. The jsonschema should be placed directly in the `schemas` directory, and then referenced from the relevant topic.

## How strict should my schema be?

If in doubt, we recommend that schemas are only as strict as is minimally required by all consumers and downstream code required by Sentry. However it is ultimately up to the owners of the schema to decide whether a stricter schema is appropriate in particular scenarios.

## Adding example messages

Example messages can be placed in the `examples` directory and referenced from the relevant topic/version.

Example messages must be stripped of **all** customer related data. This also includes things like organization and project IDs, which should be replaced with something like `project_id: 1` or `org_id: 1`.

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
// a schema referenced from `topics/events.yaml, containing topic: events
{
    "title": "main_schema",
    "description": "Some additional information about the schema."
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

Produces:

```python
# file: sentry_kafka_schemas/schema_types/events_v1.py

class MainSchema(TypedDict, total=False):
    """Some additional information about the schema."""

    subfield: SubSchema

class SubSchema(TypedDict, total=False):
    ...
```

`title` can be added at any level, not just within `definitions`, to produce
types. Use that power tastefully!

## Using Rust types

We use a completely different library for generating Rust types, and therefore
the rules by which Rust type names are generated are different. **Rust types
are work-in-progress.**

For now, schema files need to be explicitly added to `rust/build.rs`. The
generated types can be viewed with `make view-rust-types`, `cargo doc --open`, or
online on https://docs.rs/sentry-kafka-schemas.

## Release process and development install

For releasing a new stable version from main branch, go to
[Actions](https://github.com/getsentry/sentry-kafka-schemas/actions) and
trigger a new job for the `Release` workflow.

Most likely you are working on a PR to Snuba or Sentry where you already want
to use those types. You can do that by running `make build` in this repo, then
running `pip install -e ~/projects/sentry-kafka-schemas/`.

You need to re-run `make build` to update types -- they do not automatically
change with schema changes even if you install this package in development
mode.

To stop using a development version of this repo in whichever service you're
working on, you can reinstall Python dependencies in that repo. Most likely the
command is `make install-py-dev`.

## Schema ownership

All topics definitions, schemas and examples should have a defined owner or multiple owners if shared.
The CODEOWNERS file should be updated with this information whenever new schemas and topics are added.
