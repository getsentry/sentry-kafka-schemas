use serde::{Deserialize, Serialize};
use std::fmt;
use std::fs::{read_to_string, File};

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[non_exhaustive]
enum SchemaType {
    #[serde(rename = "json")]
    Json,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[non_exhaustive]
enum CompatibilityMode {
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
    fn load(path: &str) -> Result<Self, SchemaError> {
        let f = File::open(path).map_err(|_| SchemaError::TopicNotFound)?;
        serde_yaml::from_reader(f).map_err(|_| SchemaError::TopicNotFound)
    }
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct Schema {
    version: u16,
    schema_type: SchemaType,
    compatibility_mode: CompatibilityMode,
    // TODO: Actually parse the json schema
    schema: String,
}

/// # Errors
///
/// Will return `Err` if `topic` or `version` is not found or if schema data is invalid.
pub fn get_schema(topic: &str, _version: Option<u16>) -> Result<Schema, SchemaError> {
    let topic_path = format!("./topics/{topic}.yaml");
    let mut topic_data = TopicData::load(&topic_path)?;
    // TODO: Respect version
    let latest = topic_data
        .schemas
        .pop()
        .ok_or(SchemaError::InvalidVersion)?;
    if latest.schema_type != SchemaType::Json {
        return Err(SchemaError::InvalidType);
    }

    let json_schema_path = format!("./schemas/{}", latest.resource);

    Ok({
        Schema {
            version: latest.version,
            schema_type: latest.schema_type,
            compatibility_mode: latest.compatibility_mode,
            schema: read_to_string(json_schema_path).map_err(|_| SchemaError::InvalidSchema)?,
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
