#!/usr/bin/env python3
"""
ps2.py
CS 101 — Problem Set 2: Control Flow
Due Friday 16 October 2026, 17:00

Student: ____________________________

Weeks 0-2 tools only: if/elif/else, while, for, range, break/continue,
nested loops, lists with .append(). No def, no dictionaries.
"""

# --- B1: Digit Analysis ---------------------------------------------------------
n = int(input("Positive integer: "))
# TODO: one while loop over the digits (% 10, // 10): count, sum, product, largest
# TODO: digital root: keep summing digits while the value has 2+ digits
# TODO: palindrome: build the reversed number digit by digit, compare with n


# --- B2: Sequences ----------------------------------------------------------------
n = int(input("How many terms? "))
# TODO (a): list of the first n Fibonacci numbers, for loop, invariant as a comment
# TODO (b): p, q = 1, 1; print n fractions p/q, their value and error; next = p + 2q, p + q


# --- B3: Patterns -----------------------------------------------------------------
n = int(input("Size: "))
# TODO (a): right triangle
# TODO (b): diamond with half-height n
# TODO (c): n x n multiplication table, each entry :5d


# --- B4: Number Theory ------------------------------------------------------------
a = int(input("a: "))
b = int(input("b: "))
# TODO (a): Euclid's GCD with a while loop, then LCM
# TODO (b): perfect numbers among [6, 12, 28, 496, 500]
# TODO (c): prime factors of each of [360, 13, 1001]
