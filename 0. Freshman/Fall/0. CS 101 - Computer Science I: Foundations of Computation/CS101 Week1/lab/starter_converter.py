#!/usr/bin/env python3
"""
unit_converter.py
CS 101 — Week 1, Lab 1 Starter

A multi-category unit converter.

Student: ____________________________
Date: ______________________________
"""

import math

# ─── Conversion tables ────────────────────────────────────────────────────────
# Each value is the number of that unit equal to 1 base unit.
# LENGTH base unit: metre
LENGTH = {
    "mm":   0.001,
    "cm":   0.01,
    "m":    1.0,
    "km":   1000.0,
    "in":   0.0254,
    "ft":   0.3048,
    "yd":   0.9144,
    "mi":   1609.344,
    "nmi":  1852.0,      # nautical mile
}

# MASS base unit: kilogram
MASS = {
    "mg":   0.000001,
    "g":    0.001,
    "kg":   1.0,
    "t":    1000.0,      # metric ton
    "oz":   0.0283495,
    "lb":   0.453592,
    "st":   6.35029,     # stone
    "ton":  907.185,     # US short ton
}


# ─── Functions to implement ───────────────────────────────────────────────────

def convert_linear(value, from_unit, to_unit, table):
    """
    Convert a value between units using a linear conversion table.

    The strategy is a two-step conversion:
        value in from_unit
        → multiply by table[from_unit]   → value in base unit
        → divide by table[to_unit]       → value in to_unit

    Args:
        value     (float): the numeric value to convert
        from_unit (str):   the source unit (e.g. "km")
        to_unit   (str):   the target unit (e.g. "mi")
        table     (dict):  mapping of unit string → factor vs. base unit

    Returns:
        float: converted value, or None if either unit is unknown
    """
    from_unit = from_unit.lower().strip()
    to_unit   = to_unit.lower().strip()

    if from_unit not in table:
        return None
    if to_unit not in table:
        return None

    # TODO: implement conversion — two lines of math
    # Step 1: value_in_base = ?
    # Step 2: result = ?
    # return result
    pass  # Remove this once you've written the implementation


def convert_temperature(value, from_unit, to_unit):
    """
    Convert between Celsius (C), Fahrenheit (F), and Kelvin (K).

    Strategy: convert to Celsius as an intermediate step.
        F → C: C = (F - 32) × 5/9
        K → C: C = K - 273.15
        C → F: F = C × 9/5 + 32
        C → K: K = C + 273.15

    Args:
        value     (float): temperature to convert
        from_unit (str):   "C", "F", or "K" (case-insensitive)
        to_unit   (str):   "C", "F", or "K" (case-insensitive)

    Returns:
        float: converted temperature, or None if units are unknown
    """
    from_unit = from_unit.upper().strip()
    to_unit   = to_unit.upper().strip()
    valid     = {"C", "F", "K"}

    if from_unit not in valid or to_unit not in valid:
        return None
    if from_unit == to_unit:
        return float(value)   # No conversion needed

    # TODO: Step 1 — convert from_unit to Celsius
    # (write your code below this comment)
    celsius = None   # Replace with actual formula

    # TODO: Step 2 — convert Celsius to to_unit
    # (write your code below this comment)
    result = None   # Replace with actual formula

    return result


# ─── Display helpers ──────────────────────────────────────────────────────────

def print_banner():
    """Print the program header."""
    width = 38
    print("╔" + "═" * width + "╗")
    print("║" + "CS 101 Unit Converter".center(width) + "║")
    print("╚" + "═" * width + "╝")


def print_units(table):
    """Print available units sorted alphabetically."""
    units = sorted(table.keys())
    print("  Available units:", ", ".join(units))


def format_result(value, from_unit, result, to_unit):
    """
    Format a conversion result as a readable string.

    Examples:
        "100.0 cm = 1.0 m"
        "98.6 F = 37.0 C"
        "1.0 mi = 1.60934 km"

    TODO: Implement this function.
    Use the :.6g format specifier to show up to 6 significant figures
    without unnecessary trailing zeros.

    Args:
        value     (float): original value
        from_unit (str):   original unit
        result    (float): converted value
        to_unit   (str):   target unit

    Returns:
        str: formatted result string
    """
    # TODO: return a formatted string like "100.0 cm = 1.0 m"
    return f"TODO: {value} {from_unit} = {result} {to_unit}"


# ─── Main program ─────────────────────────────────────────────────────────────

def main():
    print_banner()
    print("\nWelcome! This program converts between common units.\n")

    while True:
        print("Categories:")
        print("  L — Length  |  M — Mass  |  T — Temperature  |  Q — Quit")
        choice = input("\nChoose: ").strip().upper()

        if choice == "Q":
            print("Goodbye!")
            break

        if choice not in ("L", "M", "T"):
            print("  ⚠ Invalid choice. Enter L, M, T, or Q.\n")
            continue

        # Get the numeric value
        raw_value = input("Enter value: ").strip()
        try:
            value = float(raw_value)
        except ValueError:
            print(f"  ⚠ '{raw_value}' is not a valid number.\n")
            continue

        # Perform the conversion based on category
        if choice == "L":
            print_units(LENGTH)
            from_u = input("From unit: ").strip()
            to_u   = input("To unit:   ").strip()
            result = convert_linear(value, from_u, to_u, LENGTH)

        elif choice == "M":
            print_units(MASS)
            from_u = input("From unit: ").strip()
            to_u   = input("To unit:   ").strip()
            result = convert_linear(value, from_u, to_u, MASS)

        elif choice == "T":
            print("  Units: C (Celsius)  F (Fahrenheit)  K (Kelvin)")
            from_u = input("From unit: ").strip()
            to_u   = input("To unit:   ").strip()
            result = convert_temperature(value, from_u, to_u)

        # Display result
        if result is None:
            print(f"  ⚠ Unknown unit. Check spelling and try again.\n")
        else:
            print(f"\n  ✓ {format_result(value, from_u, result, to_u)}\n")


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
