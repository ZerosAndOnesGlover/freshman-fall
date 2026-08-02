# CS 101 Python Quick Reference
## Week 0: Types, Expressions, and the Basics

*Keep this handy. Update it as you learn new things.*

---

## Types

```python
# Integers
x = 42          # int — arbitrary precision
x = -17
x = 2 ** 100    # Works! No overflow in Python

# Floats
f = 3.14        # float — IEEE 754 double (64-bit)
f = 1.5e-10     # Scientific notation
# WARNING: 0.1 + 0.2 != 0.3 (floating-point imprecision)

# Booleans
b = True
b = False
# Falsy: False, 0, 0.0, "", [], {}, (), None

# Strings
s = "hello"
s = 'hello'     # Single or double quotes — same thing
s = f"x is {x}" # f-string (use these for formatting)
s = f"{3.14:.2f}" # → "3.14" (2 decimal places)

# None
n = None        # Represents absence of value
```

## Type Checking & Conversion

```python
type(x)              # Returns the type: <class 'int'>
isinstance(x, int)   # True if x is an int (or subclass)

int(3.9)      # → 3  (truncates, does NOT round)
int("42")     # → 42
float(42)     # → 42.0
str(42)       # → "42"
bool(0)       # → False
bool("hi")    # → True
```

## Arithmetic Operators

```python
x + y    # Addition
x - y    # Subtraction
x * y    # Multiplication
x / y    # Division      → always returns float
x // y   # Floor division → rounds DOWN (towards -∞)
x % y    # Modulo (remainder)
x ** y   # Exponentiation
-x       # Unary negation

# Useful identity: x == (x // y) * y + (x % y)
```

## Comparison Operators (return bool)

```python
x == y   # Equal (not assignment!)
x != y   # Not equal
x < y    # Less than
x > y    # Greater than
x <= y   # Less than or equal
x >= y   # Greater than or equal
x is y   # Same object (use for None: x is None)
x is not y  # Not same object
```

## Logical Operators

```python
x and y  # True if both True (short-circuits)
x or y   # True if either True (short-circuits)
not x    # Inverts True/False
```

## String Operations

```python
s = "Hello, World!"

len(s)              # 13 — length
s[0]                # 'H' — indexing (0-based)
s[-1]               # '!' — last character
s[0:5]              # 'Hello' — slicing [start:stop] (stop excluded)
s[7:]               # 'World!' — to end
s[:5]               # 'Hello' — from beginning
s + " Hi"           # Concatenation → "Hello, World! Hi"
"ha" * 3            # Repetition → "hahaha"
"World" in s        # True — membership test

s.upper()           # "HELLO, WORLD!"
s.lower()           # "hello, world!"
s.strip()           # Remove leading/trailing whitespace
s.strip("!")        # Remove specific characters from ends
s.split(", ")       # ['Hello', 'World!'] — split into list
s.replace("l","L")  # "HeLLo, WorLd!"
s.startswith("He")  # True
s.endswith("!")     # True
s.find("World")     # 7 — index of first occurrence (-1 if not found)
s.count("l")        # 3 — count occurrences

f"Name: {name}, Score: {score:.2f}"  # f-string formatting
```

## Variables

```python
x = 5          # Assignment
x += 1         # Equivalent to x = x + 1
x -= 1         # x = x - 1
x *= 2         # x = x * 2
x //= 2        # x = x // 2

# Multiple assignment
a, b = 1, 2    # a=1, b=2
a, b = b, a    # Swap a and b (Python does this elegantly)

# Constants (convention — Python doesn't enforce this)
MAX_SIZE = 100
PI = 3.14159
```

## Input / Output

```python
print("Hello")              # Print to stdout
print(x, y, z)              # Print multiple values (space-separated)
print(x, y, sep=", ")       # Custom separator
print(x, end="")            # No newline at end
print(f"x = {x:.2f}")       # Formatted output

s = input("Prompt: ")       # Returns string — always!
n = int(input("Enter n: ")) # Convert to int
f = float(input("Enter f: ")) # Convert to float
```

## Operator Precedence (high → low)

```
()          Parentheses
**          Exponentiation (right-to-left)
+x, -x      Unary operators
*, /, //, % Multiplication/division
+, -        Addition/subtraction
<, <=, >, >= Comparisons
==, !=      Equality
not         Logical NOT
and         Logical AND
or          Logical OR
```

**When in doubt: use parentheses.**

---

## Git Quick Reference

```bash
git init                    # Create new repo
git status                  # See what's changed
git add filename.py         # Stage a file
git add .                   # Stage all changes
git commit -m "message"     # Commit with message
git log --oneline           # View commit history (compact)
git diff                    # See unstaged changes
git diff --staged           # See staged changes

# First time connecting to GitHub:
git remote add origin URL
git branch -M main
git push -u origin main

# After first setup:
git push                    # Push commits to GitHub
git pull                    # Pull changes from GitHub
```

---

## Terminal Quick Reference

```bash
pwd                  # Where am I?
ls                   # What's in this directory?
ls -la               # List all files with details
cd directory         # Go into directory
cd ..                # Go up one level
mkdir name           # Make directory
touch file.py        # Create empty file
cat file.py          # Print file contents
python3 file.py      # Run Python file
python3              # Open REPL (Ctrl+D to exit)
```

---

## Common Mistakes to Avoid

```python
# MISTAKE 1: = vs ==
if x = 5:    # SyntaxError! = is assignment, == is comparison
if x == 5:   # Correct

# MISTAKE 2: Comparing floats with ==
0.1 + 0.2 == 0.3    # False! Use math.isclose() instead

# MISTAKE 3: input() returns a string
n = input("Enter number: ")
n + 1    # TypeError! Must convert: int(input("Enter number: "))

# MISTAKE 4: Mutable default arguments (Week 3+)
def f(lst=[]):   # WRONG — the same list is reused across calls!
    lst.append(1)
    return lst

# MISTAKE 5: Forgetting 0-based indexing
s = "hello"
s[5]    # IndexError! Valid indices are 0–4 (length is 5, last index is 4)
s[-1]   # Correct way to get last character: 'o'
```

---

*CS 101 · Python Quick Reference · Week 0 · © CSE Department*
