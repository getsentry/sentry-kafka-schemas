.PHONY: install format type-checking tests types clean build

clean:
	rm -rf python/sentry_kafka_schemas/schema_types/

python/sentry_kafka_schemas/schema_types: schemas/ topics/
	pip install -r python/requirements-build.txt
	python python/generate_python_types.py

build: python/sentry_kafka_schemas/schema_types
	pip install wheel
	python setup.py sdist bdist_wheel

install: python/sentry_kafka_schemas/schema_types
	pip install -e .
	pip install -r python/requirements-test.txt

format:
	black tests/ python/

type-checking:
	mypy tests/ python/ --strict --config-file python/mypy.ini

types: type-checking

lint:
	flake8 tests/ python/
	black --check tests/ python/

tests:
	pytest tests/ python/ -vv
