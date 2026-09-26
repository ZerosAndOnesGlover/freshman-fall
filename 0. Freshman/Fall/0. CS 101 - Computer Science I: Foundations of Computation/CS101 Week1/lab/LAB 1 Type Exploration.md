# CS 101 · Lab 1
## Type Exploration, Expressions, and Python Tutor

**Date:** Tuesday 6 October 2026 · 15:00–16:50 · Lab Section (Week 2) — covers Week 1 (L04–L06)
*Duration: 2 hours · 100 points via TA checkoff, part of the Labs component (10%)*

---

## Objectives

By the end of this lab, you will:
- [ ] Explain the difference between mutation and rebinding, with a Python Tutor diagram
- [ ] Predict the value of expressions involving conversion, truthiness and precedence
- [ ] Read and write numbers in binary with the bitwise operators
- [ ] Format numbers with f-string format specs
- [ ] Write a straight-line converter program that handles bad input

**Tools used:** only Weeks 0–1 — expressions, `input()`, conversions, `try`/`except ValueError`,
slicing, f-strings, `math`. No `if` statements, loops or `def` are needed; they begin in Week 2.

*(Revised 2026-09-26: the parts added up to 120 minutes for a 110-minute session. Part 2 is cut from
about 36 predictions to 14, and reflection Q3 was removed.)*

---

## Setup

```bash
mkdir -p "$CS101/week1"
cd "$CS101/week1"
```

Create `lab1_notes.md`; you will record your observations in it throughout the lab.

---

## Part 1: Python Tutor, Seeing Memory (25 minutes) — 20 points

Open https://pythontutor.com next to your terminal.

### Exercise 1.1: Binding vs. Copying

Step through this:

```python
x = [1, 2, 3]
y = x
y.append(4)
print(x)
print(y)
print(x is y)

a = 10
b = a
b = b + 1
print(a)
print(b)
print(a is b)
```

**Record in `lab1_notes.md`:**
1. After `y = x`, how many arrows point to the list?
2. Why did `x` change when only `y` was used?
3. Why did `a` not change when `b` did?

### Exercise 1.2: Immutability in Action

```python
s = "hello"
t = s
s = s.upper()
print(s)
print(t)
print(s is t)
```

**Record:** Did the original string change? Why is `t` still `"hello"`?

### Exercise 1.3: The Aliasing Trap

```python
a = [1, 2, 3]
b = [a, a, a]
a.append(4)
print(b)
```

**Record:** Predict `b` before running. What does this teach about mutable objects?

---

## Part 2: Predict, Then Run (25 minutes) — 30 points

For each file: **write your prediction as a comment first**, then run it. In `lab1_notes.md`, write one
sentence for every prediction you got wrong.

### Exercise 2.1: Conversions and Truthiness — `type_experiments.py`

```python
print(int(-3.9))         # Predict:
print(int("  42  "))     # Predict: (note the spaces)
print(round(2.5), round(3.5), round(-2.5))       # Predict:
print(bool("False"))     # Predict:
print(bool("0"))         # Predict:
print(bool([False]))     # Predict:
print(True + True + True)      # Predict:
```

### Exercise 2.2: Precedence Gauntlet — `precedence_test.py`

```python
print(2 ** 3 ** 2)          # Predict: (right-associative!)
print(-2 ** 2)              # Predict: (is it (-2)**2 or -(2**2)?)
print(1 < 2 > 3)            # Predict: (chained comparison)
print(not True or False)    # Predict:
print(1 and 2 and 3)        # Predict: (not just True/False!)
print(0 or "" or [] or 42)  # Predict:
print(0 or "" or [])        # Predict:
```

### Exercise 2.3: Bitwise Operations — `bitwise_explore.py`

```python
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
```

**Answer in `lab1_notes.md`:**
1. What does `&` do to each bit position?
2. What is `a << 2` in arithmetic terms? `a >> 2`?
3. Why is `~a` negative? (L05 §5: think two's complement — `~a` is `-a - 1`.)

---

## Part 3: f-String Formatting (20 minutes) — 20 points

Create `formatting_challenge.py`. Each line is one `print` with one format spec from L06 §7.

```python
import math

pi = math.pi
large = 1234567.891234
small = 0.00001234
score = 0.87666666

# TODO: pi to 2, 4, 6 and 8 decimal places, one line each
#   3.14 / 3.1416 / 3.141593 / 3.14159265
# TODO: large with a thousands separator and 2 decimals     -> 1,234,567.89
# TODO: small in scientific notation, 3 decimals            -> 1.234e-05
# TODO: score as a percentage with 1 decimal                -> 87.7%
# TODO: 255 in decimal, hex and binary                      -> 255 / ff / 11111111
# TODO: the word "Python" right-aligned, left-aligned and centred in width 12
```

---

## Part 4: Build a Converter (30 minutes) — 30 points

Create `converter.py`. It is a straight-line program: it reads one number and prints every
conversion at once.

```python
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
    # TODO: value km -> miles        (divide by KM_PER_MILE)
    # TODO: value miles -> km
    # TODO: value kg -> pounds       (divide by KG_PER_POUND)
    # TODO: value °C -> °F           F = C × 9/5 + 32
    # TODO: value °C -> K            K = C + 273.15
    # Print each as e.g. "42.0 km = 26.0976 mi", using the :.6g format spec.
    pass
```

**Verification tests** (with `:.6g`):
```
42 km  = 26.0976 mi
100 °C = 212 °F
-40 °C = -40 °F
0 °C   = 273.15 K
1 kg   = 2.20462 lb
abc    -> 'abc' is not a number.
```

---

## Part 5: Commit and Reflection (5 minutes)

```bash
cd "$CS101/week1"
git add .
git commit -m "CS 101 Lab 1: type exploration, formatting, converter"
git push
```

In `lab1_notes.md`, answer each in 2–3 sentences:

**Q1.** Why did changing `y` affect `x`, but changing `b` did not affect `a`?

**Q2.** Python refuses `"5" + 3` but accepts `1 + 1.0`. Is that a contradiction?

---

## TA Checkoff Criteria

| Part | Points | Show your TA |
|---|---|---|
| 1 | 20 | Python Tutor diagram for 1.1, explained in your own words |
| 2 | 30 | All three files run; wrong predictions explained in notes |
| 3 | 20 | Every formatted line matches the expected output |
| 4 | 30 | `converter.py` passes all six verification tests |
| **Total** | **100** | Reflection answered and work committed (required for checkoff) |

---

*CS 101 · Week 1 · Lab 1 · Tuesday 6 October 2026 · © CSE Department*
