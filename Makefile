.PHONY: install format type-checking tests

install:
	pip install -e .
	pip install -r python/requirements-test.txt

format:
	black tests/ python/

type-checking:
	mypy tests/ python/ --strict --config-file python/mypy.ini

lint:
	flake8 tests/ python/
	black --check tests/ python/

tests:
	pytest tests/ python/ -vv
