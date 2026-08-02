# temperature.py
# CS 101, Week 0, Lab 0
# Temperature converter: Celsius ↔ Fahrenheit ↔ Kelvin
#
# Student Name: ________________________________
# Date: ________________________________________
#
# Formulas:
#   F = (C × 9/5) + 32
#   C = (F - 32) × 5/9
#   K = C + 273.15
#   Absolute zero: -273.15°C = -459.67°F = 0K

print("=== Temperature Converter ===\n")

# --- Part 1: Boiling point of water (100°C) ---
celsius = 100.0

# TODO: Compute fahrenheit and kelvin from celsius
fahrenheit = None   # Replace None with the formula
kelvin = None       # Replace None with the formula

# Uncomment when ready:
# print(f"Boiling point of water:")
# print(f"  {celsius}°C = {fahrenheit:.2f}°F = {kelvin:.2f}K")

# --- Part 2: -40 degrees (the famous crossover point) ---
celsius = -40.0

# TODO: Compute fahrenheit and kelvin
fahrenheit = None
kelvin = None

# Uncomment when ready:
# print(f"\n-40 degrees:")
# print(f"  {celsius}°C = {fahrenheit:.2f}°F = {kelvin:.2f}K")

# --- Part 3: Normal human body temperature (98.6°F) ---
fahrenheit_input = 98.6

# TODO: Compute celsius and kelvin from fahrenheit
celsius_result = None
kelvin_result = None

# Uncomment when ready:
# print(f"\nHuman body temperature:")
# print(f"  {fahrenheit_input}°F = {celsius_result:.2f}°C = {kelvin_result:.2f}K")

# --- CHALLENGE: Absolute zero (-273.15°C) ---
# TODO: Add absolute zero conversion and print it


# --- BONUS CHALLENGE: Interactive input ---
# TODO: Ask the user to enter a temperature in Celsius
#       and print the Fahrenheit and Kelvin equivalents
#       Hint: use input() and float()
