# CS 101 · Lecture 5 (Week 1, Lecture 2)
## Expressions, Operators, and Python's Evaluation Model

**Week 1 · Thursday**
*"An expression is a phrase of a programming language that describes a computation and evaluates to a value." — SICP*

---

## 0. The Core Question

How does Python turn `2 + 3 * 4 - len("hello")` into `9`? What are the rules that govern this? And why should you care?

You should care because **every bug involving wrong values comes from a misunderstanding of evaluation.** The programmer intended one computation; Python performed another. Knowing the rules eliminates an entire class of errors.

---

## 1. Expressions vs. Statements: The Precise Distinction

This distinction is fundamental to understanding Python (and most programming languages):

**An expression** is any syntactic construct that **evaluates to a value.**
```python
42                    # Literal expression → 42
2 + 3                 # Arithmetic expression → 5
"hello".upper()       # Method call expression → "HELLO"
x > 0                 # Comparison expression → True or False
x if x > 0 else -x   # Conditional expression → a value
```

**A statement** is a syntactic construct that **performs an action** but does not itself produce a value.
```python
x = 5                 # Assignment statement (action: binds name)
print(x)              # Expression statement (action: side effect)
if x > 0: ...         # Conditional statement
for i in range(10): . # Loop statement
def f(): ...          # Function definition statement
```

**The key rule:** Expressions can appear *inside* statements. Statements cannot appear inside expressions.

```python
x = 2 + 3     # Statement containing an expression (2 + 3) on the right
              # The expression evaluates first, then the statement executes

y = (x = 5)   # SyntaxError in Python — assignment is a statement, not an expression
              # (This is intentional: prevents the classic C bug if (x = 5) instead of if (x == 5))
```

---

## 2. How Python Evaluates Expressions

Python uses a recursive evaluation strategy:

1. **Literals** evaluate to themselves: `42 → 42`, `"hello" → "hello"`
2. **Names** evaluate to their bound value: `x → whatever x currently holds`
3. **Compound expressions** evaluate their parts first, then apply the operator

```python
# Evaluate: 2 + 3 * 4
# Step 1: Is there operator precedence? Yes — * before +
# Step 2: Evaluate 3 * 4 → 12
# Step 3: Evaluate 2 + 12 → 14
```

```python
# Evaluate: len("hello") + 1
# Step 1: Evaluate "hello" → the string object "hello"
# Step 2: Evaluate len("hello") — call len with the string → 5
# Step 3: Evaluate 5 + 1 → 6
```

This recursive decomposition is called **tree-structured evaluation**. The expression `2 + 3 * 4` corresponds to:

```
     +
    / \
   2   *
      / \
     3   4
```

Python evaluates this tree bottom-up: first `3 * 4 = 12`, then `2 + 12 = 14`.

---

## 3. Operator Precedence: The Complete Picture

Python evaluates operators in this order (high precedence = evaluated first):

| Precedence | Operator(s) | Description | Associativity |
|-----------|-------------|-------------|---------------|
| 1 (highest) | `()` | Parentheses (grouping) | N/A |
| 2 | `**` | Exponentiation | **Right to left** |
| 3 | `+x`, `-x`, `~x` | Unary operators | Right to left |
| 4 | `*`, `/`, `//`, `%`, `@` | Multiplication, division | Left to right |
| 5 | `+`, `-` | Addition, subtraction | Left to right |
| 6 | `<<`, `>>` | Bitwise shifts | Left to right |
| 7 | `&` | Bitwise AND | Left to right |
| 8 | `^` | Bitwise XOR | Left to right |
| 9 | `\|` | Bitwise OR | Left to right |
| 10 | `in`, `not in`, `is`, `is not`, `<`, `<=`, `>`, `>=`, `!=`, `==` | Comparisons | Left to right |
| 11 | `not` | Boolean NOT | Right to left |
| 12 | `and` | Boolean AND | Left to right |
| 13 (lowest) | `or` | Boolean OR | Left to right |

### Exponentiation is Right-Associative

```python
2 ** 3 ** 2    # → 2 ** (3 ** 2) → 2 ** 9 → 512
               # NOT (2 ** 3) ** 2 = 8 ** 2 = 64
```

This matches mathematical convention: a^b^c means a^(b^c).

### Chained Comparisons

