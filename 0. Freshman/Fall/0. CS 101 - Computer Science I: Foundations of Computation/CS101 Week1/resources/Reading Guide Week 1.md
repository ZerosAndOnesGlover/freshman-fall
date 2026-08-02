# CS 101 Week 1 Reading Guide & Resources
## Data, Types, Variables, and Expressions

---

## Required Reading

### Guttag: Introduction to Computation and Programming Using Python

**Chapter 2: Introduction to Python**
- §2.1 The Basic Elements of Python (types, operators, variables)
- §2.2 Branching Programs (preview of conditionals: we'll return to this in Week 2)
- §2.3 Strings and Input (strings in depth, `input()`)

**Chapter 3: Some Simple Numerical Programs**
- §3.1 Exhaustive Enumeration (first loop programs, preview of Week 2)
- Read this as context for where we're heading, not required to implement yet

**What to focus on:** The parts you should understand deeply after this week:
- How Python stores values as objects with identity, type, and value
- The distinction between expressions and statements
- How type conversion works (and fails)
- String indexing, slicing, and methods

---

## Focused REPL Sessions

Run these deliberately in the REPL. Don't just type them, **predict first, then check.**

### Session A: Understanding Mutability (15 min)

```python
# Test 1: int (immutable)
a = 1000
b = a
b += 1
print(a, b)       # What's the output?
print(a is b)     # Same object?

# Test 2: list (mutable)
a = [1, 2, 3]
b = a
b.append(4)
print(a, b)       # What's the output?
print(a is b)     # Same object?

# Test 3: list copy
a = [1, 2, 3]
b = a.copy()       # Explicit copy!
b.append(4)
print(a, b)        # What's the output now?
print(a is b)

# Test 4: string (immutable)
s = "hello"
t = s
s = s + " world"
print(s, t)        # What's the output?
print(s is t)
```

**Record:** What pattern do you see? Can you state the rule in one sentence?

### Session B: Short-Circuit Evaluation (10 min)

```python
# What does this return? (not just True/False — the actual value!)
0 and "hello"
1 and "hello"
"" and "hello"
"a" and "hello"

False or "default"
True or "default"
0 or 0.0 or [] or "found it"
0 or 0.0 or [] or {}

# Useful patterns:
name = ""
display = name or "Anonymous"   # What is display?

value = None
safe  = value is not None and value > 0  # No AttributeError if value is None!
```

### Session C: Type Edges (10 min)

```python
# Banker's rounding — verify the pattern
[round(x + 0.5) for x in range(10)]

# int() direction
int(-0.9)    # Does it round toward 0 or toward -∞?
int(-1.9)    # Confirm your rule

# String to int: bases
int("1010", 2)    # binary
int("ff", 16)     # hex
int("77", 8)      # octal
int("z", 36)      # base-36 (uses a-z for digits 10-35)

# Overflow behavior
import sys
sys.maxsize        # Largest int that fits in a C long on this system
sys.maxsize + 1    # Does Python handle it?
sys.float_info.max # Largest float
sys.float_info.max * 2  # Overflow to infinity, no error
```

---

## Conceptual Exercises (Without a Computer)

Work these out on paper. Then verify with the REPL.

**Exercise 1:** Trace the execution of this code. What is printed?

```python
x = 10
y = x
x = x + 5
print(x, y)
```

**Exercise 2:** Trace the execution. What is printed?

```python
lst = [1, 2, 3]
other = lst
lst = lst + [4]    # Note: +, not .append()!
print(lst)
print(other)
print(lst is other)
```

**Exercise 3:** What is the output?

```python
a = True
b = False
print(a + b + a + b + a)
print(type(a + b + a + b + a))
```

**Exercise 4:** Without running it, determine if each expression raises an error. If not, give the result and type.

```python
int("") 
float("inf")
str(None)
bool([None])
"abc"[3]
"abc"[-4]
"hello"[1:10]   # Slicing beyond end — error or not?
```

---

## Key Concepts Map

```
DATA IN PYTHON
│
├── Everything is an object
│   ├── Has identity (id())
│   ├── Has type (type())
│   └── Has value
│
├── Types
│   ├── Immutable: int, float, bool, str, tuple, None
│   │   └── Cannot be changed after creation
│   │       → reassignment creates a new object
│   └── Mutable: list, dict, set
│       └── Can be changed in place
│           → aliasing: two names → same object
│
├── Type System
│   ├── Dynamically typed: types on objects, not variables
│   └── Strongly typed: no silent conversion between unrelated types
│       except numeric promotion (int → float, bool → int)
│
├── Expressions
│   ├── Evaluate to a value
│   ├── Operator precedence governs evaluation order
│   ├── ** is right-associative
│   └── and/or short-circuit (and return operands, not just bool)
│
└── Conversions
    ├── int(): truncates toward zero
    ├── round(): banker's rounding (to nearest even)
    ├── bool(): falsy = 0/0.0/""/[]/{}/()/None/False
    └── str(): always succeeds; repr() adds quotes for strings
```

---

## Common Mistakes This Week: Know Them Now

**Mistake 1: Using `=` instead of `==`**
```python
if x = 5:    # SyntaxError — intentional Python design!
if x == 5:   # Correct
```

**Mistake 2: Comparing floats with `==`**
```python
if 0.1 + 0.2 == 0.3:   # WRONG — this is False!
import math
if math.isclose(0.1 + 0.2, 0.3):   # Correct
```

**Mistake 3: Thinking `int()` rounds**
```python
int(3.9)    # 3, NOT 4 — truncates toward zero
int(-3.9)   # -3, NOT -4 — truncates toward zero (not toward -∞)
round(3.9)  # 4 — actual rounding
```

**Mistake 4: Aliasing with mutable objects**
```python
a = [1, 2, 3]
b = a          # b and a point to THE SAME LIST
b.append(4)
print(a)       # [1, 2, 3, 4] — a changed!
# Fix:
b = a.copy()   # or b = list(a) or b = a[:]
```

**Mistake 5: Forgetting `input()` returns a string**
```python
n = input("Enter n: ")
n * 2          # "55" not 10 — if user typed 5, n is the string "5"
# Fix:
n = int(input("Enter n: "))
```

**Mistake 6: Modifying a string in place**
```python
s = "hello"
s[0] = "H"     # TypeError! Strings are immutable
# Fix:
s = "H" + s[1:]   # Creates new string
```

---

## Videos Worth Watching

**Conceptual:**
- "Python Names and Values" — Ned Batchelder (PyCon 2015) — https://youtu.be/_AEJHKGk9ns
  *The best 25-minute video on Python's object model ever made. Watch this before the weekend.*

- "Memory Management in Python" — Computerphile — https://youtu.be/F6u5rhUQ6dU
  *Explains reference counting and garbage collection visually.*

**Practical:**
- "Python f-strings are awesome" — Corey Schafer — https://youtu.be/nghuHvKLhJA
  *Comprehensive coverage of f-string formatting.*

- "Floating Point Numbers" — Computerphile — https://youtu.be/PZRI1IfStY0
  *Why 0.1 + 0.2 ≠ 0.3. Essential viewing.*

---

## Preview of Week 2

Week 2 covers **control flow**: conditionals (`if/elif/else`) and loops (`while`, `for`). 

To prepare, think about:
- How would you check if a number is positive, negative, or zero?
- How would you repeat an action 10 times?
- How would you add up all numbers from 1 to 100?

These questions will be trivial after Week 2. For now, try to think about how you might answer them using only what you know — it will make Week 2 click faster.

---

*CS 101 · Week 1 · Reading Guide · © CSE Department*
