.PHONY: install tests type-checking

install:
	pip install -e .
	pip install -r python/requirements-test.txt

type-checking:
	mypy python --strict --config-file python/mypy.ini

tests:
	pytest python -vv
