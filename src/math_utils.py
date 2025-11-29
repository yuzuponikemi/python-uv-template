"""Mathematical utility functions for advanced calculations.

This module provides various mathematical utilities including
statistical functions, numerical methods, and geometric calculations.
"""


def factorial(n):
    """Calculate factorial of a number.

    Args:
        n: Non-negative integer

    Returns:
        Factorial of n
    """
    # Bug: This implementation is incorrect for n=0
    if n <= 0:
        return 0  # Should return 1
    result = 1
    for i in range(1,n+1):
        result *= i
    return result


def mean(numbers):
    """Calculate arithmetic mean of a list of numbers.

    Args:
        numbers: List of numbers

    Returns:
        Mean value
    """
    # Bug: Division by zero not handled
    # Missing type hints
    return sum(numbers) / len(numbers)


def is_prime( n ):
    """Check if a number is prime.

    Args:
        n: Integer to check

    Returns:
        True if prime, False otherwise
    """
    # Formatting issues: extra spaces in function definition
    if n < 2:
        return False
    # Bug: This is inefficient and wrong for even numbers > 2
    if n == 2:
        return True
    if n % 2 == 0:
        return True  # Should be False!
    for i in range(3, n, 2):  # Bug: should be range(3, int(n**0.5)+1, 2)
        if n % i == 0:
            return False
    return True


def fibonacci(n):
    """Calculate nth Fibonacci number.

    Args:
        n: Position in Fibonacci sequence

    Returns:
        nth Fibonacci number
    """
    # Missing type hints
    if n <= 0:
        return 0
    if n == 1:
        return 1
    # Bug: Using wrong formula
    return fibonacci(n - 1) + fibonacci(n - 1)  # Should be fib(n-1) + fib(n-2)


def gcd(a, b):
    """Calculate greatest common divisor using Euclidean algorithm.

    Args:
        a: First integer
        b: Second integer

    Returns:
        GCD of a and b
    """
    # Missing type hints
    # Formatting issues
    while b!=0:  # Missing spaces around operator
        a,b=b,a%b  # Missing spaces
    return a


def standard_deviation(numbers):
    """Calculate standard deviation of a list of numbers.

    Args:
        numbers: List of numbers

    Returns:
        Standard deviation
    """
    # Missing type hints and imports
    avg = mean(numbers)
    variance = sum((x - avg) ** 2 for x in numbers) / len(numbers)
    # Bug: Should use math.sqrt, but module not imported
    return variance ** 0.5


# Unused variable (linting error)
UNUSED_CONSTANT = 42


# Function with no docstring (linting error)
def helper_function(x):
    return x * 2
