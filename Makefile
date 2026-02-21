# vmargato.com - Common Operations
# Usage: make [target]

.PHONY: build serve clean install test coverage lint typecheck help

# Default target
.DEFAULT_GOAL := help

## Build the static site
build:
	python build.py build

## Build and start local development server
serve:
	python build.py serve

## Remove output directory
clean:
	python build.py clean

## Install dependencies
install:
	pip install -r requirements.txt

## Install with dev dependencies
install-dev:
	pip install -e ".[dev]"

## Run tests
test:
	pytest

## Run tests with coverage report
coverage:
	pytest --cov=build --cov-report=term-missing

## Run linter (requires ruff)
lint:
	ruff check build.py

## Run type checker (requires mypy)
typecheck:
	mypy build.py

## Show this help message
help:
	@echo "vmargato.com - Static Site Generator"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## /  /'
	@echo ""
	@grep -E '^[a-zA-Z_-]+:' $(MAKEFILE_LIST) | grep -v '.PHONY' | sed 's/:.*//' | sort | sed 's/^/  make /'
