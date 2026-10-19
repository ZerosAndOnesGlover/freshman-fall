#!/usr/bin/env python3
"""
formatting_challenge.py
CS 101 Lab 1, Part 3 — f-String Formatting
Each line is one print with one format spec.
"""

import math

pi = math.pi
large = 1234567.891234
small = 0.00001234
score = 0.87666666

print(f"{pi:.2f}")                                   # 3.14
print(f"{pi:.4f}")                                   # 3.1416
print(f"{pi:.6f}")                                   # 3.141593
print(f"{pi:.8f}")                                   # 3.14159265
print(f"{large:,.2f}")                               # 1,234,567.89
print(f"{small:.3e}")                                # 1.234e-05
print(f"{score:.1%}")                                # 87.7%
print(f"{255:d} {255:x} {255:b}")                    # 255 ff 11111111
print(f"{'Python':>12}|{'Python':<12}|{'Python':^12}|")
