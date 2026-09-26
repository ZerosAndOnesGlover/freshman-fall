#!/usr/bin/env python3
"""
ps4.py
CS 101 — Problem Set 4: Recursion
Due Friday 30 October 2026, 17:00

Student: ____________________________

Each docstring must name the base case and the recursive case.
Write at least two assert tests under every function.
"""

# --- B1: Recursive list operations ---
def recursive_min(lst):
    """Smallest element of a non-empty list. Base: one element. Step: min of first and min of rest."""
    # TODO
    pass


def count_if(lst, predicate):
    """Number of elements x with predicate(x) true."""
    # TODO
    pass


def flatten(lst):
    """All non-list items of an arbitrarily nested list, in order."""
    # TODO
    pass



# --- B2: Recursive string operations ---
def count_vowels(s):
    """Number of vowels in s, any case."""
    # TODO
    pass


def is_balanced(s, depth=0):
    """True if every '(' in s is closed by a later ')'. depth = currently open brackets."""
    # TODO
    pass



# --- B3: Divide and conquer ---
def fast_power(base, exp):
    """base ** exp using halving: O(log exp) multiplications."""
    # TODO
    pass


def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    # TODO
    pass


def merge_sort(lst):
    """A new sorted list with the elements of lst (L14 §2)."""
    # TODO
    pass



# --- B4: Subsets ---
def subsets(lst):
    """All subsets of lst: those without the first element, then those with it."""
    # TODO
    pass


