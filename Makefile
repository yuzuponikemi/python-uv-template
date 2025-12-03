.PHONY: help compile install test lint format type-check clean docs benchmark all ci ci-local act-setup

# Default target: show help
help:
	@echo "Available commands:"
	@echo "  make lock           Update uv.lock file"
	@echo "  make sync           Sync dependencies from uv.lock"
	@echo "  make install        Install all dependencies (alias for sync)"
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
	@echo "  make ci-local       Run GitHub Actions CI locally with act"
	@echo "  make act-setup      Setup act configuration files"
	@echo "  make all            Run format, lint, type-check, and test"

# Update lockfile
lock:
	uv lock
	@echo "✓ uv.lock updated"

# Sync dependencies from lockfile (installs exactly what's in uv.lock)
sync:
	uv sync --all-extras
	@echo "✓ Dependencies synced from uv.lock"

# Install dependencies (alias for sync)
install: sync

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
	mypy --ignore-missing-imports

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

# Setup act configuration files
act-setup:
	@echo "Setting up act configuration..."
	@if [ ! -f .secrets ]; then \
		cp .secrets.example .secrets; \
		echo "✓ Created .secrets file (please edit with your actual secrets)"; \
	else \
		echo "✓ .secrets file already exists"; \
	fi
	@if [ ! -f .github/workflows/.env.local ]; then \
		cp .github/workflows/.env.local.example .github/workflows/.env.local; \
		echo "✓ Created .env.local file"; \
	else \
		echo "✓ .env.local file already exists"; \
	fi
	@echo "✓ Act setup complete! See LOCAL_TESTING.md for usage instructions"

# Run GitHub Actions CI locally with act
ci-local:
	@echo "Running GitHub Actions CI locally with act..."
	@if ! command -v act > /dev/null 2>&1; then \
		echo "Error: act is not installed. Please install it first:"; \
		echo "  macOS: brew install act"; \
		echo "  Linux: curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"; \
		echo "  See LOCAL_TESTING.md for more details"; \
		exit 1; \
	fi
	@if ! command -v docker > /dev/null 2>&1; then \
		echo "Error: Docker is not installed or not running."; \
		echo "Please install and start Docker first."; \
		exit 1; \
	fi
	@if ! docker ps > /dev/null 2>&1; then \
		echo "Error: Docker daemon is not running."; \
		echo "Please start Docker first."; \
		exit 1; \
	fi
	@if [ ! -f .secrets ]; then \
		echo "Warning: .secrets file not found. Running act-setup..."; \
		$(MAKE) act-setup; \
	fi
	act push -j test
	@echo "✓ Local CI completed!"
