# CS 101 · Lab 1
## Type Exploration, Expressions, and Python Tutor

**Tuesday of Week 2 · Lab Section** — sat after this week's Wed–Fri lectures, and covers Week 1.
*Duration: 2 hours · Graded on completion (checkoff by TA)*

---

## Objectives

By the end of this lab, you will:
- [ ] Confidently explain the difference between mutable and immutable objects
- [ ] Predict the output of any expression involving Python's type system
- [ ] Use Python Tutor to visualize memory and object references
- [ ] Use `dir()` and `help()` to explore objects independently
- [ ] Build a multi-function program using type conversions and string formatting
- [ ] Complete and commit all exercises to Git

---

## Setup

```bash
cd "$CS101"        # set in ~/.bashrc -- see Lab 0
mkdir -p week1
cd week1
```

Create a file `LAB 1 Type Exploration.md`, you'll record your observations in it throughout the lab.

---

## Part 1: Python Tutor, Seeing Memory (25 minutes)

Python Tutor (https://pythontutor.com) visualizes exactly what Python is doing in memory. Open it in your browser and keep it next to your terminal.

### Exercise 1.1: Variable Binding vs. Copying

Type this into Python Tutor and step through it carefully:

```python
x = [1, 2, 3]
y = x          # Does this copy the list?
y.append(4)
print(x)       # What does x contain now?
print(y)       # What does y contain now?
print(x is y)  # Are they the same object?

# Now try with an int:
a = 10
b = a
b = b + 1
print(a)       # Did a change?
print(b)
print(a is b)
```

**Record in lab1_notes.md:**
1. After `y = x`, how many arrows point to the list `[1, 2, 3]` in Python Tutor?
2. Why did `x` change when we only modified `y`?
3. Why did `a` NOT change when we modified `b`?
4. What is the difference between `y = x` (for lists) and `b = a` (for ints)?

### Exercise 1.2: Immutability in Action

```python
s = "hello"
t = s
s = s.upper()
print(s)        # What is s?
print(t)        # What is t?
print(s is t)   # Same object?
```

Step through in Python Tutor. Then answer in `LAB 1 Type Exploration.md`:
1. When `s = s.upper()` runs, does the original string change?
2. What happens to the old `"hello"` object?
3. Why is `t` still `"hello"` even though `s` changed?

### Exercise 1.3: The Aliasing Trap

This is one of the most common bugs in Python. Understand it now.

```python
# Trap 1:
a = [1, 2, 3]
b = [a, a, a]   # List containing the same list three times
a.append(4)
print(b)         # What is b?

# Trap 2:
def add_item(lst, item):
    lst.append(item)
    return lst

original = [1, 2, 3]
result = add_item(original, 4)
print(original)  # Has original changed?
print(result is original)  # Are they the same object?
```

**Record:** What lesson about mutable objects does this teach?

---

## Part 2: Type System Deep Dive (30 minutes)

For each exercise: **predict the output first**, then run it, then record if you were wrong and why.

### Exercise 2.1: Type Conversions: Edge Cases

Create `type_experiments.py`:

```python
# type_experiments.py
# CS 101, Week 1, Lab 1
# Record your predictions before running!

print("=== int() conversions ===")
print(int(3.9))       # Predict: ___
print(int(-3.9))      # Predict: ___
print(int(True))      # Predict: ___
print(int("  42  "))  # Predict: ___ (note the spaces!)

print("\n=== round() vs int() vs math.floor() ===")
import math
values = [2.5, 3.5, 4.5, -2.5, -3.5]
for v in values:
    print(f"  {v:>5}: round={round(v)}, int={int(v)}, floor={math.floor(v)}, ceil={math.ceil(v)}")

print("\n=== Truthiness ===")
falsy_values = [False, 0, 0.0, 0j, "", [], (), {}, set(), None]
for val in falsy_values:
    print(f"  bool({repr(val):>12}) = {bool(val)}")

print("\n=== Surprising truthiness ===")
print(bool("False"))    # Predict: ___
print(bool("0"))        # Predict: ___
print(bool([False]))    # Predict: ___
print(bool([0]))        # Predict: ___
print(bool(0.0000001))  # Predict: ___

print("\n=== int is bool subtypes ===")
print(isinstance(True, int))     # Predict: ___
print(isinstance(True, bool))    # Predict: ___
print(isinstance(42, bool))      # Predict: ___
print(True == 1)                 # Predict: ___
print(True is 1)                 # Predict: ___ (tricky!)
```

Run it: `python3 type_experiments.py`

**For every prediction you got wrong: write one sentence explaining why in `LAB 1 Type Exploration.md`.**

### Exercise 2.2: Operator Precedence Gauntlet

Predict the value of each expression **without running it**. Then check.

Create `precedence_test.py`:

```python
# Predict each result before running
# Write your predictions here as comments

print(2 + 3 * 4)          # Predict: ___
print(2 ** 3 ** 2)         # Predict: ___ (careful: right-associative!)
print(-2 ** 2)             # Predict: ___ (is it (-2)**2 or -(2**2)?)
print(10 // 3 + 10 % 3)   # Predict: ___
print(True + True + True)  # Predict: ___
print(1 < 2 < 3)           # Predict: ___
print(1 < 2 > 3)           # Predict: ___ (tricky chained comparison!)
print(not True or False)   # Predict: ___
print(not (True or False))  # Predict: ___
print(1 and 2 and 3)       # Predict: ___ (not just True/False!)
print(0 and 2 and 3)       # Predict: ___
print(0 or "" or [] or 42)  # Predict: ___
print(0 or "" or [])       # Predict: ___
```

**Record: Which ones surprised you and why?**

### Exercise 2.3: Bitwise Operations

```python
# bitwise_explore.py
a = 0b10110100  # What is this in decimal?
b = 0b01101011  # What is this in decimal?

print(f"a = {a} = {a:08b}")
print(f"b = {b} = {b:08b}")
print()

operations = [
    ("a & b",   a & b),
    ("a | b",   a | b),
    ("a ^ b",   a ^ b),
    ("~a",      ~a),
    ("a << 2",  a << 2),
    ("a >> 2",  a >> 2),
]

for name, result in operations:
    if result >= 0:
        print(f"  {name:>8} = {result:4d} = {result:08b}")
    else:
        print(f"  {name:>8} = {result:4d} (negative — two's complement)")
```

**Questions to answer in `LAB 1 Type Exploration.md`:**
1. What does `a & b` do to each bit position?
2. What is `a << 2` equivalent to in arithmetic terms?
3. What is `a >> 2` equivalent to in arithmetic terms?
4. Why is `~a` negative? (Hint: think about two's complement)

---

## Part 3: String Operations (25 minutes)

### Exercise 3.1: String Methods Exploration

Use `dir()` and `help()` in the REPL to discover string methods you don't know yet.

```python
>>> s = "The Quick Brown Fox"
>>> dir(s)       # See all methods
>>> help(s.zfill)  # Read the docs for an unfamiliar method
```

Find and demonstrate 5 string methods not covered in lecture. For each:
- Show the method call
- Explain what it does in one sentence

Record in a file `string_exploration.py`.

### Exercise 3.2: String Manipulation Challenges

Create `string_challenges.py`:

```python
# string_challenges.py
# CS 101, Week 1, Lab 1

# Challenge 1: Reverse a string
# Use slicing — one line!
text = "Hello, World!"
# TODO: reversed_text = ???
# print(reversed_text)  # Should print: !dlroW ,olleH

# Challenge 2: Check if a string is a palindrome
# A palindrome reads the same forwards and backwards
# Examples: "racecar", "level", "madam"
word = "racecar"
# TODO: is_palindrome = ???  (True or False, one expression using slicing)
# print(f"'{word}' is a palindrome: {is_palindrome}")

# Challenge 3: Count vowels
sentence = "The quick brown fox jumps over the lazy dog"
# TODO: count how many vowels (a, e, i, o, u) are in sentence
# Hint: use .count() for each vowel, or use a loop (preview of Week 2)
# vowel_count = ???
# print(f"Vowels in sentence: {vowel_count}")

# Challenge 4: Title case without .title()
# Convert "the quick brown fox" to "The Quick Brown Fox"
# Hint: .split(), then .capitalize() on each word, then " ".join()
s = "the quick brown fox"
# TODO: title_case = ???
# print(title_case)  # Should print: The Quick Brown Fox

# Challenge 5: String alignment table
# Print a formatted table of squares and cubes
print(f"\n{'n':>5} {'n²':>8} {'n³':>12}")
print("-" * 26)
for n in range(1, 11):
    # TODO: print each row with proper alignment
    # Format: right-aligned in columns of width 5, 8, 12
    pass
```

### Exercise 3.3: f-String Formatting Mastery

```python
# formatting_challenge.py
# CS 101, Week 1, Lab 1
# Format data in various ways using f-strings

import math

# Data to format:
pi = math.pi
large = 1234567.891234
small = 0.00001234
score = 87.666666

# TODO: Print pi to 2, 4, 6, 8 decimal places — all on separate lines
# Expected:
# π ≈ 3.14
# π ≈ 3.1416
# π ≈ 3.141593
# π ≈ 3.14159265

# TODO: Print large number with thousands separator and 2 decimal places
# Expected: 1,234,567.89

# TODO: Print small in scientific notation with 3 significant figures
# Expected: 1.234e-05

# TODO: Print score as a percentage with 1 decimal place
# Expected: 87.7%

# TODO: Print 255 in decimal, hex, octal, and binary
# Expected:
# 255 in decimal: 255
# 255 in hex:     ff
# 255 in octal:   377
# 255 in binary:  11111111
```

---

## Part 4: Build: Unit Converter (25 minutes)

Build a complete unit conversion program demonstrating all of Week 1's concepts.

Create `unit_converter.py`:

```python
#!/usr/bin/env python3
"""
unit_converter.py
CS 101 — Week 1, Lab 1

A multi-category unit converter.
Demonstrates: types, conversions, f-strings, expressions, string methods.

Student: ____________________________
Date: ______________________________
"""

import math

# ─── Conversion factors ───────────────────────────────────────────────────────
# LENGTH (relative to metres)
LENGTH = {
    "mm":  0.001,
    "cm":  0.01,
    "m":   1.0,
    "km":  1000.0,
    "in":  0.0254,
    "ft":  0.3048,
    "yd":  0.9144,
    "mi":  1609.344,
}

# MASS (relative to kilograms)
MASS = {
    "mg":  0.000001,
    "g":   0.001,
    "kg":  1.0,
    "t":   1000.0,       # metric ton
    "oz":  0.0283495,
    "lb":  0.453592,
    "st":  6.35029,      # stone
}

# TEMPERATURE — special (not a simple factor)
# Handled separately below.


# ─── Conversion functions ─────────────────────────────────────────────────────

def convert_linear(value, from_unit, to_unit, table):
    """
    Convert between units in a linear table (length, mass, etc.)
    
    Strategy: convert FROM-unit → base unit → TO-unit
    
    Args:
        value: the numeric value to convert
        from_unit: string key in table (e.g. "km")
        to_unit: string key in table (e.g. "mi")
        table: dict mapping unit string → factor relative to base unit
    
    Returns:
        converted value as float, or None if a unit is not in the table
    """
    from_unit = from_unit.lower()
    to_unit   = to_unit.lower()
    
    if from_unit not in table:
        return None  # Signal: unknown unit
    if to_unit not in table:
        return None
    
    # TODO: Implement the conversion
    # Hint: value * table[from_unit] gives you the value in the base unit
    #       Then divide by table[to_unit] to get the result in to_unit
    pass


def convert_temperature(value, from_unit, to_unit):
    """
    Convert between Celsius (C), Fahrenheit (F), and Kelvin (K).
    
    Formulas:
        C → F: F = C × 9/5 + 32
        F → C: C = (F − 32) × 5/9
        C → K: K = C + 273.15
        K → C: C = K − 273.15
    
    Returns the converted value, or None if units are unknown.
    """
    from_unit = from_unit.upper()
    to_unit   = to_unit.upper()
    valid = {"C", "F", "K"}
    
    if from_unit not in valid or to_unit not in valid:
        return None
    if from_unit == to_unit:
        return value
    
    # TODO: Convert to Celsius first, then to target unit
    # Step 1: Convert from_unit → Celsius
    # Step 2: Convert Celsius → to_unit
    pass


# ─── Display helpers ──────────────────────────────────────────────────────────

def print_banner():
    print("╔══════════════════════════════════╗")
    print("║       CS 101 Unit Converter      ║")
    print("╚══════════════════════════════════╝")

def print_categories():
    print("\nCategories:")
    print("  L — Length")
    print("  M — Mass")
    print("  T — Temperature")
    print("  Q — Quit")

def print_units(table):
    """Print available units from a conversion table."""
    print("Available units:", ", ".join(sorted(table.keys())))


# ─── Main program ─────────────────────────────────────────────────────────────

def main():
    print_banner()
    
    while True:
        print_categories()
        choice = input("\nChoose category: ").strip().upper()
        
        if choice == "Q":
            print("Goodbye!")
            break
        elif choice not in ("L", "M", "T"):
            print("Invalid choice.")
            continue
        
        # Get value
        try:
            value = float(input("Enter value: "))
        except ValueError:
            print("Invalid number.")
            continue
        
        # Get units and convert
        if choice == "L":
            print_units(LENGTH)
            from_u = input("From unit: ").strip()
            to_u   = input("To unit: ").strip()
            result = convert_linear(value, from_u, to_u, LENGTH)
            
        elif choice == "M":
            print_units(MASS)
            from_u = input("From unit: ").strip()
            to_u   = input("To unit: ").strip()
            result = convert_linear(value, from_u, to_u, MASS)
            
        elif choice == "T":
            print("Units: C (Celsius), F (Fahrenheit), K (Kelvin)")
            from_u = input("From unit: ").strip()
            to_u   = input("To unit: ").strip()
            result = convert_temperature(value, from_u, to_u)
        
        # Display result
        if result is None:
            print("Unknown unit(s). Please check spelling.")
        else:
            # TODO: Format the output nicely using f-strings
            # Use 6 significant figures
            # Example: "42.0 km = 26.0977 mi"
            # Hint: use :.6g format specifier
            print(f"TODO: display {value} {from_u} → {result} {to_u}")


if __name__ == "__main__":
    main()
```

**Tasks:**
1. Implement `convert_linear()` — the conversion formula is in the docstring
2. Implement `convert_temperature()` — formulas are in the docstring
3. Fix the `print(f"TODO: ...")` line with a properly formatted f-string
4. Test every conversion category with at least 3 values each

**Verification tests:**
```
100 cm = 1.0 m       ✓
1 mi = 1.60934 km    ✓
1 kg = 2.20462 lb    ✓
100 C = 212.0 F      ✓
0 C = 273.15 K       ✓
-40 C = -40.0 F      ✓
```

---

## Part 5: Commit and Reflection (15 minutes)

### Commit all your work:

```bash
cd "$CS101/week1"
git add .
git status
git commit -m "Week 1 Lab: type exploration, string challenges, unit converter"
git push
```

### Reflection (add to `LAB 1 Type Exploration.md`):

Answer each in 2–3 sentences:

**Q1.** You ran `y = x` for a list and `b = a` for an int. In both cases there was an assignment. Why did modifying `y` affect `x`, but modifying `b` did not affect `a`? What fundamental property explains this difference?

**Q2.** Python is "strongly typed" — it won't implicitly convert `"5"` to `5` when you write `"5" + 3`. But it *will* implicitly promote `int` to `float` in `1 + 1.0`. Is this a contradiction? Why or why not?

**Q3.** What does short-circuit evaluation allow you to write that you couldn't write safely otherwise? Give a specific example where it prevents a runtime error.

**Q4.** You used `dir()` and `help()` to explore string methods. Name one method you discovered that you think will be useful, and explain what it does.

---

## TA Checkoff Criteria

Show your TA:
- [ ] Python Tutor diagrams for Exercise 1.1 (explain what you see)
- [ ] `type_experiments.py` running with correct output
- [ ] `string_challenges.py` with all TODOs completed
- [ ] `unit_converter.py` correctly converting at least 3 units in each category
- [ ] Git log showing commits from this lab

---

## Bonus Challenges

If you finish early:

**Bonus 1:** Add a SPEED category to the unit converter (m/s, km/h, mph, knots, mach).

**Bonus 2:** Add input validation to `convert_linear` so it suggests the nearest valid unit if the user makes a typo. (Hint: look up Python's `difflib.get_close_matches`)

**Bonus 3:** Add a conversion history — keep a list of all conversions done during the session and print it when the user chooses "Q".

---

*CS 101 · Week 1 · Lab 1 · © CSE Department*
