#!/usr/bin/env python3
"""
ps3.py
CS 101 — Problem Set 3: Functions, Scope, and the Call Stack
Due Friday 23 October 2026, 17:00

Student: ____________________________

Every function needs a docstring and at least two assert tests below it.
Weeks 0-3 tools only: use assert for preconditions (raise is Week 10); no dictionaries.
"""

# --- B1: Math Library -----------------------------------------------------------
def clamp(value, lo, hi):
    """TODO"""
    pass

def lerp(a, b, t):
    """TODO"""
    pass

def normalize(value, src_min, src_max, dst_min=0.0, dst_max=1.0):
    """TODO — must call lerp"""
    pass

def smooth_step(t):
    """TODO"""
    pass


# --- B2: Strings ----------------------------------------------------------------
def title_case(text):
    """TODO"""
    pass

def count_substring(text, sub):
    """TODO — non-overlapping, while loop + slicing, no .count()"""
    pass

def is_palindrome_phrase(text):
    """TODO"""
    pass


# --- B3: Functions as Values ------------------------------------------------------
def apply_to_all(func, lst):
    """TODO"""
    pass

def keep_if(predicate, lst):
    """TODO"""
    pass

def compose(f, g):
    """TODO — return a function computing f(g(x))"""
    pass


# --- B4: Grade Report --------------------------------------------------------------
assignments = [
    ("Problem Set 1", 87, 100, 0.30),
    ("Problem Set 2", 92, 100, 0.30),
    ("Midterm", 78, 100, 0.25),
    ("Lab Average", 95, 100, 0.10),
    ("Participation", 100, 100, 0.05),
]
# TODO: percentage, contribution, weighted_average, letter_grade, print_report


# --- B5: Recursion Preview ----------------------------------------------------------
def power(base, exp):
    """TODO — recursive; comment the base case and the recursive step"""
    pass

def gcd(a, b):
    """TODO — recursive Euclid"""
    pass
