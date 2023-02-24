.PHONY: install type-checking tests

install:
	cd python && pip install -e
	cd python && pip install -r python/requirements-test.txt

type-checking:
	mypy python --strict --config-file python/mypy.ini

tests:
	pytest python -vv
