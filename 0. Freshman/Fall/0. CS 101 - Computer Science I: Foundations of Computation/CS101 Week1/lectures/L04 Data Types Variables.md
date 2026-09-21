# CS 101 · Lecture 4 (Week 1, Lecture 1)
## Data, Types, and Variables (The Full Picture)

**Week 1 · Wednesday**
*"A type is not just a label — it specifies what operations are legal on a value and how the bits representing it should be interpreted." — Barbara Liskov*

**Date:** Wednesday 30 September 2026 · 09:00–09:50 · Week 1

---

## 0. Where We Are

Week 0 gave you the conceptual landscape: what CS is, what computation means, and a first look at Python. This week we go deeper into the raw material of every program — **data**.

The central question: **what is data, really?** Not "what is a variable" — but what is it *at the machine level*, and why does Python organize it the way it does?

---

## 1. Everything Is Bits

At the hardware level, your computer stores exactly one thing: **bits** — electrical states that are either high (1) or low (0). Everything you have ever seen on a screen — text, images, music, code — is encoded as sequences of bits.

The **type system** is the layer that gives bits meaning.

```
Bits:       01000001
As uint8:   65
As ASCII:   'A'
As part of float: (depends on context)
```

The same 8 bits `01000001` mean completely different things depending on how you interpret them. **A type tells the program how to interpret a region of memory.**

This is why Python's type system is not arbitrary — it reflects a fundamental truth about computation.

---

## 2. Python's Object Model: Deep Dive

In Python, **everything is an object.** Not as a figure of speech — literally. Every value, every function, every class, every module is an object in memory.

An object has three attributes:
1. **Identity**: its address in memory (what `id()` returns)
2. **Type**: the class it belongs to (what `type()` returns)
3. **Value**: the data it holds

```python
x = 42

id(x)      # e.g. 140234567890432  — memory address
type(x)    # <class 'int'>
x          # 42 — the value
```

### 2.1 Mutable vs. Immutable Objects

This is one of the most important distinctions in Python:

**Immutable** objects cannot be changed after creation:
- `int`, `float`, `bool`, `str`, `tuple`, `frozenset`

**Mutable** objects can be changed in place:
- `list`, `dict`, `set`

```python
# Immutable example:
x = "hello"
x[0] = "H"     # TypeError! Strings are immutable

# Why does this work then?
x = "Hello"    # This doesn't change the string — it makes x point to a new object
```

```python
# Mutable example:
lst = [1, 2, 3]
lst[0] = 99     # Works! Lists are mutable
print(lst)      # [99, 2, 3]

# The list object itself changed — it's still the same object
a = [1, 2, 3]
b = a           # b points to the SAME list
b[0] = 99
print(a)        # [99, 2, 3] — a changed too!
```

**Why does mutability matter?**

It determines how objects behave when passed to functions, when assigned to multiple variables, and when used as dictionary keys. We will see the consequences repeatedly throughout this course.

### 2.2 Reference Counting and Memory

Python uses **reference counting** to manage memory. Every object has an internal counter tracking how many variables (references) point to it.

```python
a = [1, 2, 3]   # List created; reference count = 1
b = a            # b also points to it; reference count = 2
c = a            # c also points to it; reference count = 3
del b            # reference count = 2
del c            # reference count = 1
del a            # reference count = 0 → object is freed
```

When the count reaches 0, the garbage collector reclaims the memory. You don't manage memory manually in Python — but understanding this model explains why certain bugs occur.

---

## 3. Integers: The Full Picture

### 3.1 Arbitrary Precision

Python integers have **no fixed size**. They grow as large as needed:

```python
>>> 2 ** 1000
107150860718626732094842504906000181056...  # 302 digits!
```

Contrast with C's `int`: fixed at 32 bits, max value 2,147,483,647. Exceed it and you get silent overflow — one of the most dangerous bug classes in systems programming.

Python pays for arbitrary precision with **speed and memory**: Python integers are heap-allocated objects, while C integers live in registers. For most programs, this trade-off is worth it.

### 3.2 Integer Interning

`CPython` (the standard Python implementation) **interns** small integers — it pre-creates the integers from -5 to 256 and reuses those objects instead of creating new ones.

```python
>>> a = 5
>>> b = 5
>>> a is b        # True — same object!
True

>>> a = 1000
>>> b = 1000
>>> a is b        # False — different objects
False
```

**Lesson:** Never use `is` to compare values — use `==`. `is` tests object identity (same memory address), not value equality. The only correct use of `is` is `x is None`.

### 3.3 Integer Division: The Two Types

```python
10 / 3      # → 3.3333...   True division (always returns float)
10 // 3     # → 3           Floor division (rounds toward -∞)
-10 // 3    # → -4          Note: NOT -3! Floor means toward -∞
10 % 3      # → 1           Modulo
-10 % 3     # → 2           In Python, sign matches the divisor
```

