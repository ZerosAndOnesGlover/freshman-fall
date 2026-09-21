#!/usr/bin/env python3
"""
ps5.py
CS 101 — Problem Set 5: Searching and Sorting
Due Friday 6 November 2026, 17:00

Student: ____________________________

Every function: docstring with its invariant (or base/recursive case) and at least three asserts.
B3 ends with a loop that prints the comparison table for n = 100, 200, 400.
"""

# --- B1: Search variants ---
def find_first(lst, target):
    """Index of the first occurrence of target in sorted lst, or -1. O(log n).
Invariant: if target is present, its first index is in [lo, hi]; answer holds the best index found so far."""
    # TODO
    pass


def find_last(lst, target):
    """Index of the last occurrence of target in sorted lst, or -1. O(log n)."""
    # TODO
    pass


def count_occurrences(lst, target):
    """How many times target occurs in sorted lst, using find_first and find_last. O(log n)."""
    # TODO
    pass


def sqrt_floor(n):
    """floor(sqrt(n)) for n >= 0 by binary search on the answer (L16 §8)."""
    # TODO
    pass


# --- B2: Sorting ---
def insertion_sort_by_key(lst, key):
    """New list sorted by key(x), stable. Invariant: result[:i] is sorted by key."""
    # TODO
    pass


def merge(left, right):
    """TODO"""
    # TODO
    pass


def merge_k_sorted(lists):
    """Merge k sorted lists by repeated pairwise merging."""
    # TODO
    pass


def top_k(lst, k):
    """The k largest elements in descending order, by k passes of selection (no full sort)."""
    # TODO
    pass


# --- B3: Counting comparisons ---
def selection_sort_count(lst):
    """(sorted copy, number of element comparisons)."""
    # TODO
    pass


def insertion_sort_count(lst):
    """(sorted copy, number of element comparisons)."""
    # TODO
    pass
