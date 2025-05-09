use serde::Deserialize;
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

#[derive(Debug, Deserialize)]
struct TopicData {
    schemas: Vec<SchemaData>,
}

#[derive(Debug, Deserialize)]
struct SchemaData {
    #[serde(rename = "type")]
    schema_type: String,
    resource: String,
}

fn mangle_resource_name(resource: &str) -> String {
    // Remove the foo_pb2 module name.
    // While python codegen includes the module name,
    // generated rust code does not.
    let parts: Vec<&str> = resource
        .split(".")
        .filter(|part| !part.ends_with("_pb2"))
        .collect();
    parts.join("::")
}

fn generate_proto_shim() -> String {
    let mut imports = String::new();
    let mut tuples = String::new();
    let mut imported_resources = std::collections::HashSet::new();
    use std::fmt::Write;

    writeln!(imports, "use std::any::Any;").unwrap();
    writeln!(imports, "use prost::Message;").unwrap();

    let topics = enumerate_dir("topics");
    let manifest_root = std::env::var("CARGO_MANIFEST_DIR").unwrap_or_default();
    let mut resources: Vec<String> = Vec::new();

    for topic in &topics {
        let path = format!("{manifest_root}/topics/{topic}");
        let yaml_data = std::fs::read_to_string(&path).unwrap();

        let yaml_result: Result<TopicData, _> = serde_yaml::from_str(&yaml_data);
        if yaml_result.is_err() {
            continue;
        }
        let topic_data = yaml_result.unwrap();
        let schema_version = topic_data.schemas.first().unwrap();
        if schema_version.schema_type != "protobuf" {
            continue;
        }
        let resource = schema_version.resource.clone();

        resources.push(resource);
    }

    resources.sort();

    for resource in &resources {
        let struct_path = mangle_resource_name(&resource);
        let struct_name = struct_path.split("::").last().unwrap();

        // Only add import if we haven't seen the resource before
        if imported_resources.insert(struct_path.clone()) {
            writeln!(imports, "use {struct_path};").unwrap();
        }

        writeln!(tuples, "    (\"{resource}\", |input: &[u8]| {{").unwrap();
        writeln!(tuples, "        let parsed = {struct_name}::decode(input);").unwrap();
        writeln!(tuples, "        match parsed {{").unwrap();
        writeln!(
            tuples,
            "            Ok(value) => Ok(Box::new(value) as Box<dyn Any>),"
        )
        .unwrap();
        writeln!(tuples, "            Err(err) => Err(err),").unwrap();
        writeln!(tuples, "        }}").unwrap();
        writeln!(tuples, "    }}),").unwrap();
    }

    let mut code = String::new();

    writeln!(code).unwrap();
    writeln!(code).unwrap();
    writeln!(code, "// Imports for protobuf topic schemas").unwrap();
    code.push_str(&imports);
    writeln!(code).unwrap();
    writeln!(code, "pub const PROTOS: &[(&str, fn(input: &[u8]) -> Result<Box<dyn Any>, prost::DecodeError>)] = &[").unwrap();
    code.push_str(&tuples);
    writeln!(code, "];").unwrap();

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
            let mut code =
                generate_schema("schemas/ingest-metrics.v1.schema.json", "ingest_metrics_v1");
            let proto_code = generate_proto_shim();
            code.push_str(&proto_code);

            code
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