**The mathematical relationship (always holds):**
```
a == (a // b) * b + (a % b)
```

Verify: `-10 == (-10 // 3) * 3 + (-10 % 3)` → `-10 == -4 * 3 + 2` → `-10 == -12 + 2` → `-10 == -10` ✓

---

## 4. Floating-Point: The Honest Truth

### 4.1 IEEE 754 Double Precision

Python `float` is IEEE 754 **double precision**: 64 bits structured as:
- 1 bit: sign
- 11 bits: exponent (biased by 1023)
- 52 bits: mantissa (with implicit leading 1)

The value is: `(-1)^sign × 1.mantissa × 2^(exponent - 1023)`

This format can represent:
- Numbers from ~±5×10⁻³²⁴ to ~±1.8×10³⁰⁸
- About 15–17 significant decimal digits

### 4.2 Why 0.1 + 0.2 ≠ 0.3

`0.1` in binary is `0.000110011001100110011...` — a repeating pattern, like `1/3` in decimal. It cannot be stored exactly in 52 bits. The closest representable value is:
```
0.1 → 0.1000000000000000055511151231257827021181583404541015625
```

When you add two approximations, you get a slightly-off result:
```python
>>> 0.1 + 0.2
0.30000000000000004
```

This is not a Python bug. It's fundamental to binary floating-point.

### 4.3 Correct Float Comparison

```python
import math

# WRONG — almost never use == with floats
if 0.1 + 0.2 == 0.3:
    print("equal")   # Never prints!

# CORRECT — use math.isclose (relative tolerance)
if math.isclose(0.1 + 0.2, 0.3):
    print("approximately equal")   # Prints

# For absolute tolerance:
EPSILON = 1e-9
if abs((0.1 + 0.2) - 0.3) < EPSILON:
    print("close enough")
```

### 4.4 Special Float Values

```python
>>> float('inf')       # Positive infinity
inf
>>> float('-inf')      # Negative infinity
-inf
>>> float('nan')       # Not a Number
nan
>>> float('nan') == float('nan')   # NaN is not equal to itself!
False
>>> import math
>>> math.isnan(float('nan'))       # Correct way to check
True
>>> 1 / 0              # ZeroDivisionError (integer division)
ZeroDivisionError
>>> 1.0 / 0.0          # ZeroDivisionError (float division too, in Python)
ZeroDivisionError
```

---

## 5. Strings: Deep Dive

### 5.1 Strings Are Unicode

Python 3 strings are **Unicode** by default — they can contain characters from any language:

```python
>>> "Hello, 世界!"
'Hello, 世界!'
>>> "Привет"       # Russian
'Привет'
>>> "مرحبا"        # Arabic
'مرحبا'
>>> len("Hello")
5
>>> len("世界")
2   # Two characters (not 6 bytes!)
```

This matters when processing text from real-world sources.

### 5.2 String Indexing and Slicing

Strings are **sequences**, ordered collections of characters. Each character has an index:

```
 H  e  l  l  o  ,     W  o  r  l  d  !
 0  1  2  3  4  5  6  7  8  9 10 11 12
-13-12-11-10 -9 -8 -7 -6 -5 -4 -3 -2 -1
```

```python
s = "Hello, World!"

# Indexing
s[0]      # 'H'
s[7]      # 'W'
s[-1]     # '!'  (last character)
s[-2]     # 'd'  (second to last)

# Slicing: s[start:stop:step]  (stop is EXCLUDED)
s[0:5]    # 'Hello'   (indices 0,1,2,3,4)
s[7:12]   # 'World'
s[7:]     # 'World!'  (to the end)
s[:5]     # 'Hello'   (from the start)
s[::2]    # 'Hlo ol!' (every 2nd character)
s[::-1]   # '!dlroW ,olleH' (reversed)
```

### 5.3 String Immutability

Strings cannot be modified, any operation that "changes" a string actually creates a new one:

```python
s = "hello"
s[0] = "H"    # TypeError: 'str' object does not support item assignment

# What you do instead:
s = "H" + s[1:]   # → "Hello"  (creates a new string)
```

This has **performance implications**: building a string by concatenating in a loop is O(n²):

```python
# SLOW — O(n²) — creates a new string object each iteration
result = ""
for word in words:
    result = result + word + " "   # Each + creates a new string!

# FAST — O(n) — join at the end
result = " ".join(words)
```

### 5.4 f-Strings: The Professional Way to Format

