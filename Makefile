clean:
	rm -rf python/sentry_kafka_schemas/schema_types/ *.egg-info dist/
.PHONY: clean

install-build-requirements:
	pip install -r python/requirements-build.txt
	# the script also imports the python library, so dependencies need to be preinstalled
	pip install -r python/requirements.txt
.PHONY: install-build-requirements

python/sentry_kafka_schemas/schema_types: schemas/ topics/ install-build-requirements
	python python/generate_python_types.py

build: python/sentry_kafka_schemas/schema_types
	pip install wheel
	python setup.py sdist bdist_wheel
.PHONY: build

install: python/sentry_kafka_schemas/schema_types
	pip install -e .
	pip install -r python/requirements-test.txt
.PHONY: install

format:
	black python/
.PHONY: format

type-checking:
	mypy python/ --strict --config-file python/mypy.ini
.PHONY: type-checking

lint: lint-rust lint-python
.PHONY: lint

lint-python: lint-python-format type-checking
	flake8 python/
.PHONY: lint-python

lint-python-format: 
	black --check python/
.PHONY: lint-format-python

lint-rust:
	cargo clippy -- -W clippy::pedantic
.PHONY: lint-rust

tests:
	pytest -n auto python/ -vv
.PHONY: tests
