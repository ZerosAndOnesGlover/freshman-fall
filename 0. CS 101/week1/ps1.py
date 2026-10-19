#!/usr/bin/env python3
"""
ps1.py
CS 101 — Problem Set 1: Data, Types, and Expressions
Due Friday 9 October 2026, 17:00

Student: Adebayo Glover

Only Week 0-1 tools are used: expressions, f-strings, slicing, input(),
int()/float() with try/except ValueError, and the conditional expression
`a if condition else b`. No if-statements, loops or def.
"""

# --- B1: Type Inspector -------------------------------------------------------
s = input("Enter a string: ")
print(f"Input:      {s!r}")
print(f"Length:     {len(s)}")
print(f"Type:       {type(s)}")
try:
    print(f"As int:     {int(s)}")
except ValueError:
    print("As int:     not a valid integer")
try:
    print(f"As float:   {float(s)}")
except ValueError:
    print("As float:   not a valid float")
print(f"Truthy:     {bool(s)}")
# conditional expression keeps the empty string from crashing on s[0] / s[-1]
print(f"First char: {s[0]!r}" if s else "First char: (none - empty string)")
print(f"Last char:  {s[-1]!r}" if s else "Last char:  (none - empty string)")


# --- B2: Expression Evaluator --------------------------------------------------
print(f"{'2 ** 32':<30} {2 ** 32}")
print(f"{'365 * 24 * 60 * 60':<30} {365 * 24 * 60 * 60}")
leap_2023 = (2023 % 4 == 0 and 2023 % 100 != 0) or 2023 % 400 == 0
print(f"{'2023 leap year':<30} {leap_2023}")
print(f"{'len(str(2 ** 100))':<30} {len(str(2 ** 100))}")
print(f"{'racecar palindrome':<30} {'racecar' == 'racecar'[::-1]}")


# --- B3: Integer Dissector -----------------------------------------------------
n = int(input("Enter a positive integer: "))
print(f"Number:      {n}")
print(f"Binary:      {n:b}")
print(f"Hexadecimal: {n:x}")
print(f"Bits needed: {len(f'{n:b}')}")
# parity via the low bit: & 1 keeps only the ones bit, which is 1 for odd, 0 for even
print(f"Parity:      {'even' if n & 1 == 0 else 'odd'}")
# A power of two has exactly one 1-bit. Subtracting 1 flips that bit to 0 and turns every
# lower bit to 1, so the two numbers share no 1-bit and n & (n - 1) == 0. Guard n > 0 because
# 0 & (0 - 1) == 0 would otherwise report 0 as a power of two.
is_power_of_two = n > 0 and n & (n - 1) == 0
print(f"Power of 2:  {'yes' if is_power_of_two else 'no'}")
print(f"Times 8:     {n << 3}")      # shifting left by 3 multiplies by 2**3 = 8
print(f"Halved:      {n >> 1}")      # shifting right by 1 is floor division by 2


# --- B4: Loan Calculator -------------------------------------------------------
raw_p = input("Principal: ")
raw_r = input("Annual rate (%): ")
raw_y = input("Years: ")
try:
    principal = float(raw_p)
    annual_rate = float(raw_r)
    years = int(raw_y)
except ValueError:
    print("Please enter numbers only.")
else:
    # convert the annual percentage rate to a monthly decimal rate
    monthly_rate = annual_rate / 12 / 100
    n_payments = years * 12
    growth = (1 + monthly_rate) ** n_payments
    monthly_payment = principal * (monthly_rate * growth) / (growth - 1)
    total_paid = monthly_payment * n_payments
    total_interest = total_paid - principal
    print(f"Monthly payment: ${monthly_payment:,.2f}")
    print(f"Total paid:      ${total_paid:,.2f}")
    print(f"Total interest:  ${total_interest:,.2f}")
    print(f"Interest / principal: {total_interest / principal:.2%}")
