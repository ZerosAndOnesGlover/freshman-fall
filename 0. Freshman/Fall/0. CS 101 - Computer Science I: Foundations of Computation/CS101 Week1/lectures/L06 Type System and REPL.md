# CS 101 · Lecture 6 (Week 1, Lecture 3)
## Python's Type System, Conversions, and the REPL as a Thinking Tool

**Week 1 · Friday**
*"Strong typing: the language enforces type contracts. Dynamic typing: types are checked at runtime, not compile time. Python is both." — Guido van Rossum*

**Date:** Friday 28 August 2026 · 09:00–09:50 · Week 1

---

## 0. The Goal of This Lecture

By the end of Week 1, you should be able to write programs that take data in, transform it through expressions, and produce meaningful output. This lecture ties the week together: how the type system enforces correctness, how to move values between types safely, and how to use the REPL as a thinking tool rather than just a sandbox.

---

## 1. Python's Type System (Precisely)

Python is described as **dynamically typed** and **strongly typed**. These two properties are independent — understanding both is important.

### Dynamically Typed

Types are associated with **objects**, not **variables**. A variable can be rebound to an object of any type at any time:

```python
x = 42           # x references an int
x = "hello"      # x now references a str — perfectly valid
x = [1, 2, 3]   # x now references a list
```

Type checking happens **at runtime**, not before the program runs. This means type errors only show up when the offending line actually executes.

### Strongly Typed

Python **does not** silently convert between unrelated types. Operations on incompatible types raise `TypeError`:

```python
"5" + 3        # TypeError — Python refuses to guess your intent
"5" * "3"      # TypeError — can't multiply two strings
True + "yes"   # TypeError
```

Compare to JavaScript (weakly typed), which guesses:
```javascript
"5" + 3        // → "53"  (number silently converted to string — surprising!)
"5" - 3        // → 2    (string silently converted to number — inconsistent!)
```

Python's strong typing means **errors fail fast and loudly**, instead of silently producing wrong results. This is a deliberate design choice that makes debugging much easier.

---

## 2. The Type Hierarchy

Python's built-in types form a hierarchy:

```
object
├── int
│   └── bool
├── float
├── complex
├── str
├── bytes
├── NoneType
├── Sequence (abstract)
│   ├── list
│   ├── tuple
│   └── range
├── Mapping (abstract)
│   └── dict
└── Set (abstract)
    ├── set
    └── frozenset
```

`bool` is a subclass of `int` — that's why `True + 1 = 2` works. `isinstance(True, int)` returns `True`.

---

## 3. Type Conversion: The Complete Reference

### 3.1 Numeric Conversions

```python
# int() conversions
int(3.9)          # → 3      (truncates toward zero — NOT rounds)
int(-3.9)         # → -3     (truncates toward zero, not toward -∞)
int(True)         # → 1
int(False)        # → 0
int("42")         # → 42     (parses decimal string)
int("0b1010", 2)  # → 10    (parse binary string)
int("0xFF", 16)   # → 255   (parse hex string)
int("077", 8)     # → 63    (parse octal string)
int("3.14")       # → ValueError! Use int(float("3.14")) instead

# float() conversions
float(42)         # → 42.0
float("3.14")     # → 3.14
float("inf")      # → inf
float("nan")      # → nan
float("3.14abc")  # → ValueError

# round() — different from int()!
round(3.4)        # → 3
round(3.5)        # → 4
round(4.5)        # → 4   (banker's rounding — rounds to nearest even!)
round(3.14159, 2) # → 3.14
round(314.159, -1)# → 310  (negative places = round to tens, hundreds, etc.)
```

**Banker's Rounding (round half to even):**
```python
round(0.5)   # → 0  (rounds to nearest even)
round(1.5)   # → 2  (rounds to nearest even)
round(2.5)   # → 2  (rounds to nearest even)
round(3.5)   # → 4  (rounds to nearest even)
```
This minimizes cumulative rounding error — important in financial calculations.

### 3.2 String Conversions

```python
# str() — always succeeds
str(42)          # → "42"
str(3.14)        # → "3.14"
str(True)        # → "True"
str(None)        # → "None"
str([1,2,3])     # → "[1, 2, 3]"

# repr() — returns a string that could recreate the object
repr("hello")    # → "'hello'" (with quotes — useful for debugging)
repr(3.14)       # → "3.14"
repr(None)       # → "None"

# Parsing strings — can fail if format is wrong
int("42")        # → 42
float("3.14")    # → 3.14
int("hello")     # → ValueError
```

**`str()` vs `repr()`:**
- `str()`: human-readable output (what `print()` uses)
- `repr()`: unambiguous representation (what the REPL uses to display results)

