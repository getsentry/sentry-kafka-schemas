clean:
	rm -rf python/sentry_kafka_schemas/schema_types/ *.egg-info dist/
.PHONY: clean

install-build-requirements:
	pip install -r python/requirements-build.txt
	# the script also imports the python library, so dependencies need to be preinstalled
	pip install -r python/requirements.txt
	yarn
.PHONY: install-build-requirements

python/sentry_kafka_schemas/schema_types: schemas/ topics/ install-build-requirements
	python python/generate_python_types.py

rust/schema_types.rs:
	cargo run --manifest-path rust_codegen/Cargo.toml
.PHONY: rust/schema_types.rs

view-rust-types:
	cargo run --features build_deps --bin generate-schema-types
.PHONY: view-rust-types

build: python/sentry_kafka_schemas/schema_types
	pip install wheel
	python setup.py sdist bdist_wheel
.PHONY: build

install: python/sentry_kafka_schemas/schema_types
	pip install -e .
	pip install -r python/requirements-test.txt
.PHONY: install

format:
	black python/ scripts/
	cargo fmt
	yarn prettier --write .
.PHONY: format

type-checking:
	mypy scripts/ python/ --strict --config-file python/mypy.ini
.PHONY: type-checking

types: type-checking
.PHONY: types

lint: lint-python
.PHONY: lint

lint-python:
	flake8 python/ scripts/
.PHONY: lint-python

lint-rust:
	cargo clippy -- -W clippy::pedantic
.PHONY: lint-rust

tests:
	pytest -n auto python/ -vv
.PHONY: tests