Python allows comparison chaining — a feature unique among major languages:

```python
# Python:
0 < x < 10         # True if x is between 0 and 10 (exclusive)
                   # Equivalent to: (0 < x) and (x < 10)

1 <= score <= 100  # True if score is in [1, 100]
a == b == c        # True if all three are equal

# In C/Java, you would need:
0 < x && x < 10
```

Chained comparisons are evaluated left-to-right, with each middle value computed only once:

```python
# This is safe — f() is called only once:
a < f() < b

# Which is equivalent to:
temp = f()
a < temp and temp < b
```

---

## 4. Short-Circuit Evaluation: Exploiting Laziness

`and` and `or` do **not** always evaluate both operands. They stop as soon as the result is determined.

### `and` short-circuits on the first falsy value:

```python
False and (1/0)    # → False  (right side never evaluated!)
True and (1/0)     # → ZeroDivisionError (must evaluate right side)
```

More precisely: `x and y` returns `x` if `x` is falsy, otherwise returns `y`.

```python
>>> 0 and "hello"
0              # Returns 0 (falsy), not False
>>> 1 and "hello"
'hello'        # Returns "hello" (the second operand)
>>> "" and 42
''             # Returns "" (falsy)
```

### `or` short-circuits on the first truthy value:

```python
True or (1/0)    # → True  (right side never evaluated!)
False or (1/0)   # → ZeroDivisionError
```

More precisely: `x or y` returns `x` if `x` is truthy, otherwise returns `y`.

```python
>>> 0 or "hello"
'hello'        # Returns "hello" (first truthy value)
>>> 1 or "hello"
1              # Returns 1 (already truthy)
>>> "" or 42
42
```

### Practical patterns using short-circuit evaluation:

```python
# Safe attribute access — if obj is None, .name is never evaluated:
name = obj is not None and obj.name

# Default values:
value = user_input or "default"   # If user_input is falsy, use "default"

# Guard clauses in conditions:
if lst and lst[0] > 0:   # Safe: lst[0] only accessed if lst is non-empty
    print("First element is positive")
```

---

## 5. Bitwise Operators: Working at the Bit Level

These operators work directly on the binary representation of integers.

