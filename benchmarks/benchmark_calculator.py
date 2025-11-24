"""Benchmark tests for calculator module.

Run with:
    pytest benchmarks/ -v --benchmark-only
    pytest benchmarks/ -v --benchmark-compare
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from calculator import add, divide, multiply, power, subtract


class TestCalculatorBenchmarks:
    """Benchmark tests for calculator functions."""

    @pytest.mark.benchmark
    def test_benchmark_add(self, benchmark):
        """Benchmark addition operation."""
        result = benchmark(add, 1000, 2000)
        assert result == 3000

    @pytest.mark.benchmark
    def test_benchmark_subtract(self, benchmark):
        """Benchmark subtraction operation."""
        result = benchmark(subtract, 1000, 2000)
        assert result == -1000

    @pytest.mark.benchmark
    def test_benchmark_multiply(self, benchmark):
        """Benchmark multiplication operation."""
        result = benchmark(multiply, 1000, 2000)
        assert result == 2000000

    @pytest.mark.benchmark
    def test_benchmark_divide(self, benchmark):
        """Benchmark division operation."""
        result = benchmark(divide, 1000, 2000)
        assert result == 0.5

    @pytest.mark.benchmark
    def test_benchmark_power(self, benchmark):
        """Benchmark power operation."""
        result = benchmark(power, 2, 10)
        assert result == 1024


class TestCalculatorBenchmarksArray:
    """Benchmark tests for calculator with array operations."""

    @pytest.mark.benchmark
    def test_benchmark_add_array(self, benchmark):
        """Benchmark addition with arrays."""
        a = np.random.rand(1000)
        b = np.random.rand(1000)

        def add_arrays():
            return np.array([add(x, y) for x, y in zip(a, b)])

        result = benchmark(add_arrays)
        assert len(result) == 1000

    @pytest.mark.benchmark
    def test_benchmark_multiply_array(self, benchmark):
        """Benchmark multiplication with arrays."""
        a = np.random.rand(1000)
        b = np.random.rand(1000)

        def multiply_arrays():
            return np.array([multiply(x, y) for x, y in zip(a, b)])

        result = benchmark(multiply_arrays)
        assert len(result) == 1000

    @pytest.mark.benchmark
    def test_benchmark_power_array(self, benchmark):
        """Benchmark power operation with arrays."""
        base = np.random.rand(100) * 10
        exponent = 2

        def power_arrays():
            return np.array([power(b, exponent) for b in base])

        result = benchmark(power_arrays)
        assert len(result) == 100


class TestCalculatorBenchmarksComparison:
    """Benchmark tests comparing different implementations."""

    @pytest.mark.benchmark(group="comparison")
    def test_benchmark_custom_add(self, benchmark):
        """Benchmark custom add function."""
        a = np.random.rand(1000)
        b = np.random.rand(1000)
        benchmark(lambda: np.array([add(x, y) for x, y in zip(a, b)]))

    @pytest.mark.benchmark(group="comparison")
    def test_benchmark_numpy_add(self, benchmark):
        """Benchmark NumPy's native add."""
        a = np.random.rand(1000)
        b = np.random.rand(1000)
        benchmark(lambda: a + b)


# Pytest benchmark configuration
pytest_benchmark_config = {
    "disable_gc": True,
    "min_rounds": 5,
    "max_time": 1.0,
    "calibration_precision": 10,
}
