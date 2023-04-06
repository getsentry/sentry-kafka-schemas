use std::path::Path;

#[cfg(feature = "type_generation")]
use {
    schemars::schema::Schema,
    typify::{TypeSpace, TypeSpaceSettings},
};

#[cfg(feature = "type_generation")]
fn generate_schema(schema_path: &str, output_module: &str) -> String {
    println!("cargo:rerun-if-changed={schema_path}");
    let json = std::fs::read_to_string(schema_path).expect("Read schema JSON file");

    let schema = serde_json::from_str::<schemars::schema::RootSchema>(&json).unwrap();

    let mut type_space = TypeSpace::new(TypeSpaceSettings::default().with_struct_builder(true));

    // TODO: when typify 0.12 is released, replace this entire block with add_root_schema
    // see https://github.com/oxidecomputer/typify/pull/236/files
    {
        type_space.add_ref_types(schema.definitions).unwrap();

        type_space.add_type(&Schema::Object(schema.schema)).unwrap();
    }

    let code = prettyplease::unparse(&syn::parse2::<syn::File>(type_space.to_stream()).unwrap());

    // XXX: extreme hack to get rid of all hashmaps. we generally use btreemap for representation
    // of most (small) maps
    //
    // some customization in typify would be nice, but we really use hashmap very rarely.
    let code = code
        .replace("::HashMap<", "::BTreeMap<")
        .replace("::HashMap::", "::BTreeMap::");

    format!(
        "pub mod {output_module} {{
    use serde::{{Deserialize, Serialize}};
    {code}
    }}"
    )
}

fn main() {
    #[allow(unused_mut)]
    let mut module_code = String::new();

    #[cfg(feature = "type_generation")]
    {
        module_code.push_str(&generate_schema(
            "schemas/ingest-metrics.v1.schema.json",
            "ingest_metrics_v1",
        ));
    }

    if let Ok(target_dir) = std::env::var("OUT_DIR") {
        println!("cargo:rerun-if-changed=build.rs");
        std::fs::write(Path::new(&target_dir).join("schema_types.rs"), module_code)
            .expect("Failed to write schema_types.rs");
    } else {
        println!("{module_code}");
    }
}
