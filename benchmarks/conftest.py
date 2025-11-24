"""Pytest configuration for benchmarks."""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest for benchmark tests.

    Args:
        config: Pytest configuration object
    """
    config.addinivalue_line("markers", "benchmark: mark test as a performance benchmark")
