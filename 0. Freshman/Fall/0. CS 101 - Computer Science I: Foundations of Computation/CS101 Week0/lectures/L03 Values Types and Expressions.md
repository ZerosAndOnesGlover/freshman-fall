# CS 101 · Lecture 3
## Values, Types, and Expressions

**Week 0 · Lecture 3 of 3**
*"A type is a set of values together with a set of operations on those values." — Barbara Liskov*

**Date:** Friday 21 August 2026 · 09:00–09:50 · Week 0

---

## 0. The Atom of Computation

Everything a computer program does comes down to **computing values from other values**. Before we can write interesting programs, we need to understand the raw material: what values exist, how they are categorized (types), and how they can be combined (expressions).

---

## 1. Values and Objects in Python

In Python, everything is an **object**: an entity in memory with:
1. A **value** (the data it holds, e.g., `42`)
2. A **type** (what kind of thing it is, e.g., `int`)
3. An **identity** (its location in memory, accessible via `id()`)

```python
>>> x = 42
>>> x           # The value
42
>>> type(x)     # The type
<class 'int'>
>>> id(x)       # The identity (memory address)
140234567890432  # (will differ on your machine)
```

---

## 2. Python's Core Types

### 2.1 Integers (`int`)

Whole numbers with no fractional part.

```python
>>> 42
42
>>> -17
-17
>>> 0
0
>>> 1_000_000    # Underscores allowed for readability (Python 3.6+)
1000000
```

**Crucial fact:** Python integers have **arbitrary precision** — they can be as large as your memory allows. This is unusual. In C, an `int` is 32 bits (max ~2.1 billion). In Python:

```python
>>> 2 ** 1000
10715086071862673209484250490600018105614048117055336074437503883703510511249361224931983788156958581275946729175531468251871452856923140435984577574698574803934567774824230985421074605062371141877954182153046474983581941267398767559165543946077062914571196477686542167660429831652624386837205668069376
```

This makes Python excellent for cryptography and mathematical computation.

### 2.2 Floating-Point Numbers (`float`)

Numbers with a decimal point: stored in IEEE 754 double-precision binary format (64 bits).

```python
>>> 3.14
3.14
>>> 2.0
2.0
>>> 1.5e10       # Scientific notation: 1.5 × 10^10
15000000000.0
>>> 1.5e-3       # 1.5 × 10^-3
0.0015
```

**⚠️ Critical Warning: Floating-Point Imprecision**

```python
>>> 0.1 + 0.2
0.30000000000000004   # Not 0.3!
```

This is not a Python bug. It is fundamental to how binary floating-point works. The decimal `0.1` cannot be represented exactly in binary (just as `1/3` cannot be represented exactly in decimal). It is stored as the closest possible binary approximation.

**Consequence:** **Never compare floats with `==`.**

```python
# WRONG:
if 0.1 + 0.2 == 0.3:   # This is False in Python!
    print("equal")

# CORRECT:
import math
if math.isclose(0.1 + 0.2, 0.3):
    print("approximately equal")

# Or with a tolerance:
if abs((0.1 + 0.2) - 0.3) < 1e-9:
    print("close enough")
```

This matters enormously in scientific computing, financial software, and game physics.

### 2.3 Booleans (`bool`)

The simplest type — exactly two values:

```python
>>> True
True
>>> False
False
>>> type(True)
<class 'bool'>
```

**Booleans are integers in Python** (True = 1, False = 0):
```python
>>> True + True
2
>>> True * 5
5
>>> False + 1
1
```

This is occasionally useful (counting True values in a list), but mostly a curiosity to be aware of.

**Truthiness:** In Python, many non-boolean values are considered "truthy" or "falsy":

```python
# Falsy values (evaluate to False in a boolean context):
False, 0, 0.0, "", [], {}, (), None

# Everything else is truthy
```

```python
>>> bool(0)
False
>>> bool(42)
True
>>> bool("")
False
>>> bool("hello")
True
>>> bool([])
False
>>> bool([1, 2, 3])
True
```

### 2.4 Strings (`str`)

Sequences of **Unicode characters** — text.

