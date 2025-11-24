.PHONY: help install test lint format type-check clean docs benchmark all ci

# Default target: show help
help:
	@echo "Available commands:"
	@echo "  make install        Install all dependencies"
	@echo "  make test           Run all tests"
	@echo "  make test-fast      Run tests (skip slow tests)"
	@echo "  make test-cov       Run tests with coverage report"
	@echo "  make lint           Run linter (ruff)"
	@echo "  make format         Format code with ruff"
	@echo "  make type-check     Run type checker (mypy)"
	@echo "  make clean          Remove generated files"
	@echo "  make docs           Build documentation"
	@echo "  make docs-serve     Serve documentation locally"
	@echo "  make benchmark      Run performance benchmarks"
	@echo "  make ci             Run all CI checks locally"
	@echo "  make all            Run format, lint, type-check, and test"

# Install dependencies
install:
	uv pip install --system -r requirements.txt
	uv pip install --system -r requirements-dev.txt

# Run all tests
test:
	pytest

# Run fast tests only (skip slow tests)
test-fast:
	pytest -m "not slow"

# Run tests with coverage report
test-cov:
	pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Run linter
lint:
	ruff check .

# Format code
format:
	ruff format .
	ruff check --fix .

# Run type checker
type-check:
	mypy src tests

# Clean generated files
clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Build documentation
docs:
	cd docs && make html
	@echo "Documentation built in docs/_build/html/index.html"

# Serve documentation locally
docs-serve:
	cd docs && python -m http.server --directory _build/html 8000

# Run benchmarks
benchmark:
	pytest benchmarks/ -v --benchmark-only

# Run all CI checks locally (same as GitHub Actions)
ci: format lint type-check test
	@echo "✓ All CI checks passed!"

# Run all checks
all: format lint type-check test
	@echo "✓ All checks completed!"