```python
name = "Alice"
score = 94.7332
items = [1, 2, 3]

# Basic substitution
f"Name: {name}"                  # 'Name: Alice'

# Formatting numbers
f"Score: {score:.2f}"            # 'Score: 94.73'   (2 decimal places)
f"Score: {score:.0f}"            # 'Score: 95'      (rounded integer)
f"Count: {len(items):03d}"       # 'Count: 003'     (zero-padded, width 3)
f"Hex: {255:08x}"                # 'Hex: 000000ff'  (hex, 8 chars wide)
f"Sci: {0.000123:.2e}"           # 'Sci: 1.23e-04'  (scientific notation)

# Expressions inside braces
f"Double: {score * 2:.1f}"       # 'Double: 189.5'
f"Upper: {name.upper()}"         # 'Upper: ALICE'
f"List: {', '.join(map(str, items))}"  # 'List: 1, 2, 3'

# Debug format (Python 3.8+)
f"score={score!r}"               # 'score=94.7332'  (repr, shows variable name)
f"{score=}"                      # 'score=94.7332'  (shorthand)
```

---

## 6. Variables and Assignment: The Complete Model

### 6.1 Assignment is Name Binding

```python
x = 42
```

This statement:
1. Evaluates the right-hand side (creates the integer object `42`)
2. Binds the name `x` to that object in the current **namespace**

```python
x = 42
y = x      # y now references the same object as x
print(x is y)   # True (for small ints, due to interning)
```

### 6.2 Augmented Assignment

```python
x = 10
x += 5    # x = x + 5 = 15
x -= 3    # x = x - 3 = 12
x *= 2    # x = x * 2 = 24
x //= 5   # x = x // 5 = 4
x **= 3   # x = x ** 3 = 64
x %= 10   # x = x % 10 = 4
```

**Subtle point:** For immutable types (int, str), `x += 1` creates a new object and rebinds `x`. For mutable types (list), `x += [1]` modifies the existing object:

```python
a = [1, 2]
b = a
a += [3]      # Modifies the list in place
print(b)      # [1, 2, 3] — b sees the change!

a = [1, 2]
b = a
a = a + [3]   # Creates a new list, rebinds a
print(b)      # [1, 2] — b is unchanged
```

### 6.3 Multiple Assignment and Unpacking

```python
# Multiple targets
a = b = c = 0    # All three reference the same object

# Tuple unpacking
x, y = 10, 20
x, y = y, x     # Swap — Python evaluates the right side fully first

# Extended unpacking (Python 3)
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

*init, last = [1, 2, 3, 4, 5]
# init = [1, 2, 3, 4], last = 5

a, *middle, z = [1, 2, 3, 4, 5]
# a = 1, middle = [2, 3, 4], z = 5
```

---

## 7. Python's Built-in Functions for Data

Essential built-ins you should know:

```python
# Type and identity
type(x)          # Returns the type of x
isinstance(x, T) # True if x is an instance of type T
id(x)            # Memory address of x

# Math
abs(-5)          # 5 — absolute value
round(3.7)       # 4 — round to nearest int
round(3.14159, 2)# 3.14 — round to 2 decimal places
max(3, 1, 4, 1)  # 4
min(3, 1, 4, 1)  # 1
sum([1, 2, 3])   # 6
pow(2, 10)       # 1024 (same as 2**10, but can take 3 args for modular exponentiation)

# Conversions
int(x)   float(x)   str(x)   bool(x)   list(x)   tuple(x)

# Length and range
len("hello")     # 5
range(5)         # 0, 1, 2, 3, 4 (we'll use this extensively in Week 2)
range(2, 8)      # 2, 3, 4, 5, 6, 7
range(0, 10, 2)  # 0, 2, 4, 6, 8
```

---

## 8. The `None` Type: When There Is No Value

`None` is Python's null value, the absence of a meaningful value.

```python
result = None          # Explicit "no value yet"
type(None)             # <class 'NoneType'>

# Correct comparison:
if result is None:     # Use 'is', not '=='
    print("no result")

# Functions without return statements return None:
def do_something():
    x = 1 + 1          # No return statement
    
print(do_something())  # prints: None
```

`None` is the only value of type `NoneType`. It is a singleton — there is exactly one `None` object in any Python program. That's why `is None` is the correct comparison: there's only one `None` to be identical to.

---

## 9. Summary Table

| Type | Mutable? | Examples | Key Operations |
|------|---------|---------|----------------|
| `int` | No | `42`, `2**100` | `+`, `-`, `*`, `//`, `%`, `**` |
| `float` | No | `3.14`, `1e-10` | Arithmetic, beware `==` |
| `bool` | No | `True`, `False` | `and`, `or`, `not` |
| `str` | No | `"hello"`, `f"{x:.2f}"` | `+`, `*`, slicing, `.upper()`, `.split()` |
| `None` | No | `None` | `is None`, `is not None` |
| `list` | **Yes** | `[1, 2, 3]` | Indexing, `.append()`, `.sort()` |
| `tuple` | No | `(1, 2, 3)` | Indexing, unpacking |
| `dict` | **Yes** | `{"a": 1}` | `[key]`, `.get()`, `.items()` |
| `set` | **Yes** | `{1, 2, 3}` | `in`, `|`, `&`, `-` |

