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

fn generate_embedded_data() -> String {
    println!("cargo:rerun-if-changed=topics");
    println!("cargo:rerun-if-changed=schemas");

    let manifest_root = std::env::var("CARGO_MANIFEST_DIR").unwrap_or_default();
    let mut topics = enumerate_dir("topics");
    let mut schemas = enumerate_dir("schemas");
    let mut examples = enumerate_dir("examples");

    let mut code = String::new();
    use std::fmt::Write;
    let w = &mut code;

    writeln!(w, "const TOPICS: &[(&str, &str)] = &[").unwrap();
    let key_fn = |topic: &String| topic.strip_suffix(".yaml").unwrap().to_owned();
    topics.sort_by_key(key_fn);
    for topic in &topics {
        let key = key_fn(topic);
        let path = format!("{manifest_root}/topics/{topic}");
        writeln!(w, "    ({key:?}, include_str!({path:?})),").unwrap();
    }
    writeln!(w, "];\n").unwrap();

    writeln!(w, "const SCHEMAS: &[(&str, &str)] = &[").unwrap();
    let key_fn = |schema: &String| schema.clone();
    schemas.sort_by_key(key_fn);
    for schema in &schemas {
        let key = key_fn(schema);
        let path = format!("{manifest_root}/schemas/{schema}");
        writeln!(w, "    ({key:?}, include_str!({path:?})),").unwrap();
    }
    writeln!(w, "];").unwrap();

    let mut last_prefix = None;
    writeln!(w, "const EXAMPLES: &[(&str, &[crate::Example])] = &[").unwrap();
    let key_fn = |example: &String| {
        let last_slash = example.rfind('/').unwrap();
        let (prefix, _name) = example.split_at(last_slash + 1);
        prefix.to_owned()
    };
    examples.sort_by_key(key_fn);

    for example in &examples {
        let prefix = key_fn(example);
        match last_prefix {
            None => {
                writeln!(w, "    ({prefix:?}, &[").unwrap();
            }
            Some(last_prefix) if last_prefix != prefix => {
                writeln!(w, "    ]),").unwrap();
                writeln!(w, "    ({prefix:?}, &[").unwrap();
            }
            _ => {}
        }
        last_prefix = Some(prefix);
        let path = format!("{manifest_root}/examples/{example}");
        writeln!(
            w,
            "        crate::Example {{ name: {example:?}, payload: include_bytes!({path:?}) }},"
        )
        .unwrap();
    }
    writeln!(w, "    ]),").unwrap();
    writeln!(w, "];").unwrap();

    code
}

fn enumerate_dir(dir: &str) -> Vec<String> {
    let mut files = vec![];

    fn collect_files(files: &mut Vec<String>, dir: &Path, prefix: &str) {
        for entry in std::fs::read_dir(dir).unwrap() {
            let entry = entry.unwrap();
            let name = entry.file_name().into_string().unwrap();
            let name = if prefix.is_empty() {
                name
            } else {
                format!("{prefix}/{name}")
            };
            let ty = entry.file_type().unwrap();
            if ty.is_dir() {
                collect_files(files, &entry.path(), &name)
            } else if ty.is_file() {
                files.push(name);
            }
        }
    }

    collect_files(&mut files, dir.as_ref(), "");

    files
}

fn main() {
    let module_code = {
        #[cfg(feature = "type_generation")]
        {
            generate_schema("schemas/ingest-metrics.v1.schema.json", "ingest_metrics_v1")
        }
        #[cfg(not(feature = "type_generation"))]
        {
            String::new()
        }
    };

    let embedded_data = generate_embedded_data();

    if let Ok(target_dir) = std::env::var("OUT_DIR") {
        println!("cargo:rerun-if-changed=rust/build.rs");

        std::fs::write(Path::new(&target_dir).join("schema_types.rs"), module_code)
            .expect("Failed to write schema_types.rs");

        std::fs::write(
            Path::new(&target_dir).join("embedded_data.rs"),
            embedded_data,
        )
        .expect("Failed to write embedded_data.rs");
    } else {
        println!("### embedded_data.rs");
        println!("{embedded_data}");

        println!("### schema_types.rs");
        println!("{module_code}");
    }
}
