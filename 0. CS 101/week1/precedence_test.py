#!/usr/bin/env python3
"""
precedence_test.py
CS 101 Lab 1, Part 2.2 — Precedence Gauntlet

Write your prediction first (as a comment), then run.
"""

print(2 ** 3 ** 2)          # Predict: 512  (right-associative: 2 ** (3 ** 2) = 2 ** 9)
print(-2 ** 2)              # Predict: -4   (** binds tighter than unary minus: -(2 ** 2))
print(1 < 2 > 3)            # Predict: False (chained: 1 < 2 and 2 > 3)
print(not True or False)    # Predict: False (not True -> False; False or False -> False)
print(1 and 2 and 3)        # Predict: 3    (and returns the last operand when all are truthy)
print(0 or "" or [] or 42)  # Predict: 42   (or returns the first truthy operand)
print(0 or "" or [])        # Predict: []   (all falsy, so or returns the last operand)
