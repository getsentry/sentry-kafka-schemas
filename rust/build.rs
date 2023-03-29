use std::io::Write;

fn main() {
    if !std::path::Path::new("rust_codegen/Cargo.toml").is_file() {
        return;
    }

    let output = std::process::Command::new("cargo")
            .args(["run", "--manifest-path", "rust_codegen/Cargo.toml"])
            .output()
            .unwrap();

    std::io::stdout().write(&output.stdout).unwrap();
}
