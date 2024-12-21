use jsonschema::{JSONSchema, SchemaResolver, SchemaResolverError};
use serde::{Deserialize, Serialize};
use thiserror::Error;
use serde_json::Value;
use std::{sync::Arc};
use url::Url;
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
    #[serde(rename = "msgpack")]
    Msgpack,
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
struct TopicSchema {
    version: u16,
    #[serde(rename = "type")]
    schema_type: SchemaType,
    compatibility_mode: CompatibilityMode,
    resource: String,
    examples: Vec<String>,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
struct TopicData {
    schemas: Vec<TopicSchema>,
}

fn find_entry<'s, T>(slice: &'s [(&str, T)], key: &str) -> Option<&'s T> {
    let idx = slice.binary_search_by_key(&key, |&(name, _)| name).ok()?;
    Some(&slice.get(idx)?.1)
}

impl TopicData {
    fn load(topic: &str) -> Result<Self, SchemaError> {
        let topic_data = find_entry(TOPICS, topic).ok_or(SchemaError::TopicNotFound)?;
        serde_yaml::from_str(topic_data).map_err(|_| SchemaError::TopicNotFound)
    }
}

#[derive(Debug)]
pub struct Schema {
    pub version: u16,
    pub schema_type: SchemaType,
    pub compatibility_mode: CompatibilityMode,
    schema: &'static str,
    compiled_json_schema: JSONSchema,
    examples: &'static [Example],
}

impl PartialEq for Schema {
    fn eq(&self, other: &Self) -> bool {
        self.version == other.version
            && self.schema_type == other.schema_type
            && self.compatibility_mode == other.compatibility_mode
            && self.schema == other.schema
    }
}

impl Schema {
    pub fn validate_json(&self, input: &[u8]) -> Result<serde_json::Value, SchemaError> {
        let message = serde_json::from_slice(input).map_err(|_| SchemaError::InvalidMessage)?;

        if self.compiled_json_schema.is_valid(&message) {
            Ok(message)
        } else {
            Err(SchemaError::InvalidMessage)
        }
    }

    /// Returns the raw JSON Schema definition.
    pub fn raw_schema(&self) -> &str {
        self.schema
    }

    /// Returns a list of examples for this schema.
    pub fn examples(&self) -> &[Example] {
        self.examples
    }
}

#[derive(Debug)]
pub struct Example {
    name: &'static str,
    payload: &'static [u8],
}

impl Example {
    pub fn name(&self) -> &str {
        self.name
    }

    pub fn payload(&self) -> &[u8] {
        self.payload
    }
}

fn get_topic_schema(topic: &str, version: Option<u16>) -> Result<TopicSchema, SchemaError> {
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

    Ok(schema_metadata)
}

struct FileSchemaResolver { }

impl FileSchemaResolver {
    fn new() -> Self {
        Self { }
    }
}

impl SchemaResolver for FileSchemaResolver {
    fn resolve(&self, _root_schema: &Value, url: &Url, _original_reference: &str) -> Result<Arc<Value>, SchemaResolverError> {
        if url.scheme() == "file" {
           let url_str = url.as_str();
            let relative_path = &url_str[7..url_str.len() - 1];
            let schema = find_entry(SCHEMAS, relative_path).ok_or(SchemaError::InvalidSchema)?;
            let schema_json = serde_json::from_str(schema).map_err(|_| SchemaError::InvalidSchema)?;
            return Ok(Arc::new(schema_json));

        }

        Err(SchemaResolverError::new(Box::new(std::io::Error::new(
            std::io::ErrorKind::NotFound,
            format!("Unsupported URL scheme: {}", url.scheme()),
        ))))
    }
}

/// Returns the schema for a topic. If `version` is passed, return the schema for
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
    let resolver = FileSchemaResolver::new();
    let compiled_json_schema = JSONSchema::options().with_resolver(resolver).compile(&s).map_err(|_| SchemaError::InvalidSchema)?;

    // FIXME(swatinem): This assumes that there is only a single `examples` entry in the definition.
    // If we would want to support multiple, we would have to either merge those in code generation,
    // or rather use a `fn examples() -> impl Iterator`.
    let examples = schema_metadata
        .examples
        .first()
        .and_then(|example| find_entry(EXAMPLES, example))
        .copied()
        .unwrap_or_default();

    Ok(Schema {
        version: schema_metadata.version,
        schema_type: schema_metadata.schema_type,
        compatibility_mode: schema_metadata.compatibility_mode,
        schema,
        compiled_json_schema,
        examples,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_schema() {
        assert!(matches!(
            get_schema("asdf", None),
            Err(SchemaError::TopicNotFound)
        ));

        // Json topic
        let schema = get_schema("snuba-queries", None).unwrap();
        assert_eq!(schema.version, 1);
        assert_eq!(schema.schema_type, SchemaType::Json);

        // Msgpack topic
        let schema = get_schema("ingest-events", None).unwrap();
        assert_eq!(schema.version, 1);
        assert_eq!(schema.schema_type, SchemaType::Msgpack);

        // Did not error
        get_schema("snuba-queries", Some(1)).unwrap();
        get_schema("transactions", Some(1)).unwrap();
        get_schema("snuba-uptime-results", Some(1)).unwrap();
    }

    fn validate_schema(schema_name: &str) {
        let schema = get_schema(schema_name, None).unwrap();

        let examples = schema.examples();
        assert!(!examples.is_empty());
        for example in examples {
            schema.validate_json(example.payload()).unwrap();
        }

        assert!(matches!(
            schema.validate_json(b"{}"),
            Err(SchemaError::InvalidMessage)
        ));
    }

    #[test]
    fn test_validate() {
        validate_schema("snuba-queries");
        validate_schema("uptime-results");
        validate_schema("snuba-uptime-results");
    }
}