```python
>>> "Hello, World!"
'Hello, World!'
>>> 'Single quotes work too'
'Single quotes work too'
>>> """
... Triple quotes
... can span
... multiple lines
... """
'\nTriple quotes\ncan span\nmultiple lines\n'
```

**Key string operations:**
```python
s = "Hello, World!"

len(s)          # 13 — number of characters
s[0]            # 'H' — indexing (0-based)
s[-1]           # '!' — negative indexing (from the end)
s[0:5]          # 'Hello' — slicing
s[7:]           # 'World!' — slice to end
s[:5]           # 'Hello' — slice from beginning
s.upper()       # 'HELLO, WORLD!'
s.lower()       # 'hello, world!'
s.replace("World", "Python")  # 'Hello, Python!'
s.split(", ")   # ['Hello', 'World!']
" spaces ".strip()   # 'spaces' — removes leading/trailing whitespace
```

**String concatenation:**
```python
>>> "Hello" + " " + "World"
'Hello World'
>>> "ha" * 3
'hahaha'
```

**f-strings (formatted string literals) — use these constantly:**
```python
name = "Alice"
score = 94.7
>>> f"Student {name} scored {score:.1f}%"
'Student Alice scored 94.7%'
```

The `:.1f` inside the braces is a **format specifier**: show as a float with 1 decimal place.

### 2.5 `None`

The absence of a value. Not the same as 0, not the same as False, not the same as an empty string.

```python
>>> x = None
>>> type(x)
<class 'NoneType'>
>>> x is None    # The correct way to check for None
True
>>> x == None    # Works but not idiomatic
True
```

`None` is Python's way of saying "there is no value here." Functions that don't explicitly return something return `None`.

---

## 3. Expressions and Evaluation

An **expression** is any combination of values, variables, operators, and function calls that Python can evaluate to produce a value.

```python
2 + 2                  # Expression — evaluates to 4
"Hello" + " World"     # Expression — evaluates to "Hello World"
len("CS101")           # Expression — evaluates to 5
x > 0                  # Expression — evaluates to True or False
x if x > 0 else -x     # Expression — conditional expression (ternary)
```

An **expression** produces a value. A **statement** performs an action. This distinction matters:

```python
x = 5          # Statement (assignment) — doesn't produce a value
print(x)       # Statement (function call used for side effect)
x + 3          # Expression — produces 8, but if you don't use it, it's discarded
y = x + 3      # Assignment statement containing an expression on the right
```

---

## 4. Operators and Precedence

### Arithmetic Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `3 + 4` | `7` |
| `-` | Subtraction | `10 - 3` | `7` |
| `*` | Multiplication | `3 * 4` | `12` |
| `/` | Division | `10 / 3` | `3.333...` |
| `//` | Floor Division | `10 // 3` | `3` |
| `%` | Modulo | `10 % 3` | `1` |
| `**` | Exponentiation | `2 ** 8` | `256` |
| `-` | Unary negation | `-5` | `-5` |

### Comparison Operators (return bool)

```python
==    # Equal to
!=    # Not equal to
<     # Less than
>     # Greater than
<=    # Less than or equal
>=    # Greater than or equal
```

**Warning:** `=` is assignment. `==` is comparison. Confusing them is one of the most common beginner errors.

### Logical Operators

```python
and   # True if both operands are True
or    # True if at least one operand is True
not   # Inverts True/False
```

```python
>>> True and False
False
>>> True or False
True
>>> not True
False
>>> (3 > 2) and (5 < 10)
True
```

**Short-circuit evaluation:** Python stops evaluating `and` as soon as it finds a `False`, and `or` as soon as it finds a `True`.

```python
>>> False and (1/0 == 1)   # Second part never evaluated!
False
>>> True or (1/0 == 1)     # Second part never evaluated!
True
```

This is not just an optimization — it enables patterns like:
```python
if x is not None and x > 0:   # Safe: won't compare None > 0 if x is None
    ...
```

### Operator Precedence (highest to lowest)

