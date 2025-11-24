"""Pytest configuration and shared fixtures.

This file provides common fixtures and configuration for all tests.
"""

import random
import tempfile
from collections.abc import Generator
from pathlib import Path

import numpy as np
import pytest


@pytest.fixture(scope="session", autouse=True)
def set_random_seeds() -> None:
    """Set random seeds for reproducibility across all tests.

    This fixture runs automatically before all tests to ensure
    reproducible results in stochastic algorithms.
    """
    random.seed(42)
    np.random.seed(42)


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for test files.

    Yields:
        Path to a temporary directory that is automatically cleaned up.

    Example:
        >>> def test_file_operations(temp_dir):
        ...     test_file = temp_dir / "data.csv"
        ...     test_file.write_text("test data")
        ...     assert test_file.exists()
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_data() -> dict:
    """Provide sample data for testing.

    Returns:
        Dictionary containing various test data types.

    Example:
        >>> def test_processing(sample_data):
        ...     result = process(sample_data['array'])
        ...     assert len(result) > 0
    """
    return {
        "array": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
        "matrix": np.array([[1.0, 2.0], [3.0, 4.0]]),
        "list": [1, 2, 3, 4, 5],
        "dict": {"key1": "value1", "key2": "value2"},
    }


@pytest.fixture
def sample_csv_file(temp_dir: Path) -> Path:
    """Create a sample CSV file for testing.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path to the created CSV file

    Example:
        >>> def test_csv_reading(sample_csv_file):
        ...     data = read_csv(sample_csv_file)
        ...     assert len(data) == 3
    """
    csv_path = temp_dir / "sample.csv"
    csv_content = """name,value,category
item1,10.5,A
item2,20.3,B
item3,15.7,A
"""
    csv_path.write_text(csv_content)
    return csv_path


@pytest.fixture
def numerical_precision() -> float:
    """Provide numerical precision threshold for floating-point comparisons.

    Returns:
        Precision value for pytest.approx()

    Example:
        >>> def test_calculation(numerical_precision):
        ...     result = calculate_pi()
        ...     assert result == pytest.approx(3.14159, abs=numerical_precision)
    """
    return 1e-6


# Markers for categorizing tests
def pytest_configure(config: pytest.Config) -> None:
    """Register custom pytest markers.

    Args:
        config: Pytest configuration object
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "benchmark: marks tests as performance benchmarks")
    config.addinivalue_line("markers", "scientific: marks tests that validate scientific accuracy")
