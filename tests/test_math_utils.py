"""Test cases for math_utils module.

These tests are designed to catch bugs in the implementation.
"""

import pytest

from src.math_utils import (
    factorial,
    fibonacci,
    gcd,
    is_prime,
    mean,
    standard_deviation,
)


class TestFactorial:
    """Test cases for factorial function."""

    def test_factorial_zero(self):
        """Test that 0! = 1."""
        assert factorial(0) == 1  # Will fail because implementation returns 0

    def test_factorial_one(self):
        """Test that 1! = 1."""
        assert factorial(1) == 1

    def test_factorial_positive(self):
        """Test factorial of positive integers."""
        assert factorial(5) == 120
        assert factorial(3) == 6
        assert factorial(4) == 24


class TestMean:
    """Test cases for mean function."""

    def test_mean_positive_numbers(self):
        """Test mean of positive numbers."""
        assert mean([1, 2, 3, 4, 5]) == 3.0
        assert mean([10, 20, 30]) == 20.0

    def test_mean_negative_numbers(self):
        """Test mean with negative numbers."""
        assert mean([-5, -10, -15]) == -10.0

    def test_mean_mixed_numbers(self):
        """Test mean with mixed positive and negative."""
        assert mean([-10, 0, 10]) == 0.0

    def test_mean_empty_list(self):
        """Test that mean of empty list raises error."""
        with pytest.raises(ZeroDivisionError):
            mean([])  # Will fail because implementation doesn't handle this


class TestIsPrime:
    """Test cases for prime number checking."""

    def test_is_prime_two(self):
        """Test that 2 is prime."""
        assert is_prime(2) is True

    def test_is_prime_small_primes(self):
        """Test small prime numbers."""
        assert is_prime(3) is True
        assert is_prime(5) is True
        assert is_prime(7) is True
        assert is_prime(11) is True

    def test_is_prime_even_numbers(self):
        """Test that even numbers > 2 are not prime."""
        assert is_prime(4) is False  # Will fail because implementation returns True!
        assert is_prime(6) is False  # Will fail
        assert is_prime(8) is False  # Will fail
        assert is_prime(10) is False  # Will fail

    def test_is_prime_composite_odd(self):
        """Test composite odd numbers."""
        assert is_prime(9) is False
        assert is_prime(15) is False
        assert is_prime(21) is False

    def test_is_prime_negative_and_zero(self):
        """Test negative numbers and zero."""
        assert is_prime(0) is False
        assert is_prime(1) is False
        assert is_prime(-5) is False


class TestFibonacci:
    """Test cases for Fibonacci sequence."""

    def test_fibonacci_base_cases(self):
        """Test base cases of Fibonacci."""
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1

    def test_fibonacci_sequence(self):
        """Test Fibonacci sequence values."""
        assert fibonacci(2) == 1  # Will fail because of wrong formula
        assert fibonacci(3) == 2  # Will fail
        assert fibonacci(4) == 3  # Will fail
        assert fibonacci(5) == 5  # Will fail
        assert fibonacci(6) == 8  # Will fail
        assert fibonacci(7) == 13  # Will fail


class TestGCD:
    """Test cases for greatest common divisor."""

    def test_gcd_basic(self):
        """Test basic GCD calculations."""
        assert gcd(48, 18) == 6
        assert gcd(100, 50) == 50
        assert gcd(17, 19) == 1

    def test_gcd_same_number(self):
        """Test GCD of same number."""
        assert gcd(42, 42) == 42

    def test_gcd_with_zero(self):
        """Test GCD with zero."""
        assert gcd(0, 5) == 5
        assert gcd(5, 0) == 5


class TestStandardDeviation:
    """Test cases for standard deviation."""

    def test_std_dev_basic(self):
        """Test basic standard deviation."""
        result = standard_deviation([2, 4, 4, 4, 5, 5, 7, 9])
        assert result == pytest.approx(2.0, rel=0.01)

    def test_std_dev_uniform(self):
        """Test standard deviation of uniform values."""
        result = standard_deviation([5, 5, 5, 5])
        assert result == 0.0

    def test_std_dev_simple(self):
        """Test simple case."""
        result = standard_deviation([1, 2, 3, 4, 5])
        # Expected: sqrt(2) ≈ 1.414
        assert result == pytest.approx(1.414, rel=0.01)