| Precedence | Operators |
|-----------|-----------|
| 1 (highest) | `()` — parentheses |
| 2 | `**` — exponentiation |
| 3 | `+x`, `-x` — unary operators |
| 4 | `*`, `/`, `//`, `%` |
| 5 | `+`, `-` |
| 6 | `<`, `<=`, `>`, `>=` |
| 7 | `==`, `!=` |
| 8 | `not` |
| 9 | `and` |
| 10 (lowest) | `or` |

**Advice:** When in doubt, use parentheses. They make intent explicit and eliminate ambiguity.

```python
# Ambiguous:
x = 2 + 3 * 4 - 1

# Explicit (much better):
x = 2 + (3 * 4) - 1
```

---

## 5. Type Conversion

### Implicit Conversion (Coercion)

Python automatically converts some types in certain contexts:

```python
>>> 3 + 4.0      # int + float → float
7.0
>>> True + 5     # bool + int → int
6
```

### Explicit Conversion (Casting)

You can explicitly convert between types:

```python
>>> int(3.9)      # → 3 (truncates, does NOT round)
>>> int("42")     # → 42 (converts string to int)
>>> int("3.9")    # → ValueError! Cannot convert directly
>>> float(42)     # → 42.0
>>> float("3.14") # → 3.14
>>> str(42)       # → "42"
>>> bool(0)       # → False
>>> bool("hello") # → True
```

```python
# Common pattern: getting a number from user input
user_input = input("Enter a number: ")   # input() always returns a string
number = int(user_input)                  # convert to int for arithmetic
print(f"Double your number: {number * 2}")
```

---

## 6. The `input()` Function

Your program's first connection to the outside world:

```python
name = input("What is your name? ")   # Prints prompt, waits for user, returns string
print(f"Hello, {name}!")
```

`input()` **always returns a string**, even if the user types a number. Always convert if you need arithmetic.

```python
age_str = input("How old are you? ")
age = int(age_str)
next_year = age + 1
print(f"Next year you'll be {next_year}")
```

---

## 7. Thinking About Types Rigorously

Here is a question to test your understanding:

```python
x = "5"
y = 3
z = x + y    # What happens?
```

```
TypeError: can only concatenate str (not "int") to str
```

Python does not automatically convert "5" to an integer. The `+` operator is defined on str and str (concatenation), or int and int (addition), but not str and int.

```python
# Fix 1: convert x to int
z = int(x) + y    # → 8

# Fix 2: convert y to str
z = x + str(y)    # → "53" (string concatenation!)
```

**The lesson:** Types define what operations are legal. This is not an arbitrary restriction — it prevents logical errors. Adding the string "5" to the number 3 is meaningless. The type system forces you to be explicit about your intent.

---

## 8. Putting It Together: A First Real Program

```python
# temperature_converter.py
# Converts between Celsius and Fahrenheit
# CS 101 — Week 0

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

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
```

Notice how this program uses:
- Variable assignment
- Function definitions (preview of Week 3)
- Type conversion (`float()`)
- String methods (`.strip()`, `.upper()`)
- f-strings with format specifiers (`:.2f`)
- Conditional logic (preview of Week 2)

You do not need to fully understand all of this yet — but read it and notice that it reads almost like English.

---

## 9. Summary

| Type | Description | Example |
|------|-------------|---------|
| `int` | Arbitrary-precision integers | `42`, `-17`, `2**100` |
| `float` | IEEE 754 double precision | `3.14`, `1.5e-10` |
| `bool` | True or False | `True`, `False` |
| `str` | Unicode character sequences | `"Hello"`, `f"{x:.2f}"` |
| `None` | Absence of a value | `None` |

| Concept | Key Point |
|---------|-----------|
| Expression | Any code that evaluates to a value |
| Statement | Code that performs an action |
| Operator Precedence | `**` > `*/%` > `+-` > comparisons > `not` > `and` > `or` |
| Type Conversion | Python doesn't auto-convert between unrelated types; be explicit |
| Float imprecision | Never compare floats with `==`; use `math.isclose()` |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Evaluate each of these by hand using the precedence table in §4, then check in the REPL. Three of the six commonly surprise people.

```python
2 ** 3 ** 2
-2 ** 2
7 // -2
7 % -2
-7 % 2
10 / 2
```

