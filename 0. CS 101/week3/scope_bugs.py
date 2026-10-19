#!/usr/bin/env python3
"""
scope_bugs.py
CS 101 — Week 3, Lab 3
Scope bug hunt: find, explain, and fix each bug.
"""

# ─── Bug 1 ────────────────────────────────────────────────────────────────────
# This should accumulate a running total across calls.
running_total = 0

def accumulate(n):
    # BUG: `running_total += n` assigns to running_total, which makes the name
    # local to accumulate for the WHOLE body (LEGB), so the read on the right
    # raises UnboundLocalError. Fix: declare it global (or pass/return it).
    global running_total
    running_total += n
    return running_total

assert accumulate(5) == 5
assert accumulate(3) == 8


# ─── Bug 2 ────────────────────────────────────────────────────────────────────
# This should return a list with the item appended, WITHOUT modifying the input.
def append_copy(lst, item):
    # BUG: `lst.append(item)` mutates the caller's list because lst and original
    # name the same object (aliasing). Fix: build and return a NEW list.
    return lst + [item]

original = [1, 2, 3]
new_list = append_copy(original, 4)
assert original == [1, 2, 3]          # input left untouched
assert new_list == [1, 2, 3, 4]


# ─── Bug 3 ────────────────────────────────────────────────────────────────────
# This should return the maximum of a list, defaulting to 0 for empty lists.
def safe_max(lst, default=0):
    # NO BUG HERE. `default=0` is an immutable int, so every call sharing the same
    # object is harmless — nothing can change it. A mutable default such as
    # `default=[]` would be dangerous, because all calls would share ONE list.
    if lst == []:
        return default
    max_val = lst[0]
    for x in lst:
        if x > max_val:
            max_val = x
    return max_val

assert safe_max([]) == 0
assert safe_max([1, 2, 3]) == 3


# ─── Bug 4 ────────────────────────────────────────────────────────────────────
# This should count items and take the average without clobbering the built-in.
def analyze(data):
    # BUG: `len = 0` makes `len` a local int that shadows the built-in inside
    # analyze, so any len(...) call here would raise TypeError. Rename it.
    count = 0
    for item in data:
        count += 1
    average = sum(data) / count
    return count, average

assert analyze([1, 2, 3, 4, 5]) == (5, 3.0)
assert analyze([10, 20]) == (2, 15.0)
