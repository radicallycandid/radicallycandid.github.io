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
	uv sync

## Install with dev dependencies
install-dev:
	uv sync --extra dev

## Run tests
test:
	uv run pytest

## Run tests with coverage report
coverage:
	uv run pytest --cov=build --cov-report=term-missing

## Run linter and format check
lint:
	uv run ruff check .
	uv run ruff format --check .

## Run type checker (strict)
typecheck:
	uv run mypy build.py tests

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
