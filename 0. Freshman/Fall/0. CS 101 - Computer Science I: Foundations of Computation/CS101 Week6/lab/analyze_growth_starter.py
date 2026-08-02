#!/usr/bin/env python3
"""
analyze_growth_starter.py
CS 101 — Week 6, Lab 6 Starter

Fit a curve to empirical measurements and estimate the complexity class.

Student: ____________________________
Date: ______________________________
"""

import json
import math


def estimate_polynomial_exponent(measurements):
    """
    Given a list of (n, time) pairs, estimate k assuming T(n) ≈ c * n^k.

    Method:
        Take the natural log of both n and time for each data point.
        Fit a straight line: log(time) = log(c) + k * log(n).
        The slope of this line is the estimated exponent k.

    Linear regression formula for slope:
        slope = sum((x_i - mean_x) * (y_i - mean_y)) / sum((x_i - mean_x)^2)

    Args:
        measurements: list of (n, time_in_seconds) tuples

    Returns:
        float: estimated exponent k, or None if insufficient data

    Example:
        If T(n) = 0.001 * n^2 exactly, measurements at n=[100,200,400]
        would give times=[10, 40, 160] (in some unit), and this function
        should return approximately 2.0.
    """
    valid = [(n, t) for n, t in measurements if t > 0]
    if len(valid) < 2:
        return None

    # TODO:
    # 1. Compute log_ns = [log(n) for each valid point]
    # 2. Compute log_times = [log(t) for each valid point]
    # 3. Compute mean_x, mean_y
    # 4. Compute numerator = sum((x-mean_x)*(y-mean_y))
    # 5. Compute denominator = sum((x-mean_x)^2)
    # 6. Return numerator / denominator (guard against denominator == 0)
    pass


def estimate_exponential_base(measurements):
    """
    Given a list of (n, time) pairs, estimate b assuming T(n) ≈ c * b^n.

    Method:
        Take the natural log of time only (NOT of n — n stays linear).
        Fit a straight line: log(time) = log(c) + n * log(b).
        The slope of this line is log(b), so b = e^slope.

    Args:
        measurements: list of (n, time_in_seconds) tuples

    Returns:
        float: estimated base b, or None if insufficient data

    Example:
        If T(n) = 0.001 * 2^n exactly, this should return approximately 2.0.
    """
    valid = [(n, t) for n, t in measurements if t > 0]
    if len(valid) < 2:
        return None

    # TODO:
    # 1. ns = [n for each valid point]  (NOT logged)
    # 2. log_times = [log(t) for each valid point]
    # 3. Linear regression of log_times against ns (same method as above)
    # 4. slope = ...
    # 5. return math.exp(slope)
    pass


def classify_complexity(k_or_b, is_exponential=False):
    """
    BONUS: Given an estimated exponent (polynomial) or base (exponential),
    return a human-readable classification string.

    Args:
        k_or_b: the estimated exponent or base
        is_exponential: if True, k_or_b is a base (from estimate_exponential_base);
                        if False, k_or_b is an exponent (from estimate_polynomial_exponent)

    Returns:
        str: e.g. "O(n)", "O(n^2)", "O(log n)", "O(2^n)"

    Suggested thresholds (tune based on your own data):
        Polynomial exponent k:
            k < 0.3        → "O(log n)" or "O(1)"
            0.7 <= k < 1.3 → "O(n)"
            1.3 <= k < 1.8 → "O(n log n)"  (grows slightly faster than linear)
            1.8 <= k < 2.5 → "O(n^2)"
            k >= 2.5       → "O(n^3) or higher"
        Exponential base b:
            b > 1.1 → "O(b^n)" (exponential)
    """
    # TODO: implement classification logic
    pass


if __name__ == "__main__":
    with open("benchmark_results.json") as f:
        results = json.load(f)

    print("=" * 60)
    print("POLYNOMIAL EXPONENT ESTIMATES (assumes T(n) ~ n^k)")
    print("=" * 60)
    for name in ["func_a", "func_b", "func_d", "func_g", "func_h"]:
        measurements = results[name]
        k = estimate_polynomial_exponent(measurements)
        if k is not None:
            print(f"  {name}: estimated exponent k ≈ {k:.2f}")
        else:
            print(f"  {name}: insufficient data")

    print()
    print("=" * 60)
    print("LOGARITHMIC CHECK (func_c should show near-ZERO exponent)")
    print("=" * 60)
    k_c = estimate_polynomial_exponent(results["func_c"])
    if k_c is not None:
        print(f"  func_c: estimated exponent k ≈ {k_c:.3f}  (expect close to 0)")

    print()
    print("=" * 60)
    print("EXPONENTIAL BASE ESTIMATES (assumes T(n) ~ b^n)")
    print("=" * 60)
    for name in ["func_e", "func_f"]:
        measurements = results[name]
        b = estimate_exponential_base(measurements)
        if b is not None:
            print(f"  {name}: estimated base b ≈ {b:.2f}")
        else:
            print(f"  {name}: insufficient data")
