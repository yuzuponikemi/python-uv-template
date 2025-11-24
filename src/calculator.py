"""Simple calculator module for demonstration purposes.

This module demonstrates test-driven development and type-safe Python code.
"""

from typing import Union


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b

    Examples:
        >>> add(2, 3)
        5
        >>> add(2.5, 3.5)
        6.0
    """
    return a + b


def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Subtract b from a.

    Args:
        a: First number
        b: Number to subtract

    Returns:
        Difference of a and b

    Examples:
        >>> subtract(5, 3)
        2
        >>> subtract(10.5, 2.5)
        8.0
    """
    return a - b


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b

    Examples:
        >>> multiply(3, 4)
        12
        >>> multiply(2.5, 4)
        10.0
    """
    return a * b


def divide(a: Union[int, float], b: Union[int, float]) -> float:
    """Divide a by b.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Quotient of a and b

    Raises:
        ValueError: If b is zero

    Examples:
        >>> divide(10, 2)
        5.0
        >>> divide(7, 2)
        3.5
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
    """Raise base to the power of exponent.

    Args:
        base: Base number
        exponent: Exponent

    Returns:
        base raised to the power of exponent

    Examples:
        >>> power(2, 3)
        8
        >>> power(2.5, 2)
        6.25
    """
    return base ** exponent
