"""Test cases for calculator module.

Following TDD principles, these tests validate the calculator functionality.
"""

import pytest
from src.calculator import add, subtract, multiply, divide, power


class TestAdd:
    """Test cases for addition function."""

    def test_add_positive_integers(self):
        """Test addition of positive integers."""
        assert add(2, 3) == 5
        assert add(10, 20) == 30

    def test_add_negative_integers(self):
        """Test addition with negative integers."""
        assert add(-5, 3) == -2
        assert add(-10, -20) == -30

    def test_add_floats(self):
        """Test addition of floating point numbers."""
        assert add(2.5, 3.5) == 6.0
        assert add(1.1, 2.2) == pytest.approx(3.3)

    def test_add_zero(self):
        """Test addition with zero."""
        assert add(0, 5) == 5
        assert add(5, 0) == 5
        assert add(0, 0) == 0


class TestSubtract:
    """Test cases for subtraction function."""

    def test_subtract_positive_integers(self):
        """Test subtraction of positive integers."""
        assert subtract(5, 3) == 2
        assert subtract(20, 10) == 10

    def test_subtract_negative_integers(self):
        """Test subtraction with negative integers."""
        assert subtract(-5, 3) == -8
        assert subtract(5, -3) == 8

    def test_subtract_floats(self):
        """Test subtraction of floating point numbers."""
        assert subtract(10.5, 2.5) == 8.0
        assert subtract(5.5, 3.3) == pytest.approx(2.2)


class TestMultiply:
    """Test cases for multiplication function."""

    def test_multiply_positive_integers(self):
        """Test multiplication of positive integers."""
        assert multiply(3, 4) == 12
        assert multiply(5, 6) == 30

    def test_multiply_negative_integers(self):
        """Test multiplication with negative integers."""
        assert multiply(-3, 4) == -12
        assert multiply(-3, -4) == 12

    def test_multiply_floats(self):
        """Test multiplication of floating point numbers."""
        assert multiply(2.5, 4) == 10.0
        assert multiply(1.5, 2.5) == pytest.approx(3.75)

    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        assert multiply(5, 0) == 0
        assert multiply(0, 5) == 0


class TestDivide:
    """Test cases for division function."""

    def test_divide_positive_integers(self):
        """Test division of positive integers."""
        assert divide(10, 2) == 5.0
        assert divide(15, 3) == 5.0

    def test_divide_floats(self):
        """Test division of floating point numbers."""
        assert divide(7.5, 2.5) == 3.0
        assert divide(10, 4) == 2.5

    def test_divide_by_zero_raises_error(self):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_zero_by_number(self):
        """Test division of zero by a number."""
        assert divide(0, 5) == 0.0


class TestPower:
    """Test cases for power function."""

    def test_power_positive_integers(self):
        """Test power with positive integers."""
        assert power(2, 3) == 8
        assert power(5, 2) == 25

    def test_power_with_zero_exponent(self):
        """Test power with zero exponent."""
        assert power(5, 0) == 1
        assert power(100, 0) == 1

    def test_power_with_negative_exponent(self):
        """Test power with negative exponent."""
        assert power(2, -1) == 0.5
        assert power(4, -2) == 0.0625

    def test_power_floats(self):
        """Test power with floating point numbers."""
        assert power(2.5, 2) == 6.25
        assert power(9, 0.5) == 3.0
