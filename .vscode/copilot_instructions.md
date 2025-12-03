# **Standing Instructions: Modern Python Project Management with uv**

This document outlines the strict, mandatory guidelines for managing Python projects. The **sole and exclusive tool** for all virtual environment and package management tasks is **uv**.

This project uses **uv's native project management features** for superior dependency management, leveraging `pyproject.toml` and `uv.lock` for reproducible, fast, and reliable builds.

### **Golden Rule: uv is the Only Tool**

For any task involving Python virtual environments or packages, you **MUST** use the uv command-line tool. You **MUST NOT** use `python -m venv`, `pip`, or any other package manager unless explicitly instructed for a specific, exceptional reason.

## **The Core Workflow: Native uv Project Management**

This workflow leverages uv's built-in project management capabilities for maximum performance and reproducibility.

### **Step 1: Define Dependencies in pyproject.toml**

The project's dependencies **MUST** be declared in `pyproject.toml`. This is the single source of truth for all dependencies.

**✅ Example pyproject.toml:**

```toml
[project]
name = "my-project"
version = "0.1.0"
dependencies = [
    "pandas>=2.0.0",
    "fastapi>=0.100.0",
    "httpx[http2]>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.3.0",
    "mypy>=1.8.0",
]
```

### **Step 2: Generate Lockfile with uv lock**

After modifying `pyproject.toml`, you **MUST** update the lockfile `uv.lock`. This file ensures deterministic, reproducible builds with cryptographic hash verification.

**✅ DO THIS:**

```bash
uv lock
```

The resulting `uv.lock` will contain every direct and transitive dependency with exact versions and hashes. It **MUST NOT** be edited by hand.

### **Step 3: Sync Environment with uv sync**

To install dependencies into a virtual environment, you **MUST** use `uv sync`. This command:
- Creates or updates the virtual environment automatically
- Installs exactly what's in `uv.lock`
- Removes any packages not in the lockfile (prevents drift)
- Runs in parallel for 10-100x faster installs than pip

**✅ DO THIS:**

```bash
# Sync with all optional dependencies
uv sync --all-extras

# Or sync with specific optional dependencies
uv sync --extra dev
```

## **Common Operations**

### **Initial Project Setup (for a new collaborator)**

1. Clone the repository.
2. Sync dependencies from the lockfile (uv handles venv creation automatically):
   ```bash
   uv sync --all-extras
   ```

That's it! uv creates the virtual environment and installs all dependencies in one command.

### **Adding a New Package**

1. Edit `pyproject.toml` to add the new package:
   ```toml
   [project]
   dependencies = [
       "pandas>=2.0.0",
       "polars>=0.20.0",  # New package
   ]
   ```

2. Update the lockfile:
   ```bash
   uv lock
   ```

3. Sync the environment:
   ```bash
   uv sync --all-extras
   ```

### **Updating All Packages**

1. Update all packages to their latest allowed versions:
   ```bash
   uv lock --upgrade
   ```

2. Sync the environment:
   ```bash
   uv sync --all-extras
   ```

### **Running Scripts**

Use `uv run` to execute Python scripts in the project environment:

```bash
# Run a Python script
uv run python scripts/process_data.py

# Run pytest
uv run pytest

# Run any command in the project environment
uv run mypy src/
```

**Benefits of uv run:**
- No need to manually activate virtual environment
- Automatically uses the correct environment
- Works across all platforms

## **Version Control (GitHub) Policy**

You **MUST** commit the following files to the Git repository:

1. **pyproject.toml**: This tracks all project metadata and dependencies.
2. **uv.lock**: This is the generated lockfile that ensures reproducible builds for all collaborators and CI/CD pipelines.
3. **.python-version**: Specifies the Python version for the project.

The `.venv` directory **MUST** be added to the `.gitignore` file.

### **❌ Forbidden Commands ❌**

Under this workflow, you **MUST NEVER** use the following commands:

* `pip install ...`
* `pip freeze ...`
* `python -m venv ...`
* `uv pip install ...` (use `uv sync` instead)
* Manually editing `uv.lock` or `requirements.txt`

## **Benefits of uv Native Project Management**

1. **10-100x Faster**: Parallel downloads and installs
2. **Cryptographic Verification**: Hash-based integrity checks
3. **Automatic Cleanup**: Removes stale packages automatically
4. **Built-in Caching**: Optimized caching in CI/CD
5. **No Manual venv Management**: uv handles it automatically
6. **Single Source of Truth**: All configuration in `pyproject.toml`
7. **Better Reproducibility**: Exact versions and hashes in `uv.lock`

## **Makefile Commands**

This project provides convenient Make targets:

```bash
make sync     # Sync dependencies from uv.lock
make lock     # Update uv.lock file
make test     # Run tests
make lint     # Run linter
make format   # Format code
make ci       # Run all CI checks locally
```