```python
s = "hello"
print(s)      # hello    (no quotes — str())
print(repr(s)) # 'hello' (with quotes — repr())
```

### 3.3 Boolean Conversions

The `bool()` function reveals Python's **truthiness** rules:

```python
# Falsy values — evaluate to False:
bool(False)   # False
bool(0)       # False
bool(0.0)     # False
bool(0j)      # False (complex zero)
bool("")      # False
bool([])      # False
bool(())      # False
bool({})      # False
bool(set())   # False
bool(None)    # False

# Everything else is Truthy:
bool(1)       # True
bool(-1)      # True (any non-zero number!)
bool(0.001)   # True
bool("a")     # True
bool([0])     # True (non-empty, even if contents are falsy)
bool(" ")     # True (non-empty string)
```

**The truthiness rule is simple:** An object is falsy if it represents "nothing" or "zero". Everything else is truthy.

---

## 4. Working with User Input Safely

`input()` always returns a string. Converting it safely requires handling errors:

```python
# Naive (crashes on bad input):
age = int(input("Enter your age: "))   # Crashes if user types "hello"

# Safe (handles bad input):
age_str = input("Enter your age: ")
try:
    age = int(age_str)
    print(f"You are {age} years old")
except ValueError:
    print(f"'{age_str}' is not a valid integer")
```

We'll study `try/except` fully in Week 10. For now: know that `int()` and `float()` raise `ValueError` on invalid input, and this can be caught.

---

## 5. The `math` Module: Essential Functions

For mathematical operations beyond the basic operators:

```python
import math

# Constants
math.pi      # 3.141592653589793
math.e       # 2.718281828459045
math.inf     # infinity
math.tau     # 6.283... (= 2π)

# Basic functions
math.sqrt(16)       # 4.0 — square root
math.abs(-5)        # 5   — absolute value (also built-in abs())
math.ceil(3.2)      # 4   — round UP to nearest int
math.floor(3.9)     # 3   — round DOWN to nearest int
math.trunc(3.9)     # 3   — truncate toward zero (same as int())
math.trunc(-3.9)    # -3  (not -4!)

# Logarithms and exponentials
math.log(math.e)    # 1.0     — natural log
math.log(100, 10)   # 2.0     — log base 10
math.log2(1024)     # 10.0    — log base 2
math.exp(1)         # 2.718...— e^1

# Trigonometry (radians!)
math.sin(math.pi/2) # 1.0
math.cos(0)         # 1.0
math.degrees(math.pi)  # 180.0  — radians → degrees
math.radians(180)      # 3.14...— degrees → radians

# Float comparison
math.isclose(0.1 + 0.2, 0.3)            # True
math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9)  # True (custom tolerance)
math.isnan(float('nan'))                 # True
math.isinf(float('inf'))                 # True

# Combinatorics (useful!)
math.factorial(5)      # 120 — 5!
math.comb(10, 3)       # 120 — C(10,3) = 10!/(3!×7!) — combinations
math.perm(10, 3)       # 720 — P(10,3) — permutations
math.gcd(12, 8)        # 4   — greatest common divisor
```

---

## 6. The REPL as a Thinking Tool

The REPL is not just for testing code — it is a **thinking environment**. Here is how expert Python programmers use it:

### 6.1 Hypothesis Testing

Before committing to an approach, test your assumptions:

```python
# "I think floor division of negative numbers rounds down..."
>>> -7 // 2
-4    # Yes — toward -∞, not toward zero

# "I think 'in' works on dict values..."
>>> {"a": 1, "b": 2}
{'a': 1, 'b': 2}
>>> "a" in {"a": 1, "b": 2}
True   # Checks keys
>>> 1 in {"a": 1, "b": 2}
False  # Doesn't check values — use .values() for that
>>> 1 in {"a": 1, "b": 2}.values()
True
```

### 6.2 Exploring Unfamiliar Objects

```python
# What can I do with a string?
>>> dir("hello")
['__add__', '__class__', ..., 'capitalize', 'casefold', 'center',
 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', ...]

# What does a method do?
>>> help("hello".center)
Help on built-in function center:

center(width, fillchar=' ', /)
    Return a centered string of length width.
    Padding is done using the specified fill character (default is a space).

>>> "hello".center(11)
'   hello   '
>>> "hello".center(11, "-")
'---hello---'
```

### 6.3 Incremental Development

Build complex expressions one step at a time:

```python
# Goal: Get the average word length in a sentence
sentence = "the quick brown fox jumps over the lazy dog"

# Step 1: Split into words
words = sentence.split()
>>> words
['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']

# Step 2: Get lengths
lengths = [len(w) for w in words]
>>> lengths
[3, 5, 5, 3, 5, 4, 3, 4, 3]

# Step 3: Average
avg = sum(lengths) / len(lengths)
>>> avg
3.888...

# Step 4: Round nicely
>>> round(avg, 2)
3.89
```

