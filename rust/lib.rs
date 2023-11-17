use std::path::PathBuf;

use jsonschema::JSONSchema;
use serde::{Deserialize, Serialize};
use thiserror::Error;

// This file is supposed to be auto-generated via rust/build.rs
pub mod schema_types {
    include!(concat!(env!("OUT_DIR"), "/schema_types.rs"));
}

include!(concat!(env!("OUT_DIR"), "/embedded_data.rs"));

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[non_exhaustive]
pub enum SchemaType {
    #[serde(rename = "json")]
    Json,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[non_exhaustive]
pub enum CompatibilityMode {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "backward")]
    Backward,
}

#[derive(Debug, Error)]
#[non_exhaustive]
pub enum SchemaError {
    #[error("Topic not found")]
    TopicNotFound,
    #[error("Invalid version")]
    InvalidVersion,
    #[error("Invalid type")]
    InvalidType,
    #[error("Invalid schema")]
    InvalidSchema,
    // FIXME(swatinem): maybe a dedicated `ValidationError` would be nice which
    // carries a JSON error as well as the exact Schema error.
    #[error("Invalid message")]
    InvalidMessage,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct TopicSchema {
    version: u16,
    #[serde(rename = "type")]
    schema_type: SchemaType,
    compatibility_mode: CompatibilityMode,
    resource: String,
    examples: Vec<String>,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
struct TopicData {
    topic: String,
    schemas: Vec<TopicSchema>,
}

fn find_entry<'s>(slice: &[(&str, &'s str)], key: &str) -> Option<&'s str> {
    let idx = slice.binary_search_by_key(&key, |&(name, _)| name).ok()?;
    Some(slice.get(idx)?.1)
}

impl TopicData {
    fn load(topic: &str) -> Result<Self, SchemaError> {
        let topic_data = find_entry(TOPICS, topic).ok_or(SchemaError::TopicNotFound)?;
        serde_yaml::from_str(topic_data).map_err(|_| SchemaError::TopicNotFound)
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Schema {
    pub version: u16,
    pub schema_type: SchemaType,
    pub compatibility_mode: CompatibilityMode,
    // FIXME(swatinem): this should maybe be private, with an accessor, or rather &'static str?
    pub schema: String,
    // FIXME(swatinem): this should be removed in a breaking release
    pub schema_filepath: PathBuf,
    // FIXME(swatinem): this is an `Option` because of `Default`/`Deserialize`.
    #[serde(skip)]
    compiled_json_schema: Option<JSONSchema>,
}

impl PartialEq for Schema {
    fn eq(&self, other: &Self) -> bool {
        self.version == other.version
            && self.schema_type == other.schema_type
            && self.compatibility_mode == other.compatibility_mode
            && self.schema == other.schema
            && self.schema_filepath == other.schema_filepath
    }
}

impl Schema {
    pub fn validate_json(&self, input: &[u8]) -> Result<(), SchemaError> {
        let message = serde_json::from_slice(input).map_err(|_| SchemaError::InvalidMessage)?;

        let compiled = self
            .compiled_json_schema
            .as_ref()
            .ok_or(SchemaError::InvalidSchema)?;

        compiled
            .validate(&message)
            .map_err(|_| SchemaError::InvalidMessage)?;

        // FIXME(swatinem): we might as well just return the `Value` here
        Ok(())
    }
}

pub fn get_topic_schema(topic: &str, version: Option<u16>) -> Result<TopicSchema, SchemaError> {
    let mut topic_data = TopicData::load(topic)?;
    topic_data.schemas.sort_by_key(|x| x.version);

    let schema_metadata = if let Some(version) = version {
        topic_data
            .schemas
            .into_iter()
            .find(|x| x.version == version)
            .ok_or(SchemaError::TopicNotFound)?
    } else {
        topic_data
            .schemas
            .pop()
            .ok_or(SchemaError::InvalidVersion)?
    };

    if schema_metadata.schema_type != SchemaType::Json {
        return Err(SchemaError::InvalidType);
    }

    Ok(schema_metadata)
}

/// Returns the schema for a topic. If `version`` is passed, return the schema for
/// the specified version, otherwise the latest version is returned.
///
/// Only JSON schemas are currently supported.
///
/// # Errors
///
/// Will return `Err` if `topic` or `version` is not found or if schema data is invalid.
pub fn get_schema(topic: &str, version: Option<u16>) -> Result<Schema, SchemaError> {
    let schema_metadata = get_topic_schema(topic, version)?;

    let schema =
        find_entry(SCHEMAS, &schema_metadata.resource).ok_or(SchemaError::InvalidSchema)?;

    let s = serde_json::from_str(schema).map_err(|_| SchemaError::InvalidSchema)?;
    let compiled_json_schema =
        Some(JSONSchema::compile(&s).map_err(|_| SchemaError::InvalidSchema)?);

    let schema = schema.to_string();

    Ok({
        Schema {
            version: schema_metadata.version,
            schema_type: schema_metadata.schema_type,
            compatibility_mode: schema_metadata.compatibility_mode,
            schema,
            schema_filepath: PathBuf::new(),
            compiled_json_schema,
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    use std::fs::read_to_string;
    use std::path::Path;

    #[test]
    fn test_get_schema() {
        assert!(matches!(
            get_schema("asdf", None),
            Err(SchemaError::TopicNotFound)
        ));
        let schema = get_schema("snuba-queries", None).unwrap();
        assert_eq!(schema.version, 1);
        assert_eq!(schema.schema_type, SchemaType::Json);

        // Did not error
        get_schema("snuba-queries", Some(1)).unwrap();
    }

    #[test]
    fn test_validate() {
        let topic = "snuba-queries";
        let topic_schema = get_topic_schema(topic, None).unwrap();
        let schema = get_schema(topic, None).unwrap();
        let example_dir = topic_schema.examples.first().unwrap();
        let example_path = Path::new(env!("CARGO_MANIFEST_DIR"))
            .join(format!("examples/{}{}", example_dir, "snuba-queries1.json"));
        let example = read_to_string(example_path).unwrap();
        schema.validate_json(example.as_bytes()).unwrap();

        let invalid = "{}";
        assert!(matches!(
            schema.validate_json(invalid.as_bytes()),
            Err(SchemaError::InvalidMessage)
        ));
    }
}
