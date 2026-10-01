# temperature.py
# Temperature converter: Celsius ↔ Fahrenheit ↔ Kelvin
# CS 101, Week 0, Lab 0
# Adebayo Glover, 1 October 2026

# --- Formulas ---
# F = (C × 9/5) + 32
# C = (F - 32) × 5/9
# K = C + 273.15

print("=== Temperature Converter ===\n")

# Convert 100°C (boiling point of water)
celsius = 100.0
fahrenheit = (celsius * 9/5) + 32
kelvin = celsius + 273.15

print(f"Boiling point of water:")
print(f"  {celsius}°C = {fahrenheit:.2f}°F = {kelvin:.2f}K")

# Convert -40 (the point where Celsius and Fahrenheit are equal)
celsius = -40.0
fahrenheit = (celsius * 9/5) + 32
kelvin = celsius + 273.15

print(f"\n-40 degrees:")
print(f"  {celsius}°C = {fahrenheit:.2f}°F = {kelvin:.2f}K")

# Convert 98.6°F (normal human body temperature)
fahrenheit = 98.6
celsius = (fahrenheit - 32) * 5/9
kelvin = celsius + 273.15

print(f"\nHuman body temperature:")
print(f"  {fahrenheit}°F = {celsius:.2f}°C = {kelvin:.2f}K")

# CHALLENGE: Add absolute zero (-273.15°C)
celsius = -273.15
fahrenheit = (celsius * 9/5) + 32
kelvin = celsius + 273.15

print(f"\nAbsolute zero:")
print(f"  {celsius}°C = {fahrenheit:.2f}°F = {kelvin:.2f}K")
