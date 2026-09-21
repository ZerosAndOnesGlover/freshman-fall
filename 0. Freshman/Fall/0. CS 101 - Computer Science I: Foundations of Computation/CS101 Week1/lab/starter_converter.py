#!/usr/bin/env python3
"""
converter.py — CS 101, Week 1, Lab 1 (Tuesday 6 October 2026)
Reads one number and prints it converted several ways.
Week 0-1 tools only: input(), float(), try/except/else, f-strings.
"""

KM_PER_MILE = 1.609344
KG_PER_POUND = 0.453592

raw = input("Enter a value: ")

try:
    value = float(raw)
except ValueError:
    print(f"{raw!r} is not a number.")
else:
    # TODO: value km -> miles        (divide by KM_PER_MILE)
    # TODO: value miles -> km
    # TODO: value kg -> pounds       (divide by KG_PER_POUND)
    # TODO: value °C -> °F           F = C × 9/5 + 32
    # TODO: value °C -> K            K = C + 273.15
    # Print each as e.g. "42.0 km = 26.0976 mi", using the :.6g format spec.
    pass
