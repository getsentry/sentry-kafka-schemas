.PHONY: install type-checking tests

install:
	pip install -e .
	pip install -r requirements-test.txt

type-checking:
	mypy python --strict --config-file python/mypy.ini

tests:
	pytest python -vv
