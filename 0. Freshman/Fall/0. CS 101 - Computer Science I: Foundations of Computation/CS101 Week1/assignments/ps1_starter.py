#!/usr/bin/env python3
"""
ps1.py
CS 101 — Problem Set 1: Data, Types, and Expressions
Due Friday 9 October 2026, 17:00

Student: ____________________________

Only Week 0-1 tools are needed: expressions, f-strings, slicing, input(),
int()/float() with try/except ValueError, and the conditional expression
`a if condition else b`. No if-statements, loops or def.
"""

# --- B1: Type Inspector -------------------------------------------------------
s = input("Enter a string: ")
print(f"Input:      {s!r}")
# TODO: length and type
# TODO: try int(s); on ValueError print "As int:     not a valid integer"
# TODO: try float(s); on ValueError print "As float:   not a valid float"
# TODO: truthiness
# TODO: first and last character, safe for the empty string (conditional expression)


# --- B2: Expression Evaluator --------------------------------------------------
print(f"{'2 ** 32':<30} {2 ** 32}")
# TODO: items 2-5, one print each, same layout


# --- B3: Integer Dissector -----------------------------------------------------
n = int(input("Enter a positive integer: "))
print(f"Number:      {n}")
# TODO: binary (:b), hexadecimal (:x), bits needed
# TODO: parity using & 1
# TODO: power of 2 using n & (n - 1) == 0 -- explain why it works in a comment
# TODO: n << 3 and n >> 1, with comments on what each does


# --- B4: Loan Calculator -------------------------------------------------------
raw_p = input("Principal: ")
raw_r = input("Annual rate (%): ")
raw_y = input("Years: ")
# TODO: try: convert all three / except ValueError: message / else: compute and print
#       r = annual_rate / 12 / 100 ; n = years * 12
#       M = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