| Operator | Name | Example (8-bit) | Result |
|---------|------|-----------------|--------|
| `&` | AND | `0b1010 & 0b1100` | `0b1000` (8) |
| `\|` | OR | `0b1010 \| 0b1100` | `0b1110` (14) |
| `^` | XOR | `0b1010 ^ 0b1100` | `0b0110` (6) |
| `~` | NOT (bitwise) | `~0b1010` | `-11` (two's complement) |
| `<<` | Left shift | `0b0001 << 3` | `0b1000` (8) |
| `>>` | Right shift | `0b1000 >> 2` | `0b0010` (2) |

```python
# Binary literals in Python:
a = 0b1010   # 10 in decimal
b = 0b1100   # 12 in decimal

a & b    # → 0b1000 = 8    (AND: 1 where both are 1)
a | b    # → 0b1110 = 14   (OR: 1 where either is 1)
a ^ b    # → 0b0110 = 6    (XOR: 1 where exactly one is 1)
~a       # → -11           (NOT: flip all bits, result in two's complement)
a << 1   # → 0b10100 = 20  (shift left by 1 = multiply by 2)
a >> 1   # → 0b0101 = 5    (shift right by 1 = integer divide by 2)
```

### Why Bitwise Operators Matter in CS

**Checking if n is even:**
```python
n % 2 == 0      # Division-based — correct but slower
n & 1 == 0      # Bitwise AND — faster, checks the lowest bit directly
```

**Setting, clearing, and toggling flags:**
```python
flags = 0b00000000       # All flags off
READABLE   = 0b00000001  # bit 0
WRITABLE   = 0b00000010  # bit 1
EXECUTABLE = 0b00000100  # bit 2

# Set the READABLE flag:
flags |= READABLE        # → 0b00000001

# Set the WRITABLE flag:
flags |= WRITABLE        # → 0b00000011

# Check if READABLE is set:
if flags & READABLE:
    print("File is readable")

# Clear the WRITABLE flag:
flags &= ~WRITABLE       # → 0b00000001

# Toggle the EXECUTABLE flag:
flags ^= EXECUTABLE      # → 0b00000101
```

This pattern (bit flags) is used extensively in operating systems, network protocols, and hardware interfaces. You'll use it in PROG 101 (C), CS 201 (architecture), and CS 202 (OS).

---

## 6. The `in` Operator: Membership Testing

`in` tests whether a value appears in a collection:

```python
"e" in "hello"          # True
"z" in "hello"          # False
3 in [1, 2, 3, 4]       # True
"key" in {"key": 1}     # True — tests dict keys
5 in range(10)          # True — works on ranges too

# not in — the readable negation:
"z" not in "hello"      # True
```

**Performance note:** The time complexity of `in` depends on the data structure:
- `list`: O(n) — scans every element
- `set` / `dict`: O(1) — hash-based lookup
- `str`: O(n×m) — substring search

We will study this deeply in Weeks 7 and 8.

---

## 7. Type Coercion in Expressions

Python is *mostly* not implicit about type conversion. But a few rules exist:

### Numeric promotion:
```python
int + float → float
bool + int  → int     (True=1, False=0)
bool + float → float
```

```python
>>> 1 + 1.0
2.0        # int promoted to float
>>> True + 1
2          # bool promoted to int
>>> True + 1.0
2.0        # bool promoted to float
```

### Everything else is explicit:
```python
"5" + 3     # TypeError — no automatic string-to-int conversion
"5" * 3     # → "555" — string repetition (different operation!)
[1,2] + [3] # → [1, 2, 3] — list concatenation
```

The rule: `+` means different things for different types. The **type determines the operation**, not the other way around.

---

## 8. Conditional Expressions (Ternary Operator)

Python's conditional expression:

```python
value_if_true if condition else value_if_false
```

```python
x = 5
abs_x = x if x >= 0 else -x    # → 5
abs_y = -3 if -3 >= 0 else 3   # → 3

grade = "pass" if score >= 60 else "fail"

# Compare to the if-statement equivalent:
if score >= 60:
    grade = "pass"
else:
    grade = "fail"
```

Conditional expressions are useful for **simple cases**. For complex logic, use a full `if-else` statement — clarity beats cleverness.

---

## 9. Common Expression Errors and How to Debug Them

### `NameError` — using a variable before assigning it:
```python
print(x)    # NameError: name 'x' is not defined
x = 5
```

### `TypeError` — wrong type for an operation:
```python
"5" + 3     # TypeError: can only concatenate str (not "int") to str
len(42)     # TypeError: object of type 'int' has no len()
```

### `ZeroDivisionError`:
```python
10 / 0      # ZeroDivisionError: division by zero
10 // 0     # ZeroDivisionError
10 % 0      # ZeroDivisionError
```

### `OverflowError` (floats only — not ints):
```python
1e308 * 10  # → inf (overflow to infinity — no error in Python)
```

### Debugging strategy for expression errors:
1. Read the error message — it tells you the line and the type of error
2. Break the expression into parts and evaluate each piece
3. Use the REPL to test subexpressions interactively
4. Add `print(type(x))` before the error line if you're unsure of a type

---

## 10. Building Readable Expressions

**The goal:** any engineer on your team should be able to read your expression and immediately understand what it computes.

```python
# Hard to read:
r = ((x*x)+(y*y))**0.5

# Better:
distance = (x**2 + y**2) ** 0.5

# Even better (with a named intermediate):
sum_of_squares = x**2 + y**2
distance = sum_of_squares ** 0.5

# Or use math.hypot (communicates intent):
import math
distance = math.hypot(x, y)
```

**Naming intermediate results** is not wasteful — it is documentation. The Python compiler is smart enough to optimize these away when needed. Clarity for the human reader is almost always more valuable than a slightly shorter expression.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Expression vs. Statement | Expressions produce values; statements perform actions |
| Evaluation model | Recursive, bottom-up tree evaluation |
| Operator precedence | `**` > `*//%` > `+-` > comparisons > `not` > `and` > `or` |
| Right-associativity | `**` chains right-to-left: `2**3**2 = 2**9 = 512` |
| Short-circuit | `and` stops on first falsy; `or` stops on first truthy |
| Bitwise operators | Work on individual bits; essential in systems programming |
| Type coercion | Numeric types promote; other combinations raise TypeError |
| Conditional expr | `value if condition else other` — for simple cases only |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict the printed output, in order, including which function-call messages appear.

```python
def f():
    print("f")
    return True

def g():
    print("g")
    return False

print(g() and f())
print(f() or g())
print(0 or 'x')
print('' and 5)
```

**2. (Explain.)** In Python, `3 & 1 == 1` evaluates to `True`. In C, the same expression evaluates to `1` *for a different structural reason*. Work out how each language parses it, and say which parse Python uses.

**3. (Build.)** Write a single expression using short-circuit evaluation that safely returns the first element of a list `xs`, or the string `"empty"` if the list has no elements — without using `if`, and without ever indexing an empty list.

**4. (Stretch.)** Predict each, then explain the pattern that connects them.

```python
1 << 2 + 3
~5
-8 >> 1
5 ^ 3
```


### Answers

**1.**

```
g
False
f
True
x

```

(The last line is an empty string, so it looks blank.)

`g() and f()` — `g()` returns a falsey value, so `and` **short-circuits**: `f` is never called, and "f" is not printed. `f() or g()` — `f()` is truthy, so `or` short-circuits and `g` is never called.

The other half of the lesson is in the last two lines: `and` and `or` do **not** return `True`/`False`, they return **one of their operands**. `0 or 'x'` is the string `'x'`, and `'' and 5` is the empty string `''`. This is what makes `name = user_input or "anonymous"` a working default-value idiom — and also what makes it a bug when `0` is a legitimate input, since `0` is falsey and gets replaced.

**2.** They parse it **oppositely**.

In Python, all bitwise operators bind **tighter** than all comparisons, so it is `(3 & 1) == 1` → `1 == 1` → `True`.

In C, `==` binds tighter than `&`, so it is `3 & (1 == 1)` → `3 & 1` → `1`. This is one of the most notorious precedence mistakes in C's design — Dennis Ritchie acknowledged it as an error kept for backward compatibility. It is why C code that tests a bit is always written `if ((flags & MASK) != 0)` with the inner parentheses, and why `gcc -Wparentheses` warns when they are missing.

Both languages arrive at a truthy result here, which is exactly what makes the trap dangerous: the difference is invisible in this example and appears the moment the mask has more than one bit. Try `6 & 2 == 2` in each — Python gives `True`, C gives `0`.

**3.**

```python
xs and xs[0] or "empty"
```

…but this is a **trap**, and recognising why is the point of the exercise. If `xs` is `[0]` or `[""]` or `[None]`, then `xs[0]` is falsey, so `or` moves past it and the expression wrongly returns `"empty"`. The `a and b or c` pattern is a pre-2.5 idiom for a conditional and is correct only when `b` can never be falsey.

The correct answer uses a conditional expression (§8), which evaluates exactly one branch and has no such hole:

```python
xs[0] if xs else "empty"
```

Both short-circuit — neither indexes an empty list — but only the second is right for every input.

**4.** `32`, `-6`, `-4`, `6`.

- `1 << 2 + 3` — arithmetic binds tighter than shifts, so this is `1 << 5`, not `(1 << 2) + 3 = 7`. Parenthesise shifts, always.
- `~5 = -6` — `~n` is exactly `-n - 1`, because two's complement defines `-n` as `~n + 1`. Rearranged, `~n = -n - 1`.
- `-8 >> 1 = -4` — Python's `>>` is an **arithmetic** shift: it preserves the sign, so shifting right is floor division by 2 (and floor of `-4.0` is `-4`). It is *not* division truncating toward zero, which differs the moment the result is not exact: `-7 >> 1` is `-4`, while `-7 // 2` is also `-4` but `int(-7/2)` is `-3`.
- `5 ^ 3 = 6` — XOR: `101 ^ 011 = 110`.

The connecting pattern is that Python's integers behave like **infinite-width two's complement**. There is no sign bit to run out of, so `~` and `>>` extend the sign forever and negative numbers have conceptually infinite leading `1`s. This is why `bin(-5)` shows `-0b101` rather than a bit pattern — there is no finite pattern to show.



---

## Reading

- **Guttag, Ch. 2.2** — Branching Programs (includes expression evaluation)
- **Python Docs:** https://docs.python.org/3/reference/expressions.html (bookmark this — the authoritative reference)

---

*CS 101 · Week 1 · Lecture 5 (Thu) · © CSE Department*
