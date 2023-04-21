use serde_json::Value;
use std::fmt::Write;
use std::fs::read_to_string;


fn test_examples(schema_file: &str, example_file: &str) {
    let jsonschema_value: Value = serde_json::from_str(&read_to_string(schema_file).unwrap()).unwrap();
    let schema = jsonschema::JSONSchema::compile(&jsonschema_value).unwrap();

    let message_value: Value = serde_json::from_str(&read_to_string(example_file).unwrap()).unwrap();
    let result = schema.validate(&message_value);
    if let Err(e) = result {
        let mut result = String::new();
        for error in e {
            writeln!(result, "{}", error).unwrap();
        }

        panic!("{result}");
    }
}

script_macro::run_script!(r##"
    let output = "";

    fn produce_test(topic, version, resource, example_file) {
        let fn_name = slugify_ident(`test_example_${topic}_v${version}_${example_file.to_string()}`);
        return `
        #[test]
        fn ${fn_name}() {
            test_examples("schemas/${resource}", "${example_file}");
        }
        `;
    }

    for topic_filename in open_dir("topics/") {
        let topic_yaml = parse_yaml(open_file(topic_filename).read_string());

        let topic = topic_filename.to_string().split('/')[-1];
        topic.replace(".yaml", "");

        for schema in topic_yaml["schemas"] {
            let version = schema["version"];

            for example_entry_str in schema["examples"] {
                let example_entry = path("examples/" + example_entry_str);

                for file in open_dir(example_entry) {
                    output += produce_test(topic, version, schema["resource"], file);
                }
            }
        }
    }

    return output;
"##);
