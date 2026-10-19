#!/usr/bin/env python3
"""
recursion_intro.py
CS 101 — Week 3, Lab 3
First recursive functions. Visualize each one in Python Tutor.
"""


def factorial(n):
    """
    Return n! using recursion.
    Base case: factorial(0) = 1
    Recursive case: factorial(n) = n * factorial(n-1)
    """
    assert n >= 0 and isinstance(n, int)
    if n == 0:
        return 1
    return n * factorial(n - 1)


def count_down(n):
    """
    Print n, n-1, n-2, ..., 1, 0 using recursion.
    Base case: count_down(0) prints 0 and stops.
    Recursive case: print n, then count_down(n-1).
    """
    print(n)
    if n > 0:
        count_down(n - 1)


def power(base, exp):
    """
    Compute base**exp using recursion (exp is a non-negative integer).
    Base case: power(base, 0) = 1
    Recursive case: power(base, exp) = base * power(base, exp - 1)
    """
    assert exp >= 0 and isinstance(exp, int)
    if exp == 0:
        return 1
    return base * power(base, exp - 1)


def sum_digits(n):
    """
    Return the sum of digits of non-negative integer n using recursion.
    Base case: single digit → return n
    Recursive case: last digit (n%10) + sum_digits(n//10)

    sum_digits(1234) → 10
    """
    assert n >= 0 and isinstance(n, int)
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)


# Tests:
assert factorial(0) == 1
assert factorial(5) == 120
assert factorial(10) == 3628800
print("✓ factorial")

assert power(2, 0) == 1
assert power(2, 10) == 1024
assert power(3, 4) == 81
print("✓ power")

assert sum_digits(0) == 0
assert sum_digits(9) == 9
assert sum_digits(1234) == 10
assert sum_digits(9999) == 36
print("✓ sum_digits")

print("\nVisualize in Python Tutor:")
print("  factorial(5) — count how deep the stack gets")
print("  sum_digits(123) — trace how the result is assembled")
