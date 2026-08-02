#!/usr/bin/env python3
"""
ps1.py
CS 101 — Problem Set 1: Data, Types, and Expressions

Student: ____________________________
Date: ______________________________

Honor pledge: I wrote this code myself and understand every line.
Signed: ____________________________
"""

import math

# ─────────────────────────────────────────────────────────────────────────────
# B1: Type Inspector
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 50)
print("B1: Type Inspector")
print("=" * 50)

raw = input("Enter a value: ")

# TODO: print analysis as described in the problem statement
# - Original string, length, type
# - Attempt int, float conversion (success or failure)
# - Truthiness
# - First and last character (handle empty string!)


# ─────────────────────────────────────────────────────────────────────────────
# B2: Expression Evaluator
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("B2: Expression Evaluator")
print("=" * 50)

# Each line should print: "Expression: <expr_text>    Result: <value>"
# Use f-strings with appropriate padding for alignment.

# 1. 2 raised to the power 32
expr1 = 2 ** 32
print(f"{'2**32':<35} = {expr1}")

# 2. Seconds in a year
# TODO:
expr2 = None  # Replace with expression
print(f"{'seconds in a year':<35} = {expr2}")

# 3. 1_000_000_007 mod 997
# TODO:
expr3 = None
print(f"{'1_000_000_007 % 997':<35} = {expr3}")

# 4. Integer part of sqrt(2)
# TODO: use ** 0.5 and int() — no math module
expr4 = None
print(f"{'int(2**0.5)':<35} = {expr4}")

# 5. Is 17 even? (boolean expression)
# TODO:
expr5 = None
print(f"{'17 is even':<35} = {expr5}")

# 6. Is 2023 a leap year? (single boolean expression)
# Leap year rules:
#   divisible by 4? → might be leap year
#   divisible by 100? → not a leap year (unless...)
#   divisible by 400? → IS a leap year
# TODO: write as ONE boolean expression
year = 2023
expr6 = None
print(f"{'2023 is a leap year':<35} = {expr6}")

# 7. Number of decimal digits in 2^100
# TODO: convert to string, check len
expr7 = None
print(f"{'digits in 2**100':<35} = {expr7}")

# 8. Is "racecar" a palindrome? (slicing, one expression)
# TODO:
word = "racecar"
expr8 = None
print(f"{'racecar is palindrome':<35} = {expr8}")


# ─────────────────────────────────────────────────────────────────────────────
# B3: Integer Dissector
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("B3: Integer Dissector")
print("=" * 50)

raw_n = input("Enter a positive integer: ")
try:
    n = int(raw_n)
    if n <= 0:
        print("Must be positive. Using 42 as default.")
        n = 42
except ValueError:
    print(f"'{raw_n}' is not valid. Using 42 as default.")
    n = 42

# TODO: Print all required fields as shown in the problem statement
# - Decimal, binary, hex, octal
# - Even or odd (use bitwise AND: n & 1)
# - Power of 2? (use n & (n-1) == 0 — add a comment explaining why this works)
# - Digit sum
# - Bit length


# ─────────────────────────────────────────────────────────────────────────────
# B4: String Sculptor
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("B4: String Sculptor")
print("=" * 50)

text = "  The quick brown fox jumps over the lazy dog.  "

# TODO: Compute and print all 12 transformations


# ─────────────────────────────────────────────────────────────────────────────
# B5: Number Formatter
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("B5: Number Formatter")
print("=" * 50)

raw_f = input("Enter a number: ")
try:
    f = float(raw_f)
except ValueError:
    print(f"'{raw_f}' is not valid. Using 1234567.89.")
    f = 1234567.89

# TODO: Print the number in 8 different formats
# For whole numbers: also print binary, hex, octal


# ─────────────────────────────────────────────────────────────────────────────
# B6: Boolean Logic Table
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("B6: Boolean Logic Table")
print("=" * 50)

# The expression: (A and not B) or (not A and B)
# This is XOR. Print the truth table for all 4 combinations of A and B.
# Also verify it matches A ^ B for each case.

# TODO: Print the truth table — no loops allowed yet.
# Just 4 lines of print() with the appropriate expressions.

header = f"{'A':<8}{'B':<8}{'(A∧¬B)∨(¬A∧B)':<25}{'A^B':<8}{'Match?'}"
print(header)
print("-" * len(header))

# Row 1: A=True, B=True
A, B = True, True
xor_manual = (A and not B) or (not A and B)
xor_op     = A ^ B
match      = xor_manual == xor_op
# TODO: print this row with f-string
# print(f"{str(A):<8}...")

# Row 2: A=True, B=False
# TODO

# Row 3: A=False, B=True
# TODO

# Row 4: A=False, B=False
# TODO


# ─────────────────────────────────────────────────────────────────────────────
# B7: Mortgage Calculator
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("B7: Mortgage Calculator")
print("=" * 50)

# TODO: Get inputs (principal, annual_rate_percent, years)
#       Validate them
#       Compute monthly payment using the formula in the problem statement
#       Print the summary
#       Print the first 12 months analytically (no loops yet):
#
#         balance(n) = P × (1+r)^n - M × [(1+r)^n - 1] / r
#         interest(n) = balance(n-1) × r
#         principal_paid(n) = M - interest(n)
#
# Use f-strings with comma formatting for all dollar amounts.