*(Lists, tuples, dicts, sets covered fully in Weeks 7–8)*

---

## Key Takeaways

1. **Types give meaning to bits.** The same bit pattern means different things depending on type.
2. **Everything is an object.** Every value has identity, type, and value.
3. **Mutable vs. immutable** is one of the most consequential distinctions in Python.
4. **Float arithmetic is approximate.** Never use `==` to compare floats.
5. **Variables are labels**, not boxes. Multiple labels can point to the same object.
6. **`is` tests identity, `==` tests equality.** Use `is` only for `None`.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict the output, then run it. Explain the difference between the two halves in terms of the object model from §2.

```python
x = [1, 2, 3]
y = x
y += [4]
print(x)

z = [1, 2, 3]
w = z
w = w + [4]
print(z)
```

**2. (Explain.)** Run these two lines and explain the results.

```python
print(int("100") is int("100"))    # True
print(int("1000") is int("1000"))  # False
```

Then state the rule about when `is` may be used on integers.

**3. (Build.)** §4 shows that `0.1 + 0.2 != 0.3`. Write a function `close(a, b, tol=1e-9)` that reports whether two floats are equal to within a tolerance, and explain why comparing against an *absolute* tolerance alone is not good enough for large values.

**4. (Stretch.)** Python integers have arbitrary precision — `2 ** 200` is computed exactly, with no overflow. C's `int` is typically 32 bits and wraps around. State one concrete advantage each design has over the other, then explain which one a cryptography library needs and why.


### Answers

**1.** `[1, 2, 3, 4]` then `[1, 2, 3]`.

`+=` on a list calls `__iadd__`, which **mutates the object in place** and then rebinds the same object to the name — so the single list that both `x` and `y` label is modified, and `x` sees it. `w = w + [4]` calls `__add__`, which **builds a new list**, leaving the original untouched; only the label `w` moves. `z` still labels the original.

So for lists, `a += b` and `a = a + b` are *not* interchangeable. For immutable types they are, since there is no in-place option — which is exactly why the distinction is invisible until the first time it bites you.

**2.** CPython pre-allocates a single object for every small integer in the range **−5 to 256** and hands out the same one every time. `100` is in that range, so both calls return the identical object and `is` is `True`. `1000` is not, so each call builds a fresh object and `is` is `False`.

The rule: **never use `is` to compare integers** (or any numbers, or strings). It asks "are these the same object?" when you mean "are these equal?" — use `==`. The small-int cache is a CPython implementation detail, is not part of the language, and differs between interpreters and versions.

One subtlety worth knowing: written as `a = 1000; b = 1000` on a single line inside a function, `a is b` may be `True` — the compiler folds identical literals in one code object into one constant. Calling `int()` defeats that folding, which is why the exercise is phrased this way.

**3.**

```python
def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(abs(a), abs(b), 1.0)
```

A pure absolute test, `abs(a - b) <= tol`, fails at scale. Doubles carry about 15–16 significant decimal digits, so near `1e12` the *smallest possible gap* between representable neighbours is already larger than `1e-9` — two values as close as floating point can express would be reported unequal. Scaling the tolerance by the magnitude of the operands (a **relative** tolerance) tracks the precision actually available. The `max(..., 1.0)` keeps the test from collapsing to `a == b` when both are near zero, where a relative tolerance is meaningless.

Python ships this as `math.isclose(a, b, rel_tol=..., abs_tol=...)`, which combines both and is what you should use in real code. Writing it once yourself is how you learn what its parameters mean.

**4.** **Arbitrary precision** is correct by construction: no overflow bugs, no silent wraparound, and results match ordinary mathematics. **Fixed width** is fast and predictable: an `int` fits in a register, arithmetic is one instruction, and every value occupies exactly the same known number of bytes, which matters for arrays, structs, and anything laid out in memory. Python's integers are heap objects with a sign, a length, and a digit array — roughly 28 bytes for a small one, and the arithmetic is a function call rather than an instruction.

Cryptography needs **arbitrary precision**. RSA operates on integers of 2048 bits or more, and it needs them exact — a wraparound in a modular exponentiation does not produce a slightly wrong answer, it produces a broken cipher. This is why C cryptography libraries do not use `int` at all; they ship their own big-integer implementation (GMP, or OpenSSL's BIGNUM) that reconstructs in C what Python gives you by default. The catch: those implementations must also run in **constant time** regardless of the operand values, since timing differences leak key material — which Python's `int` does not guarantee.



---

## Reading

- **Guttag, Ch. 2** — sections 2.1 and 2.3 (types, variables, expressions)
- **Guttag, Ch. 3.1** — strings in depth

---

*CS 101 · Week 1 · Lecture 4 (Wed) · © CSE Department*
