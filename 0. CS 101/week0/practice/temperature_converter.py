# temperature_converter.py
# Converts between Celsius and Fahrenheit
# CS 101 — Week 0


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


# Main program
print("=== Temperature Converter ===")
choice = input("Convert FROM: (C)elsius or (F)ahrenheit? ").strip().upper()

if choice == "C":
    temp = float(input("Enter temperature in Celsius: "))
    result = celsius_to_fahrenheit(temp)
    print(f"{temp}°C = {result:.2f}°F")
elif choice == "F":
    temp = float(input("Enter temperature in Fahrenheit: "))
    result = fahrenheit_to_celsius(temp)
    print(f"{temp}°F = {result:.2f}°C")
else:
    print("Invalid choice. Please enter C or F.")
