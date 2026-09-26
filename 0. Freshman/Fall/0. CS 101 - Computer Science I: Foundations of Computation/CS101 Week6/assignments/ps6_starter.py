#!/usr/bin/env python3
"""
ps6.py
CS 101 — Problem Set 6: Algorithm Analysis
Due Friday 13 November 2026, 17:00

Student: ____________________________

Docstring first line: the Theta-bound. At least two asserts per function.
B2 ends with loops that print its table.
"""

# --- B1: Classifying real code ---
def has_zero_triple(lst):
    """True if three elements at distinct positions sum to 0.  O(n^3): three nested loops over i < j < k."""
    # TODO
    pass


def matrix_multiply(A, B):
    """Product of two n x n matrices (lists of lists).  O(n^3): n^2 entries, each a sum of n products."""
    # TODO
    pass


def count_inversions(lst):
    """Number of pairs i < j with lst[i] > lst[j].  O(n^2): n(n-1)/2 pairs checked."""
    # TODO
    pass


# --- B2: Amortized cost of appends ---
def simulate_appends(n, grow):
    """Append n items to an array that starts with capacity 1. When full, the capacity becomes grow(capacity)
and every stored item is copied. Returns the total number of copies."""
    # TODO
    pass


double = lambda c: 2 * c

plus_one = lambda c: c + 1
