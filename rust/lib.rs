use serde::{Deserialize, Serialize};
use std::error;
use std::fmt;
use std::fs::{read_to_string, File};
use std::path::{Path, PathBuf};

// This file is supposed to be auto-generated via rust/build.rs
pub mod schema_types {
    include!(concat!(env!("OUT_DIR"), "/schema_types.rs"));
}

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

#[derive(Debug, PartialEq, Eq)]
#[non_exhaustive]
pub enum SchemaError {
    TopicNotFound,
    InvalidVersion,
    InvalidType,
    InvalidSchema,
}

impl fmt::Display for SchemaError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            SchemaError::TopicNotFound => write!(f, "Topic not found"),
            SchemaError::InvalidVersion => write!(f, "Invalid version"),
            SchemaError::InvalidType => write!(f, "Invalid type"),
            SchemaError::InvalidSchema => write!(f, "Invalid schema"),
        }
    }
}

impl error::Error for SchemaError {}

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
    topic: String,
    schemas: Vec<TopicSchema>,
}

impl TopicData {
    fn load(path: &Path) -> Result<Self, SchemaError> {
        let f = File::open(path).map_err(|_| SchemaError::TopicNotFound)?;
        serde_yaml::from_reader(f).map_err(|_| SchemaError::TopicNotFound)
    }
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct Schema {
    pub version: u16,
    pub schema_type: SchemaType,
    pub compatibility_mode: CompatibilityMode,
    // TODO: Actually parse the json schema
    pub schema: String,
    pub schema_filepath: PathBuf,
}

/// Returns the schema for a topic. If version is passed, return the schema for
/// the specified version, otherwise the latest version is returned.
///
/// Only JSON schemas are currently supported.
///
/// # Errors
///
/// Will return `Err` if `topic` or `version` is not found or if schema data is invalid.
pub fn get_schema(topic: &str, version: Option<u16>) -> Result<Schema, SchemaError> {
    let topic_path = Path::new(env!("CARGO_MANIFEST_DIR")).join(format!("topics/{topic}.yaml"));
    let mut topic_data = TopicData::load(&topic_path)?;
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

    let json_schema_path =
        Path::new(env!("CARGO_MANIFEST_DIR")).join(format!("schemas/{}", schema_metadata.resource));

    Ok({
        Schema {
            version: schema_metadata.version,
            schema_type: schema_metadata.schema_type,
            compatibility_mode: schema_metadata.compatibility_mode,
            schema: read_to_string(&json_schema_path).map_err(|_| SchemaError::InvalidSchema)?,
            schema_filepath: json_schema_path.to_owned(),
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_schema() {
        assert_eq!(get_schema("asdf", None), Err(SchemaError::TopicNotFound));
        let schema = get_schema("querylog", None).unwrap();
        assert_eq!(schema.version, 1);
        assert_eq!(schema.schema_type, SchemaType::Json);
    }
}
