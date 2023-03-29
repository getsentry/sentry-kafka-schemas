use typify::{TypeSpace, TypeSpaceSettings};

#[must_use]
fn generate_schema(schema_path: &str, output_module: &str) -> String {
    println!("cargo:rerun-if-changed={schema_path}");
    let json = std::fs::read_to_string(schema_path).expect("Read schema JSON file");

    let schema = serde_json::from_str::<schemars::schema::RootSchema>(&json).unwrap();

    let mut type_space = TypeSpace::new(TypeSpaceSettings::default().with_struct_builder(true));
    type_space.add_root_schema(schema).unwrap();

    let code = prettyplease::unparse(&syn::parse2::<syn::File>(type_space.to_stream()).unwrap());

    format!("pub mod {output_module} {{
    use serde::{{Deserialize, Serialize}};
    {code}
    }}")
}

fn main() {
    println!("cargo:rerun-if-changed=rust_codegen/src/main.rs");
    println!("cargo:rerun-if-changed=rust_codegen/Cargo.toml");

    let mut module_code = String::new();
    module_code.push_str("// @generated This file is generated via rust_codegen/src/main.rs\n\n");

    module_code.push_str(
        &generate_schema("schemas/ingest-metrics.v1.schema.json", "ingest_metrics_v1")
    );

    std::fs::write("rust/schema_types.rs", module_code).expect("Failed to write schema_types.rs");
}
