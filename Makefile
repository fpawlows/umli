setup:
	poetry install

test:
	poetry run pytest

tox-test:
	poetry run tox

docs:
	poetry run mkdocs serve

docs-build:
	poetry run mkdocs build

clean:
	rm -rf .tox
	rm -rf .pytest_cache
	rm -rf site
	rm -rf __pycache__
	rm -rf tests/.pytest_cache
	rm -rf tests/__pycache__

export:
	poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt

.PHONY: run clean docs clean export