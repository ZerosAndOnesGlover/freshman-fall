# CS 101 Problem Set 1
## Data, Types, Expressions, and Variables

**Released:** Friday, Week 1
**Due:** Friday, Week 2 at 11:59 PM
**Submission:** Upload `ps1.py` and `PS 1 Data Types and Expressions.md` to the course portal.
**Weight:** Part of the 30% Problem Sets grade (Week 12's is dropped if lowest)

---

## Overview

This problem set covers:
- Python's type system and object model
- Arithmetic and string expressions
- Type conversion and truthiness
- Operator precedence and short-circuit evaluation
- f-string formatting
- Building programs with variables and expressions

**Structure:**
- Part A: Written questions (no Python required) — in `PS 1 Data Types and Expressions.md`
- Part B: Python coding problems — in `ps1.py`
- Part C: Challenge (optional, no grade impact, purely for learning)

---

## Academic Integrity Reminder

You may discuss approaches with classmates. Every word and line of code you submit must be written by you. If you discuss a problem, close the chat, wait 10 minutes, then write your solution from memory. If you can't, you don't understand it yet — and that's what office hours are for.

---

## Part A: Written Questions (`PS 1 Data Types and Expressions.md`)

Answer these in `PS 1 Data Types and Expressions.md`. Aim for precision — these are conceptual questions, not opinion questions.

**A1. (4 points)** Explain the difference between **mutable** and **immutable** objects in Python. Give one example of each, and explain a practical consequence of this difference when passing objects to functions.

**A2. (4 points)** Python's `and` and `or` operators are **short-circuit evaluated** and return one of their operands (not necessarily a boolean). Explain what each of the following evaluates to and why:

```python
(a)  0 or "default"
(b)  "result" and None
(c)  [] or {} or () or "finally"
(d)  1 and 2 and 3
```

**A3. (4 points)** The expression `2 ** 3 ** 2` evaluates to `512`, not `64`. Explain why, and write a different expression using explicit parentheses that evaluates to `64`.

**A4. (4 points)** Explain why `0.1 + 0.2 == 0.3` evaluates to `False` in Python. Your explanation must include:
- The root cause (in 1–2 sentences)
- The correct way to compare floats
- One real-world domain where this difference matters critically

**A5. (4 points)** Python distinguishes `==` (equality) from `is` (identity). Explain the difference. When should you use `is` and when `==`? Give the one common use case where `is` is the *correct* choice.

---

## Part B: Python Coding (`ps1.py`)

Put all code in a single file `ps1.py`. Use the section comments below to organize your work.

### Template for ps1.py:

```python
#!/usr/bin/env python3
"""
ps1.py
CS 101 — Problem Set 1: Data, Types, and Expressions

Student: ____________________________
Date: ______________________________

Honor pledge: I wrote this code myself and understand every line.
"""

# ─── B1: Type Inspector ───────────────────────────────────────────────────────
# [Your B1 code here]

# ─── B2: Expression Evaluator ─────────────────────────────────────────────────
# [Your B2 code here]

# ─── B3: Integer Dissector ────────────────────────────────────────────────────
# [Your B3 code here]

# ─── B4: String Sculptor ──────────────────────────────────────────────────────
# [Your B4 code here]

# ─── B5: Number Formatter ─────────────────────────────────────────────────────
# [Your B5 code here]

# ─── B6: Boolean Logic Table ──────────────────────────────────────────────────
# [Your B6 code here]

# ─── B7: Mortgage Calculator ──────────────────────────────────────────────────
# [Your B7 code here]
```

---

### B1: Type Inspector (10 points)

Write a program that takes user input and prints a detailed analysis of it.

**Requirements:**
- Prompt the user for a string
- Print: the original string, its length, the type
- Attempt to parse it as int, float, and bool — report success or failure for each
- Print the truthiness of the original string
- Print the first and last characters (handle empty string gracefully)

**Example output for input `"42"`:**
```
Input:      '42'
Length:     2
Type:       <class 'str'>

Parsed as int:   42       ✓
Parsed as float: 42.0     ✓
Parsed as bool:  True     (non-empty string)

First char: '4'
Last char:  '2'
```

**Example output for input `"hello"`:**
```
Input:      'hello'
Length:     5
Type:       <class 'str'>

Parsed as int:   ✗ (not a valid integer)
Parsed as float: ✗ (not a valid float)
Parsed as bool:  True     (non-empty string)

First char: 'h'
Last char:  'o'
```

**Hint:** Use `try/except ValueError` to attempt conversions safely.

---

### B2: Expression Evaluator (8 points)

Without using any loops or functions beyond what Week 1 covers, write expressions that compute each value. Print the result and the expression that produced it.

```python
# For each item, your code should print a line like:
# "Expression: 2**10           Result: 1024"
```

Compute and display:
1. 2 raised to the power 32
2. The number of seconds in a year (365 days, 24 hours, 60 minutes, 60 seconds)
3. The remainder when 1,000,000,007 is divided by 997
4. The integer part of the square root of 2 (without importing math — use `** 0.5` and `int()`)
5. Whether 17 is even (a boolean expression)
6. Whether 2023 is a leap year (a year is a leap year if divisible by 4, except centuries, except every 400 years — express this as a single boolean expression)
7. The number of digits in 2^100 (hint: convert to string, check length)
8. `True` if the string `"racecar"` is a palindrome, `False` otherwise (use slicing, one expression)

---

### B3: Integer Dissector (10 points)

Write a program that takes a positive integer from the user and prints:
- Its decimal representation
- Its binary representation (use `bin()` and f-strings)
- Its hexadecimal representation
- Its octal representation
- Whether it is even or odd (using bitwise AND, not modulo)
- Whether it is a power of 2 (hint: `n & (n-1) == 0` — figure out why this works and explain in a comment)
- Its digit sum (sum of its decimal digits)
- How many bits are needed to represent it (hint: `int.bit_length()`)

**Example output for input `42`:**
```
Number:      42
Binary:      0b101010   (6 bits)
Hexadecimal: 0x2a
Octal:       0o52
Parity:      Even
Power of 2:  No
Digit sum:   4 + 2 = 6
Bit length:  6 bits
```

---

### B4: String Sculptor (12 points)

Write a function-free program (just expressions and variable assignments) that, given the string `text` below, computes and prints each transformation.

```python
text = "  The quick brown fox jumps over the lazy dog.  "
```

Compute and print:
1. The string stripped of leading and trailing whitespace
2. The word count (number of words after stripping)
3. The character count (not including leading/trailing spaces)
4. The string reversed
5. The string in UPPER CASE
6. The string in Title Case
7. The string with all vowels (aeiouAEIOU) replaced by `*` — do this without loops, using chained `.replace()` calls
8. Whether the stripped string ends with a period
9. The index of the first occurrence of `"fox"` in the stripped string
10. The stripped string with `"fox"` replaced by `"cat"`
11. The stripped string split into a list of words, then rejoined with `" | "` as separator
12. A formatted line: `"Words: 9 | Characters: 44 | Reversed: .god yzal eht r"` (first 15 chars of reversed)

---

### B5: Number Formatter (8 points)

Write a program that takes a float from the user and prints it in 8 different formats:

```python
# For input 1234567.89:
# 
# Fixed (2dp):        1234567.89
# Fixed (0dp):        1234568
# Scientific (3sig):  1.235e+06
# Engineering:        1.235e+06
# Percentage:         123456789.00%
# With commas:        1,234,567.89
# Binary integer:     N/A (not an integer)
# Padded (width 20):  '          1234567.89'
```

For inputs that are whole numbers (e.g. 255.0), also print binary, hex, and octal.

---

### B6: Boolean Logic Table (8 points)

Without using loops (we haven't covered them yet), write expressions that build and print a truth table for the expression `(A and not B) or (not A and B)` — which is the XOR operation.

Print the complete truth table:
```
A       B       (A and not B) or (not A and B)
True    True    False
True    False   True
False   True    True
False   False   False
```

Then add a column for `A ^ B` (Python's XOR operator) and verify the two columns are always equal.

---

### B7: Mortgage Calculator (16 points)

This is the main programming challenge of PS1.

Write a **mortgage calculator** that takes user input and produces a detailed payment summary.

**Background math:**
Monthly payment formula:
```
M = P × [r(1+r)^n] / [(1+r)^n - 1]
```
Where:
- `P` = principal (loan amount in dollars)
- `r` = monthly interest rate = annual_rate / 12 / 100
- `n` = number of payments = years × 12
- `M` = monthly payment

**Requirements:**

1. Prompt for: principal (dollars), annual interest rate (percent), loan term (years)
2. Validate all inputs — handle non-numeric input with a helpful error message
3. Validate constraints: principal > 0, rate > 0, years > 0
4. Compute and print:
   - Monthly payment
   - Total amount paid over the life of the loan
   - Total interest paid
   - Interest as a percentage of the principal
5. Print a first-year summary (months 1–12): for each month, show payment number, interest portion, principal portion, and remaining balance
6. Format all dollar amounts with commas and 2 decimal places

**Example output for P=300000, rate=6.5%, years=30:**
```
════════════════════════════════════════
         MORTGAGE CALCULATOR
════════════════════════════════════════

Loan Amount:     $300,000.00
Annual Rate:         6.500%
Term:              30 years (360 payments)

Monthly Payment:  $1,896.20
Total Paid:     $682,633.47
Total Interest: $382,633.47
Interest/Principal: 127.54%

────────────────────────────────────────
First Year Payment Schedule
────────────────────────────────────────
Mo  Payment      Interest    Principal   Balance
 1  $1,896.20    $1,625.00   $271.20     $299,728.80
 2  $1,896.20    $1,623.53   $272.67     $299,456.12
 3  $1,896.20    $1,622.05   $274.15     $299,181.97
...
12  $1,896.20    $1,608.40   $287.81     $296,646.82
```

*Note on rounding: the figures above use the unrounded monthly payment throughout. If you instead multiply the rounded payment ($1,896.20 × 360), Total Paid comes to $682,632.00. Either convention is acceptable — state which you used.*

**Hints:**
- Use `math.pow()` or `**` for the exponent
- The natural approach is a loop over the months — but **loops are Week 2**, so they are not available to you yet.
- Instead, either compute the first 12 months explicitly, or derive the balance after $n$ months in closed form:
  - `balance(n) = P × (1+r)^n - M × [(1+r)^n - 1] / r`
  - Interest in month n = `balance(n-1) × r`
  - Principal in month n = `M - interest_in_month_n`
- This is a preview of why loops matter — you'll revisit this in Week 2

---

## Grading Rubric

| Problem | Points | Criteria |
|---------|--------|---------|
| A1–A5 (written) | 20 | Accuracy, completeness, concision |
| B1 Type Inspector | 10 | Handles all cases including edge cases |
| B2 Expressions | 8 | Correct values, clear formatting |
| B3 Integer Dissector | 10 | All fields, correct for all valid inputs |
| B4 String Sculptor | 12 | All 12 transformations correct |
| B5 Number Formatter | 8 | All 8 formats, correct for int and non-int |
| B6 Boolean Table | 8 | Correct truth table, XOR verification |
| B7 Mortgage Calculator | 16 | Input handling, math, formatting, schedule |
| **Total** | **92** | |
| Code style (bonus) | up to 5 | Clear names, comments, consistent formatting |

---

## Part C: Challenge Problems (Ungraded)

These do not affect your grade. They are for students who want to go deeper.

**C1: Integer Square Root**
Implement integer square root (floor of the square root of n) without using `math.sqrt` or `**`. Instead, use the Babylonian method:
- Start with guess = n
- Iterate: guess = (guess + n // guess) // 2
- Stop when guess² ≤ n < (guess+1)²

Why is this method called "Babylonian"? Look it up.

**C2: Floating-Point Analysis**
Using only Python's built-in operations (no `struct` or `ctypes`), extract the sign, exponent, and mantissa from a 64-bit float. Verify: `(-1)^sign × (1 + mantissa/2^52) × 2^(exponent-1023)` equals the original number.

**C3: The Billion-Dollar Question**
The `0.1 + 0.2 != 0.3` problem has real consequences. Research the Patriot missile failure of 1991 and the Ariane 5 rocket explosion of 1996. Both were caused by floating-point errors. Write a 200-word analysis: what went wrong and how could it have been prevented?

**C4: Arbitrary Precision**
Python's `int` is arbitrary precision. Using only Python integers and the `%` operator, implement modular exponentiation: compute `(base ** exponent) % modulus` efficiently. (This is the heart of RSA encryption.) Compare runtime for `pow(2, 10000000, 1000000007)` vs. a naive implementation.

---

## Submission Checklist

- [ ] `ps1.py` — all B sections completed, runs without errors
- [ ] `PS 1 Data Types and Expressions.md` — all A sections answered
- [ ] Code is commented where the logic is non-obvious
- [ ] Variable names are descriptive (`monthly_payment`, not `mp` or `x`)
- [ ] Both files committed to Git and submitted to the course portal

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Point totals follow the Grading Rubric above (92 + up to 5 style bonus).

### ⚠️ Errata — CORRECTED in the student-facing text above

Three printed values were wrong and **have now been fixed in this document**. Recorded here for the change log, and in case students hold an older copy.

| Location | Was (wrong) | Now (correct) | Note |
|---|---|---|---|
| B4 item 12 example | `Characters: 43` | **44** | The stripped string is 44 chars — 43 letters/spaces **plus** the final period. |
| B7 example | `Total Paid: $682,632.00` | **$682,633.47** | `$682,632.00` is `round(M,2) × 360`. Both conventions are defensible; a note making the choice explicit was added to the assignment. Accept either if the student states which they used. |
| B7 example, month 12 | `$1,608.27` / bal `$295,835.69` | **$1,608.40** / **$296,646.82** | The old month-12 balance matched no month of the true schedule. Months 1–3 were already correct (months 2–3 were also off by one cent; now exact). |

If any student worked from the pre-correction copy, accept the old figures for B4 #3 and the B7 totals without deduction.

---

### Part A — Written (20 points)

**A1 (4 pts).** *Mutable* objects can be changed in place after creation; *immutable* objects cannot — any "change" produces a new object.
- Immutable: `int`, `float`, `str`, `bool`, `tuple`, `None`. Mutable: `list`, `dict`, `set`.
- **Practical consequence.** Python passes references by value. Rebinding a parameter never affects the caller, but *mutating* a mutable argument does:

```python
def rebind(x):  x = x + [99]      # caller unaffected — new list bound locally
def mutate(x):  x.append(99)      # caller's list IS modified

a = [1, 2]; rebind(a)   # a == [1, 2]
b = [1, 2]; mutate(b)   # b == [1, 2, 99]
```

*Grading: 1 pt definition of each. 1 pt correct examples. 2 pts for a consequence that correctly distinguishes rebinding from mutation. Award only 1 of those 2 if the student says "lists are passed by reference, ints by value" — that is the common misconception; Python passes references uniformly, and the difference is mutability, not the passing mechanism.*

**A2 (4 pts).** `and`/`or` return an **operand**, not a coerced bool. `or` returns the first truthy operand (else the last); `and` returns the first falsy operand (else the last).

| Expression | Result | Why |
|---|---|---|
| `0 or "default"` | `"default"` | `0` is falsy → return second operand |
| `"result" and None` | `None` | `"result"` truthy → return second operand |
| `[] or {} or () or "finally"` | `"finally"` | all of `[]`, `{}`, `()` falsy → last operand |
| `1 and 2 and 3` | `3` | none falsy → last operand |

*Grading: 1 pt each. Deduct nothing for writing `True`/`False` **only if** the student also names the actual operand; a bare `True` for (d) earns 0 — that is precisely the misconception being tested.*

**A3 (4 pts).** `**` is the only common Python operator that is **right-associative**, so `2 ** 3 ** 2` parses as `2 ** (3 ** 2)` = `2 ** 9` = **512**. To get 64, force left grouping: `(2 ** 3) ** 2` = `8 ** 2` = **64**.

*Grading: 2 pts for naming right-associativity (not merely "precedence" — precedence alone does not explain it, since both operators are `**`). 2 pts for the correct parenthesised expression.*

**A4 (4 pts).**
- **Root cause.** IEEE-754 binary64 stores values as sums of negative powers of two. `0.1` and `0.2` are non-terminating in binary, so each is stored rounded; their sum is `0.30000000000000004`, which is a different double than the nearest double to `0.3`.
- **Correct comparison.** `math.isclose(a, b)` (or `abs(a-b) < tol` with a justified tolerance). For exact decimal arithmetic use `decimal.Decimal` or integer cents.
- **Domain.** Finance (accumulated cent errors), aerospace/guidance (the 1991 Patriot battery's drifting time accumulator), or scientific simulation.

*Grading: 1 pt root cause, 1 pt `isclose`/tolerance, 1 pt for naming Decimal-or-integer as the exact alternative, 1 pt domain. Accept any concrete domain with a real mechanism; reject "computers are imprecise" with no mechanism.*

**A5 (4 pts).** `==` asks *are these values equal* (calls `__eq__`); `is` asks *are these the same object* (compares `id()`). Use `==` for values; use `is` for identity.
- **The correct use case:** comparing against singletons — `if x is None:` (likewise `is True` / `is False` / sentinel objects). This is correct because `None` is a singleton, and because a class may override `__eq__` such that `x == None` is unreliable.
- Caution — CPython caches small integers (−5…256), so identity can surprise:

```python
int("256") is int("256")   # True  — inside the small-int cache
int("257") is int("257")   # False — outside it, two distinct objects
```

  Note the values must be built at **runtime** to show this. Written as plain literals in one code block (`a = 257; b = 257`), the compiler folds them to a single constant and `a is b` is `True`. Either way this is an implementation detail and must never be relied on.

*Grading: 1 pt each definition, 1 pt correct guidance, 1 pt for `is None` specifically. Bonus-worthy (style points) if the student raises the small-int/string-interning caveat.*

---

### Part B — Coding

Reference implementations below are complete and were executed before release. Students may deviate freely in style; grade on behaviour.

**B1 Type Inspector (10 pts).**

```python
s = input("Enter a string: ")
print(f"Input:      {s!r}")
print(f"Length:     {len(s)}")
print(f"Type:       {type(s)}")
print()
try:
    print(f"Parsed as int:   {int(s):<8} ✓")
except ValueError:
    print("Parsed as int:   ✗ (not a valid integer)")
try:
    print(f"Parsed as float: {float(s):<8} ✓")
except ValueError:
    print("Parsed as float: ✗ (not a valid float)")
note = "non-empty string" if s else "empty string"
print(f"Parsed as bool:  {str(bool(s)):<8} ({note})")
print()
if s:
    print(f"First char: {s[0]!r}")
    print(f"Last char:  {s[-1]!r}")
else:
    print("First char: (none — empty string)")
    print("Last char:  (none — empty string)")
```

*Grading: 3 pts prompt + the three header fields. 3 pts all three parse attempts using `try/except ValueError`. 2 pts truthiness. 2 pts first/last char **with** the empty-string guard.*
*Common errors: (a) bare `except:` instead of `except ValueError` — deduct 1, it swallows `KeyboardInterrupt`; (b) `f"{bool(s):<8}"` prints `1`/`0` because `bool` formats numerically under a width spec — `str()` is required, deduct 1; (c) no empty-string guard → `IndexError`, deduct the full 2 pts for that item.*

**B2 Expression Evaluator (8 pts).** 1 pt each; values must match exactly.

| # | Expression | Result |
|---|---|---|
| 1 | `2 ** 32` | `4294967296` |
| 2 | `365 * 24 * 60 * 60` | `31536000` |
| 3 | `1_000_000_007 % 997` | `34` |
| 4 | `int(2 ** 0.5)` | `1` |
| 5 | `17 % 2 == 0` | `False` |
| 6 | `(2023 % 4 == 0 and 2023 % 100 != 0) or 2023 % 400 == 0` | `False` |
| 7 | `len(str(2 ** 100))` | `31` |
| 8 | `"racecar" == "racecar"[::-1]` | `True` |

*Common errors: #4 — students write `2 ** 0.5` and report `1.414…`; the question asks for the **integer part**, so `int()` is required. #6 — a bare `2023 % 4 == 0` earns 0; the century rules must appear even though 2023 exercises neither.*

**B3 Integer Dissector (10 pts).**

```python
n = int(input("Enter a positive integer: "))
print(f"Number:      {n}")
print(f"Binary:      {bin(n)}   ({n.bit_length()} bits)")
print(f"Hexadecimal: {hex(n)}")
print(f"Octal:       {oct(n)}")
print(f"Parity:      {'Even' if n & 1 == 0 else 'Odd'}")
# n & (n-1) clears the lowest set bit. A power of two has exactly one set bit,
# so clearing it yields 0. Guard n > 0 because 0 & -1 == 0 would falsely report Yes.
print(f"Power of 2:  {'Yes' if n > 0 and n & (n - 1) == 0 else 'No'}")
print(f"Digit sum:   {' + '.join(str(n))} = {sum(int(d) for d in str(n))}")
print(f"Bit length:  {n.bit_length()} bits")
```

Verified for `42` → `0b101010`, `0x2a`, `0o52`, Even, not a power of 2, digit sum 6, 6 bits. For `64` → power of 2 = Yes, 7 bits.

*Grading: 1 pt each of the four representations (4). 1 pt parity **via `& 1`** — using `% 2` earns 0, the problem specifies bitwise. 2 pts power-of-2 including a correct written explanation of `n & (n-1)`. 1 pt digit sum. 1 pt bit length.*
*Common error: omitting the `n > 0` guard. Accept without deduction if the prompt restricts to positive input, but note it.*

**B4 String Sculptor (12 pts).** 1 pt each. Against `text = "  The quick brown fox jumps over the lazy dog.  "`:

| # | Result |
|---|---|
| 1 | `'The quick brown fox jumps over the lazy dog.'` |
| 2 | `9` |
| 3 | **`44`** (see errata) |
| 4 | `'.god yzal eht revo spmuj xof nworb kciuq ehT'` |
| 5 | `THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.` |
| 6 | `The Quick Brown Fox Jumps Over The Lazy Dog.` |
| 7 | `Th* q**ck br*wn f*x j*mps *v*r th* l*zy d*g.` |
| 8 | `True` |
| 9 | `16` |
| 10 | `The quick brown cat jumps over the lazy dog.` |
| 11 | `The \| quick \| brown \| fox \| jumps \| over \| the \| lazy \| dog.` |
| 12 | `Words: 9 \| Characters: 44 \| Reversed: .god yzal eht r` |

*Common errors: #3 counting 43 (matches the erratum — accept both). #7 forgetting the five uppercase vowels; here only `T` leads so output is unchanged either way, but the chained-`.replace()` must still show all ten calls to earn the point. #9 answering `17` (1-indexed) — `.find()` is 0-indexed.*

**B5 Number Formatter (8 pts).** For `1234567.89`:

```
Fixed (2dp):        1234567.89
Fixed (0dp):        1234568
Scientific (3sig):  1.235e+06
Percentage:         123456789.00%
With commas:        1,234,567.89
Padded (width 20):  '          1234567.89'
Binary integer:     N/A (not an integer)
```

For a whole-valued float such as `255.0`, additionally `0b11111111`, `0xff`, `0o377`.

*Grading: 1 pt per format (7) + 1 pt for correctly branching on `x == int(x)` to decide whether the integer bases apply.*
*Common error: testing `type(x) is int` instead of `x == int(x)` — `255.0` is a `float` yet is whole-valued, so the type test wrongly prints N/A. Deduct the branching point.*

**B6 Boolean Logic Table (8 pts).**

```
A       B       (A and not B) or (not A and B)   A ^ B   match
True    True    False                           False   True
True    False   True                            True    True
False   True    True                            True    True
False   False   False                           False   True
```

*Grading: 4 pts (1 per row of the expression column), 2 pts for the `A ^ B` column, 2 pts for an explicit equality check per row rather than an eyeball claim.*
*Note: `^` on bools returns a `bool`; on ints it is bitwise. `True ^ True` is `False`, not `0`, because `bool` overrides the result type.*

**B7 Mortgage Calculator (16 pts).** For P=300000, rate=6.5%, years=30 — verified output:

```
Monthly Payment:  $1,896.20
Total Paid:       $682,633.47      (or $682,632.00 using the rounded payment — see errata)
Total Interest:   $382,633.47
Interest/Principal: 127.54%

Mo  Payment      Interest    Principal   Balance
 1  $1,896.20    $1,625.00   $271.20     $299,728.80
 2  $1,896.20    $1,623.53   $272.67     $299,456.12
 3  $1,896.20    $1,622.05   $274.15     $299,181.97
...
12  $1,896.20    $1,608.40   $287.81     $296,646.82
```

Since loops arrive only in Week 2, the intended route is the closed-form balance:

```python
r = annual_rate / 12 / 100
n = years * 12
M = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

def balance(k):                     # balance after k payments
    return P * (1 + r) ** k - M * ((1 + r) ** k - 1) / r

# month m: interest = balance(m-1) * r ; principal = M - interest
```

*Grading: 3 pts input validation (non-numeric **and** the three positivity constraints). 4 pts correct `M` — the single most common failure is using the annual rate directly, or dividing by 12 but not by 100. 3 pts the three summary figures. 4 pts a correct 12-month schedule (award 2 if only the first 3 months are right — that usually indicates hand-computation that then drifted). 2 pts comma + 2dp formatting throughout.*
*Common errors: (a) `r = annual_rate / 12` without `/100` → payment ≈ $150k; (b) recomputing interest from the **original** principal each month, which makes every row identical — this is the diagnostic error for "did not understand amortisation"; (c) accumulating rounded balances month-to-month, which drifts a few cents from the closed form — accept, do not deduct.*

---

### Part C — Challenge (ungraded)

Brief notes only; these carry no marks.
- **C1** Babylonian/Heron's method is Newton–Raphson applied to `f(x) = x² − n`. Integer version converges when `guess*guess <= n < (guess+1)**2`; terminate on non-decreasing guesses to avoid a 2-cycle.
- **C2** Sign = bit 63, exponent = bits 62–52 (bias 1023), mantissa = bits 51–0. Reachable without `struct` via `float.hex()` parsing, or by scaling with `math.frexp`.
- **C3** Patriot: 24-bit fixed-point truncation of a 0.1-second tick accumulating ~0.34 s drift over 100 h. Ariane 5: a 64-bit float horizontal-velocity value converted to 16-bit signed integer overflowed — an unprotected conversion of code reused from Ariane 4, whose flight envelope made the value smaller.
- **C4** `pow(base, exp, mod)` uses square-and-multiply in O(log exp) modular multiplications; the naive `(base ** exp) % mod` first materialises an astronomically large integer.

---

*CS 101 · Week 1 · Problem Set 1 · Due Friday Week 2 · © CSE Department*
