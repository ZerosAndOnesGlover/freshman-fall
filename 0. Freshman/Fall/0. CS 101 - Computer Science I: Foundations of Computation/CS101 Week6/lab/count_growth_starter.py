#!/usr/bin/env python3
"""
count_growth.py — CS 101 Lab 6 (Tuesday 10 November 2026)
TODO: in each function, add `global ops` and `ops += 1` at its innermost step (Part 2).
"""
import math

ops = 0


def func_a(n):
    total = 0
    for i in range(n):
        total += i
    return total


def func_b(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += i * j
    return total


def func_c(n):
    count = 0
    i = 1
    while i < n:
        count += 1
        i *= 2
    return count


def func_e(n):
    if n <= 1:
        return 1
    return func_e(n - 1) + func_e(n - 1)


def func_f(n):
    if n <= 1:
        return n
    return func_f(n - 1) + func_f(n - 2)


def func_g(lst):
    n = len(lst)
    for i in range(n):
        for j in range(i + 1, n):
            if lst[i] == lst[j]:
                return True
    return False


def func_h(n):
    if n <= 1:
        return n
    return func_h(n // 2) + func_h(n // 2) + n


def count_ops(func, arg):
    """Reset ops, run func(arg), return how many steps it counted."""
    ops = 0
    func(arg)
    return ops


if __name__ == "__main__":
    print("Polynomial-looking functions: steps at n and 2n, and k = log2(ratio)")
    for name, func, make_arg in [("A", func_a, lambda n: n), ("B", func_b, lambda n: n),
                                 ("C", func_c, lambda n: n), ("G", func_g, lambda n: list(range(n))),
                                 ("H", func_h, lambda n: n)]:
        row = f"  {name}:"
        previous = None
        for n in [256, 512, 1024, 2048]:
            steps = count_ops(func, make_arg(n))
            if previous:
                row += f"  n={n}: {steps} (k={math.log2(steps / previous):.2f})"
            else:
                row += f"  n={n}: {steps}"
            previous = steps
        print(row)

    print("\nExponential-looking functions: ratio of steps from n to n+1")
    for name, func in [("E", func_e), ("F", func_f)]:
        row = f"  {name}:"
        previous = None
        for n in range(16, 21):
            steps = count_ops(func, n)
            row += f"  n={n}: {steps}" + (f" (x{steps / previous:.3f})" if previous else "")
            previous = steps
        print(row)
