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


def deep_sum(lst):
    """Sum of every number in an arbitrarily nested list."""
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


def interleave(s1, s2):
    """Alternate characters of s1 and s2; append the rest of the longer one."""
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


def binary_search(lst, target, lo=0, hi=None):
    """Index of target in sorted lst, or -1 (L13 §8)."""
    # TODO
    pass


# --- B4: Choose-explore-unchoose ---
def subsets(lst):
    """All subsets of lst: those without the first element, then those with it."""
    # TODO
    pass


def combinations(lst, k):
    """All k-element subsets of lst, keeping lst's order: C(n,k) = C(n-1,k-1) + C(n-1,k)."""
    # TODO
    pass


# --- B5: Recursion to iteration ---
def factorial_iterative(n):
    """TODO"""
    # TODO
    pass


def binary_search_iter(lst, target):
    """TODO"""
    # TODO
    pass
