# calculator.py
# A simple interactive calculator
# CS 101, Week 0, Lab 0
# Adebayo Glover, 1 October 2026

print("=== Simple Calculator ===")
print("Enter two numbers and I'll compute several things.\n")

# Get input
a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

# Compute and display results
print(f"\nResults for {a} and {b}:")
print(f"  Sum:          {a} + {b} = {a + b}")
print(f"  Difference:   {a} - {b} = {a - b}")
print(f"  Product:      {a} × {b} = {a * b}")

print(f"  Power:        {a} ** {b} = {a ** b}")
print(f"  Quotient:     {a} / {b} = {a / b:.6f}")
print(f"  Floor div:    {a} // {b} = {a // b}")
print(f"  Remainder:    {a} % {b} = {a % b}")
