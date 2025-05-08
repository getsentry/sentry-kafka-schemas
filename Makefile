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
	black python/ scripts/ docs/
	isort --overwrite-in-place python/ scripts/ docs/
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
	flake8 python/ scripts/ docs/
.PHONY: lint-python

lint-rust:
	cargo clippy --no-default-features --all-targets -- -W clippy::pedantic
	cargo clippy --all-features --all-targets -- -W clippy::pedantic
.PHONY: lint-rust

tests:
	pytest -n auto python/ -vv
.PHONY: tests

tests-rust:
	cargo test
.PHONY: tests-rust

install-docs:
	pip install -U -r python/requirements-doc.txt
.PHONY: install-docs

docs: install install-docs
	mkdir -p build/
	python docs/source/generate_services.py > build/services.rst.inc
	sphinx-build -b html docs/source docs/build
.PHONY: docs
