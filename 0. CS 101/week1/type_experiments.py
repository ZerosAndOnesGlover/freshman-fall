#!/usr/bin/env python3
"""
type_experiments.py
CS 101 Lab 1, Part 2.1 — Conversions and Truthiness

Write your prediction first (as a comment), then run.
"""

print(int(-3.9))                  # Predict: -3   (int() truncates toward zero)
print(int("  42  "))              # Predict: 42   (int() tolerates surrounding whitespace)
print(round(2.5), round(3.5), round(-2.5))   # Predict: 2 4 -2  (round is half-to-even)
print(bool("False"))              # Predict: True (non-empty string is truthy)
print(bool("0"))                  # Predict: True (non-empty string is truthy)
print(bool([False]))              # Predict: True (non-empty list is truthy)
print(True + True + True)         # Predict: 3    (bool is a subclass of int)
