#!/usr/bin/env python3
"""
bitwise_explore.py
CS 101 Lab 1, Part 2.3 — Bitwise Operations
"""

a = 0b10110100
b = 0b01101011

print(f"a = {a} = {a:08b}")
print(f"b = {b} = {b:08b}")
print(f"a & b  = {a & b:08b}")
print(f"a | b  = {a | b:08b}")
print(f"a ^ b  = {a ^ b:08b}")
print(f"~a     = {~a}")
print(f"a << 2 = {a << 2}")
print(f"a >> 2 = {a >> 2}")
