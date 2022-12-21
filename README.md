# Kafka topic and schema registry for Sentry

This is currently intended for use by the Snuba service

## Defining topics

Each topic is a yaml file in the topics directory. This topic name is really a "logical" topic name as many services in Sentry default name to a different physical topic name if desired. Topic names must be unique in Sentry: the same name cannot be used for different types of data.

The yaml file of a topic has 3 keys:

1. `topic`. This is the logical topic name. It must match the filename.

2. `topic_creation_config`. Key/value pairs containing any configuration needed when creating the topic. A common example we use at Sentry is `message.timestamp.type:LogAppendTime`

3. `schema`. `type` and `resource` should be provided. Currently the only `type` supported is json. `resource` should match the name of the file in the `schemas` directory.

## Defining schemas

Currently only jsonschema is supported. The jsonschema should be placed directly in the `schemas` directory, and then referenced from the relevant topic/s.