Each step is verified in the REPL before combining. This is how you build confidence in complex code.

### 6.4 REPL Shortcuts

```python
_           # The last result
__          # The result before that
___         # The result three steps ago

>>> 2 + 2
4
>>> _ * 3
12          # Uses the 4 from above
>>> _ + _   
24          # Uses the 12 from above
```

---

## 7. String Formatting: The Full Picture

Python has four ways to format strings. Know them all; use f-strings for most things.

### Method 1: f-strings (Python 3.6+) — PREFERRED
```python
name = "Alice"
score = 94.7

f"Name: {name}, Score: {score:.1f}%"
# → 'Name: Alice, Score: 94.7%'
```

### Method 2: `.format()` method
```python
"Name: {}, Score: {:.1f}%".format(name, score)
"Name: {n}, Score: {s:.1f}%".format(n=name, s=score)
```

### Method 3: `%` operator (old-style, C-like) — avoid in new code
```python
"Name: %s, Score: %.1f%%" % (name, score)
```

### Method 4: Template strings (for user-supplied templates)
```python
from string import Template
t = Template("Name: $name, Score: $score")
t.substitute(name=name, score=score)
```

### Format Specification Mini-Language

Inside `{}` in an f-string, after the colon:

```
{value:[[fill]align][sign][#][0][width][grouping][.precision][type]}
```

```python
# Width and alignment
f"{'left':<10}"      # 'left      '  (left-align, width 10)
f"{'right':>10}"     # '     right'  (right-align)
f"{'center':^10}"    # '  center  '  (center)
f"{'center':*^10}"   # '**center**'  (fill with *)

# Numbers
f"{42:05d}"          # '00042'    (zero-padded, width 5)
f"{1234567:,}"       # '1,234,567' (thousands separator)
f"{3.14159:.2f}"     # '3.14'     (2 decimal places)
f"{3.14159:.4g}"     # '3.142'    (4 significant figures)
f"{255:x}"           # 'ff'       (hexadecimal)
f"{255:X}"           # 'FF'       (uppercase hex)
f"{255:08b}"         # '11111111' (binary, 8 digits wide)
f"{3.14e3:.2e}"      # '3.14e+03' (scientific notation)
f"{0.001234:.2%}"    # '0.12%'    (percentage)
```

---

## 8. Putting It All Together: A Complete Program

This program demonstrates all of Week 1's concepts working together:

```python
#!/usr/bin/env python3
"""
bmi_calculator.py
CS 101 — Week 1 Summary Program

Computes Body Mass Index (BMI) and categorizes it.
BMI = weight(kg) / height(m)^2
"""

import math

def get_positive_float(prompt):
    """Prompt user for a positive float, retry on invalid input."""
    while True:
        raw = input(prompt)
        try:
            value = float(raw)
            if value <= 0:
                print("Value must be positive. Try again.")
            else:
                return value
        except ValueError:
            print(f"'{raw}' is not a valid number. Try again.")

def categorize_bmi(bmi):
    """Return the BMI category as a string."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25.0:
        return "Normal weight"
    elif 25.0 <= bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"

print("=" * 40)
print("      BMI Calculator")
print("=" * 40)

unit = input("Use metric (M) or imperial (I)? ").strip().upper()

if unit == "M":
    weight_kg = get_positive_float("Weight in kg: ")
    height_m  = get_positive_float("Height in metres: ")
elif unit == "I":
    weight_lb = get_positive_float("Weight in pounds: ")
    height_in = get_positive_float("Height in inches: ")
    weight_kg = weight_lb * 0.453592
    height_m  = height_in * 0.0254
else:
    print("Invalid unit choice. Exiting.")
    exit()

bmi = weight_kg / (height_m ** 2)
category = categorize_bmi(bmi)

print()
print(f"{'BMI':>12}: {bmi:.1f}")
print(f"{'Category':>12}: {category}")
print()

# Visual representation using bit-level tricks (bonus):
full_blocks = int(bmi) // 5
partial = bmi % 5
bar = "█" * full_blocks + ("▒" if partial >= 2.5 else "")
print(f"Scale: |{bar:<10}| (each █ ≈ 5 BMI units)")
```

