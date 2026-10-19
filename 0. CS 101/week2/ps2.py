#!/usr/bin/env python3
"""
ps2.py
CS 101 — Problem Set 2: Control Flow
Due Friday 16 October 2026, 17:00

Student: Adebayo Glover

Weeks 0-2 tools only: if/elif/else, while, for, range, break/continue,
nested loops, lists with .append(). No def, no dictionaries.
"""

# --- B1: Digit Analysis ---------------------------------------------------------
n = int(input("Positive integer: "))
count = 0
digit_sum = 0
digit_product = 1
largest = 0
m = n
while m > 0:
    d = m % 10
    count += 1
    digit_sum += d
    digit_product *= d
    if d > largest:
        largest = d
    m //= 10

# digital root: repeatedly sum the digits until a single digit is left
root = digit_sum
while root >= 10:
    s = 0
    while root > 0:
        s += root % 10
        root //= 10
    root = s

# palindrome: build the reversed number one digit at a time and compare with n
reversed_n = 0
m = n
while m > 0:
    reversed_n = reversed_n * 10 + m % 10
    m //= 10

print(f"Digits:        {count}")
print(f"Digit sum:     {digit_sum}")
print(f"Digit product: {digit_product}")
print(f"Largest digit: {largest}")
print(f"Digital root:  {root}")
print(f"Palindrome:    {reversed_n == n}")


# --- B2: Fibonacci --------------------------------------------------------------
n = int(input("How many terms? "))
fibs = []
a, b = 0, 1
for i in range(n):
    # invariant: fibs holds F(0)..F(i-1); a == F(i), b == F(i+1)
    fibs.append(a)
    a, b = b, a + b
print(fibs)


# --- B3: Patterns ---------------------------------------------------------------
n = int(input("Size: "))
# (a) right triangle
for row in range(1, n + 1):
    print("*" * row)
# (b) diamond with half-height n: growing top half, then shrinking bottom half
for row in range(1, n + 1):
    print(" " * (n - row) + "*" * (2 * row - 1))
for row in range(n - 1, 0, -1):
    print(" " * (n - row) + "*" * (2 * row - 1))


# --- B4: Number Theory ----------------------------------------------------------
a = int(input("a: "))
b = int(input("b: "))
x, y = a, b
while y != 0:
    x, y = y, x % y
print(f"gcd({a}, {b}) = {x}")
print(f"lcm({a}, {b}) = {a * b // x}")

for n in [360, 13, 1001]:
    factors = []
    m = n
    f = 2
    while m > 1:
        while m % f == 0:
            factors.append(f)
            m //= f
        f += 1
    print(n, factors)
