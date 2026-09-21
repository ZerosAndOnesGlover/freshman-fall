#!/usr/bin/env python3
"""
ps6.py
CS 101 — Problem Set 6: Algorithm Analysis
Due Friday 13 November 2026, 17:00

Student: ____________________________

Docstring first line: the Theta-bound. At least two asserts per function.
B2 and B3 end with loops that print their tables.
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


# --- B2: A recurrence in code ---
calls = 0

def tribonacci(n):
    """T(0)=0, T(1)=0, T(2)=1, T(n)=T(n-1)+T(n-2)+T(n-3). Naive; counts its calls in the global `calls`."""
    # TODO
    pass


def predicted_calls(n):
    """C(n) = 1 for n <= 2, else 1 + C(n-1) + C(n-2) + C(n-3) — computed with a loop."""
    # TODO
    pass


previous = None

# --- B3: Amortized cost of appends ---
def simulate_appends(n, grow):
    """Append n items to an array that starts with capacity 1. When full, the capacity becomes grow(capacity)
and every stored item is copied. Returns the total number of copies."""
    # TODO
    pass


double = lambda c: 2 * c

plus_one = lambda c: c + 1
