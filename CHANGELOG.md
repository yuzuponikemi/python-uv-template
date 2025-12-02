# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **CI/CD Improvements**
  - Dependency caching for uv, pip, and pre-commit (2-3x faster CI runs)
  - Bandit security checks in CI pipeline
  - Code coverage reporting via GitHub Actions Artifacts (30-day retention)
  - Pre-commit hooks execution in CI
  - Comprehensive test logs
  - Optional Python matrix testing (3.9, 3.10, 3.11, 3.12) - disabled by default to save CI minutes

- **Automated Dependency Management**
  - Dependabot configuration for weekly dependency updates
  - Automatic PR creation for Python packages, GitHub Actions, and pre-commit hooks
  - Grouped patch and minor updates for cleaner PR management

- **Release Automation**
  - Automatic GitHub Releases creation on version tags
  - Changelog generation from git commits
  - Package building (wheel + sdist)
  - Optional PyPI publishing support

- **Documentation**
  - Automatic documentation building with Sphinx
  - Documentation artifacts with 30-day retention
  - Optional GitHub Pages deployment (for public repos or GitHub Pro+)

- **Performance Monitoring**
  - Automated benchmark execution on PRs and main branch
  - Benchmark result comparison between PR and base branch
  - 90-day retention of benchmark results
  - JSON benchmark reports as artifacts

- **Cost Optimization**
  - All features work 100% free for private repositories using GitHub Free tier
  - Python testing limited to 3.11 by default (saves 75% CI minutes vs matrix testing)
  - No paid external services required (CodeCov, etc.)

### Changed
- **Cost Optimization**: Simplified CI to test only Python 3.11 by default (matrix testing optional)
- **Cost Optimization**: Removed CodeCov integration (use free GitHub Actions Artifacts instead)
- **Cost Optimization**: Disabled GitHub Pages deployment by default (optional for public repos)
- Enhanced CI to include comprehensive quality checks (ruff, mypy, bandit, pre-commit)
- Expanded README with detailed CI/CD documentation, cost information, and setup instructions

### Fixed
- Artifact naming in auto-fix workflow to match simplified CI structure

## [0.1.0] - 2024-12-02

### Added
- Initial template release
- uv-based dependency management
- Test-Driven Development (TDD) setup
- Claude Code integration for automated assistance
- Pre-commit hooks configuration
- Basic CI workflow
- Auto-fix workflow for CI failures
- Comprehensive project structure (src, tests, benchmarks, docs, examples)
- Makefile for common development tasks
- Ruff linting and formatting
- Mypy type checking
- pytest with coverage support

[Unreleased]: https://github.com/yuzuponikemi/python-uv-template/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yuzuponikemi/python-uv-template/releases/tag/v0.1.0