This program uses: type conversion, f-strings, format specifiers, `math`, conditional expressions, boolean logic, and `while` (preview of next week).

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Dynamic typing | Variables have no fixed type; objects do |
| Strong typing | Python refuses implicit conversion between unrelated types |
| `int()` | Truncates (toward zero), parses strings, handles bases |
| `round()` | Banker's rounding (round half to even) |
| `bool()` | Falsy: 0, 0.0, "", [], {}, (), None — truthy: everything else |
| `math` module | sqrt, ceil, floor, log, isclose, factorial, gcd |
| REPL workflow | Test → explore → build incrementally |
| f-strings | `f"{value:format_spec}"` — the professional way to format output |

---

## Problem Set 1 Released Today

See [[PS 1 Data Types and Expressions]]. Due next Friday at 11:59 PM. Read it this weekend — start early.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict each formatted result exactly, including spaces.

```python
f"{3.14159:.2f}"
f"{255:#x}"
f"{42:>8,}"
f"{0.5:.0%}"
f"{7:03d}"
f"{2.5:.0f}"
f"{3.5:.0f}"
```

**2. (Explain.)** `math.floor(-2.5)` is `-3`, `int(-2.5)` is `-2`, and `round(-2.5)` is `-2`. All three "convert a float to an integer". State precisely what each one actually promises.

**3. (Build.)** Write a loop that repeatedly prompts for a positive integer and returns it, re-prompting on anything else — a non-number, a negative, or zero. It must never crash and must not loop forever on valid input.

**4. (Stretch.)** `f"{x}"` and `f"{x!r}"` can produce different text. Predict the output of each line, then state when you should prefer `!r` in a program you are debugging.

```python
x = "5"
print(f"value: {x}")
print(f"value: {x!r}")
y = None
print(f"got {y} and {y!r}")
```


### Answers

**1.** `'3.14'`, `'0xff'`, `'      42'` (six spaces then `42`), `'50%'`, `'007'`, `'2'`, `'4'`.

The last pair is the one to remember. `f"{2.5:.0f}"` gives `'2'` and `f"{3.5:.0f}"` gives `'4'` — both round to the **nearest even** value rather than always rounding half up. This is *banker's rounding* (IEEE 754 round-half-to-even), and `round()` does the same: `round(2.5)` is `2`, `round(3.5)` is `4`, `round(-0.5)` is `0`. The reason is statistical — always rounding halves upward biases the sum of a large set of rounded values upward, while rounding to even cancels out. If you need round-half-up for money, use `decimal.Decimal` with an explicit `ROUND_HALF_UP` context; do not try to patch it with `int(x + 0.5)`, which is wrong for negatives.

**2.** They implement three different rules, and the disagreement on `-2.5` is the fastest way to see it.

- `math.floor(x)` — the largest integer **≤ x**. Always rounds toward negative infinity. `-2.5 → -3`.
- `int(x)` — **truncation**: discard the fractional part, rounding toward **zero**. `-2.5 → -2`, and `2.5 → 2`. Note this is not the same as `floor` for negatives, and equals `math.trunc(x)`.
- `round(x)` — nearest integer, ties to **even**. `-2.5 → -2` because `-2` is even; `-3.5 → -4`.

They agree on every positive non-tie value, which is why the difference stays hidden until a negative or a `.5` appears. Choose deliberately: `floor` for bucketing into intervals, `int` for stripping a fraction you have already decided is noise, `round` for presenting a number to a human.

**3.**

```python
def read_positive_int(prompt="Enter a positive integer: "):
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print(f"  {raw!r} is not a whole number.")
            continue
        if value <= 0:
            print(f"  {value} is not positive.")
            continue
        return value
```

The structure matters more than the code. **Convert first, validate second** — you cannot check the sign of something that is not yet a number, so the `try` must come first and must wrap only the conversion. The two failure modes get distinct messages, because "invalid input" tells the user nothing about which rule they broke. And `return` inside `while True` is the clean exit: the loop condition is "forever", and the *validity* test is what ends it.

**4.**

```
value: 5
value: '5'
got None and None
```

`{x}` calls `str(x)`, which is the human-readable form; `{x!r}` calls `repr(x)`, which aims to be an unambiguous form a programmer could paste back into source. For strings these differ — `repr` adds the quotes. For `None` they happen to coincide.

**Use `!r` whenever the point of the message is to identify a value rather than display it.** `Expected a number, got 5` leaves you wondering whether the input was the integer `5` or the string `'5'` — which is exactly the bug you are hunting. `got '5'` answers it. The same reasoning covers trailing whitespace (`'5 '` is visible, `5 ` is not) and empty strings (`''` is visible, nothing is not). In error messages about user input, `!r` should be your default.



---

## Reading

- **Guttag, Ch. 2.3–2.4** — strings and user input
- **Guttag, Ch. 3.1** — simple programs (good end-of-week synthesis)

---

*CS 101 · Week 1 · Lecture 6 (Fri) · © CSE Department*
