#!/usr/bin/env python3
"""
converter.py — CS 101, Week 1, Lab 1
Reads one number and prints it converted several ways.
"""

KM_PER_MILE = 1.609344
KG_PER_POUND = 0.453592

raw = input("Enter a value: ")

try:
    value = float(raw)
except ValueError:
    print(f"{raw!r} is not a number.")
else:
    print(f"{value} km = {value / KM_PER_MILE:.6g} mi")
    print(f"{value} mi = {value * KM_PER_MILE:.6g} km")
    print(f"{value} kg = {value / KG_PER_POUND:.6g} lb")
    print(f"{value} °C = {value * 9 / 5 + 32:.6g} °F")
    print(f"{value} °C = {value + 273.15:.6g} K")