**2. (Explain.)** `int("42")` succeeds and `int("3.0")` raises `ValueError`, even though `int(3.0)` succeeds and returns `3`. Explain why this is deliberate rather than an inconsistency.

**3. (Build.)** Write a program that reads a temperature in Celsius from the user and prints it in Fahrenheit to one decimal place. It must not crash on non-numeric input; instead it should print a clear message. Use only material from this lecture plus `try`/`except ValueError`.

**4. (Stretch.)** `bool` is a subclass of `int` in Python, with `True == 1` and `False == 0`. Predict the value of each expression below, then explain what practical technique the last one enables.

```python
True + True
sum([True, False, True, True])
[10, 20][True]
```


### Answers

**1.** `512`, `-4`, `-4`, `-1`, `1`, `5.0`.

- `2 ** 3 ** 2` — `**` is **right**-associative, so this is `2 ** 9 = 512`, not `8 ** 2 = 64`. It is the only right-associative arithmetic operator in Python.
- `-2 ** 2` — `**` binds tighter than unary minus, so this is `-(2 ** 2) = -4`. Write `(-2) ** 2` if you meant `4`.
- `7 // -2 = -4` — floor division rounds toward **negative infinity**, not toward zero. `-3.5` floors to `-4`.
- `7 % -2 = -1` and `-7 % 2 = 1` — Python's `%` takes the **sign of the divisor**, which is the choice that makes `a == (a // b) * b + a % b` hold. C makes the opposite choice, so `-7 % 2` is `-1` in C. PROG 101 Week 1 revisits this.
- `10 / 2 = 5.0` — a `float`. In Python 3, `/` is always true division even when the operands divide exactly. Use `//` when you want an `int`.

**2.** The two calls do genuinely different jobs that happen to share a name. `int(3.0)` performs a **numeric conversion**: the argument is already a number, and the documented behaviour is to truncate toward zero. `int("3.0")` performs **parsing**: it reads a string according to the grammar of an integer literal, and `3.0` is not an integer literal, so parsing fails. Python refuses to silently chain string→float→truncate, because doing so would make `int("3.9")` return `3` and quietly discard data the user explicitly typed. If you want that, ask for it: `int(float("3.9"))`. The design principle is that conversions that lose information should be visible in the source.

**3.**

```python
raw = input("Temperature in Celsius: ")

try:
    celsius = float(raw)
except ValueError:
    print(f"Not a number: {raw!r}")
else:
    fahrenheit = celsius * 9 / 5 + 32
    print(f"{celsius:.1f} C = {fahrenheit:.1f} F")
```

Three things worth noting. `input()` **always** returns a string — the conversion is yours to do and yours to guard. `float`, not `int`, because `-3.5` is a legitimate temperature. And the conversion sits alone in the `try` with the rest in `else`, so an unrelated bug in the arithmetic is not silently caught and mislabelled as bad input.

**4.** `2`, `3`, and `20`.

Because `True` *is* `1` numerically, arithmetic on booleans is defined and useful. The second expression is the technique: **`sum()` over a list of booleans counts how many are true**, which makes `sum(c.isdigit() for c in s)` an idiomatic one-line digit count. The third — indexing a list with a boolean — is legal for the same reason but is poor style; it works, but a reader has to stop and reconstruct why. Use a conditional expression instead.

This unification is not universal across languages. C has no `bool` before C99 and uses `int` throughout; Java's `boolean` is a genuinely separate type where `true + true` is a compile error. Python chose subclassing for backward compatibility when `bool` was added in 2.3.



---

## Reading for This Week

- **Guttag, Ch. 2**: "Introduction to Python" (covers types and expressions in depth)
- REPL exploration: try every example in this lecture in the Python REPL before Lab 0

---

## Lab 0 Preview

In Lab 0 (Tuesday), you will:
1. Verify your Python, VS Code, and Git installations
2. Run your first Python programs
3. Experiment with types and expressions in the REPL
4. Make your first Git commit
5. Solve 3 warm-up exercises

See you there.

---

*CS 101 · Week 0 · Lecture 3 · © CSE Department*
