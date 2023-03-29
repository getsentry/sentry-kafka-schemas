#[must_use]
fn generate_schema(schema_path: &str, output_module: &str) -> String {
    println!("cargo:rerun-if-changed={schema_path}");
    let json = std::fs::read_to_string(schema_path).expect("Read schema JSON file");

    let schema = serde_json::from_str(&json).unwrap();
    let mut expander = schemafy_lib::Expander::new(
        None,
        "::schemafy_core::",
        &schema,
    );

    let code = expander.expand(&schema);

    format!("mod {output_module} {{ use serde::{Serialize, Deserialize}; {code} }}\n\n")
}

fn main() {
    let mut module_code = String::new();
    module_code.push_str("// @generated This file is generated via rust_codegen/src/main.rs\n\n");

    module_code.push_str(
        &generate_schema("schemas/ingest-metrics.v1.schema.json", "ingest_metrics_v1")
    );

    std::fs::write("rust/schema_types.rs", module_code).expect("Failed to write schema_types.rs");
}
