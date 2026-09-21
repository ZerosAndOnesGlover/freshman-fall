# CS 101 · Problem Set 1
## Data, Types, Expressions, and Variables

**Released:** Friday 2 October 2026, 10:00 (after L06) · Week 1
**Due:** Friday 9 October 2026, 17:00 · Week 2 — late penalty from 17:01
**Submission:** `ps1.py` (Part B) and your answer sheet (Part A) in `"$CS101/week1"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 3–4 hours

---

## What this problem set uses

Only Weeks 0–1: types (`int`, `float`, `bool`, `str`, `None`), expressions and precedence,
short-circuit `and`/`or`, bitwise operators (L05 §5), the conditional expression `x if c else y`
(L05 §8), `input()` with `int()`/`float()` and the `try`/`except ValueError` idiom (L03 §8, L06 §4),
string indexing and slicing (L04 §5), and f-string format specs (L06 §7).

**Not needed and not expected:** `if` statements, loops, your own functions (`def`), lists beyond
what `.split()` returns, dictionaries. Those arrive in Weeks 2, 3 and 8. Every problem below can be
solved without them.

---

## Academic Integrity Reminder

You may discuss approaches with classmates. Every word and line of code you submit must be written by you.

---

## Part A: Written Questions (24 points)

**A1. (6 points)** Explain the difference between **mutable** and **immutable** objects. Give one
example of each. Then predict the output of this code and explain it using that difference:

```python
x = [1, 2, 3]
y = x
y.append(4)
a = "hi"
b = a
b = b + "!"
print(x, a)
```

**A2. (6 points)** `and` and `or` return one of their operands, not necessarily a `bool`. What does
each expression evaluate to, and why?

```python
(a)  0 or "default"
(b)  "result" and None
(c)  [] or "" or 0.0 or "finally"
(d)  1 and 2 and 3
```

**A3. (6 points)** `2 ** 3 ** 2` evaluates to `512`, not `64`. Explain why, and write the expression
with parentheses that gives `64`.

**A4. (6 points)** Explain why `0.1 + 0.2 == 0.3` is `False`. Give (i) the root cause in one or two
sentences, (ii) the correct way to compare floats, (iii) one domain where it matters.

---

## Part B: Python (`ps1.py`) (76 points)

Put all code in one file, `ps1.py`, with a comment line before each problem (`# --- B1 ---`).

### B1: Type Inspector (18 points)

Read a string with `input()` and print:

- the string (use `!r`), its length, and its type
- its value as an `int`, or `not a valid integer` if `int()` raises `ValueError`
- its value as a `float`, or `not a valid float`
- its truthiness (`bool(s)`)
- its first and last characters — and for an empty string, print `(none - empty string)` instead of
  crashing. Use a conditional expression, not an `if` statement.

**Example for input `42`:**
```
Input:      '42'
Length:     2
Type:       <class 'str'>
As int:     42
As float:   42.0
Truthy:     True
First char: '4'
Last char:  '2'
```

### B2: Expression Evaluator (16 points)

Write one expression for each item, and print the expression text next to its value, lined up with
a width spec (e.g. `f"{'2 ** 32':<30} {2 ** 32}"`).

1. 2 raised to the power 32
2. The number of seconds in a 365-day year
3. The remainder when 1,000,000,007 is divided by 997
4. The integer part of √2, using `** 0.5` and `int()` (no `math`)
5. Whether 17 is even
6. Whether 2023 is a leap year — divisible by 4, except centuries, except every 400 years — as a single boolean expression
7. The number of digits in 2¹⁰⁰ (convert to `str`, take `len`)
8. Whether `"racecar"` is a palindrome, in one expression using slicing

### B3: Integer Dissector (20 points)

Read a positive integer and print:

- the number, its binary form (`:b`) and its hexadecimal form (`:x`)
- how many bits it needs (hint: the length of the binary string)
- `even` or `odd`, **using `& 1`**, not `%`
- whether it is a power of 2, using `n & (n - 1) == 0` — and a comment explaining why that test works
- the number shifted left by 3 and right by 1, and in a comment, what each shift does arithmetically

**Example for input `42`:**
```
Number:      42
Binary:      101010
Hexadecimal: 2a
Bits needed: 6
Parity:      even
Power of 2:  no
Times 8:     336
Halved:      21
```

### B4: Loan Calculator (22 points)

Read a principal (dollars), an annual interest rate (percent) and a term (whole years). The monthly
payment is

```
M = P × r(1 + r)^n / ((1 + r)^n − 1)
```

where `r = annual_rate / 12 / 100` and `n = years × 12`.

1. Convert the three inputs inside one `try` block. If any conversion raises `ValueError`, print
   `Please enter numbers only.` and compute nothing else (use `try` / `except` / `else`, as in L03 §8).
2. Print the monthly payment, the total paid (`M × n`), the total interest, and interest as a
   percentage of the principal (`:.2%`).
3. Print every dollar amount with a thousands separator and 2 decimal places (`:,.2f`).

**Example for 300000, 6.5, 30:**
```
Monthly payment: $1,896.20
Total paid:      $682,633.47
Total interest:  $382,633.47
Interest / principal: 127.54%
```

You may assume the numbers entered are positive.

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1–A4 (written) | 24 |
| B1 Type Inspector | 18 |
| B2 Expressions | 16 |
| B3 Integer Dissector | 20 |
| B4 Loan Calculator | 22 |
| **Total** | **100** |

---

## Submission Checklist

- [ ] `ps1.py` runs without errors on the example inputs
- [ ] Part A answered on the answer sheet
- [ ] Descriptive variable names (`monthly_payment`, not `mp`)
- [ ] Committed and pushed from `"$CS101/week1"`

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** All code below was run; the outputs shown are real.

### Part A (24 points, 6 each)

**A1.** Mutable objects can be changed in place (`list`); immutable objects cannot — any "change"
builds a new object (`str`, `int`, `tuple`). Output: `[1, 2, 3, 4] hi`. `y = x` puts a second name on
the **same** list, and `append` changes that one object, so `x` sees it. `b = b + "!"` builds a new
string and rebinds only `b`; `a` still names `"hi"`.
*2 pts definitions + examples, 2 pts correct output, 2 pts explanation that separates mutation from rebinding.*

**A2.** `or` returns the first truthy operand (else the last); `and` returns the first falsy operand (else the last).
(a) `"default"` (b) `None` (c) `"finally"` — `[]`, `""` and `0.0` are all falsy (d) `3`.
*1.5 pts each. A bare `True` for (d) earns 0 — that is the misconception being tested.*

**A3.** `**` is right-associative: `2 ** (3 ** 2)` = `2 ** 9` = 512. `(2 ** 3) ** 2` = 64.
*3 pts for "right-associative" (precedence alone does not explain it — both operators are `**`), 3 pts for the expression.*

**A4.** (i) `0.1` and `0.2` have no exact binary representation, so each is stored rounded, and the
rounded sum `0.30000000000000004` is a different double from the one nearest `0.3`. (ii) `math.isclose(a, b)`
or `abs(a - b) < tolerance`. (iii) Money, navigation, scientific simulation — any concrete domain with a mechanism.
*2 pts each.*

### Part B

**Reference solution** (run on the example inputs; output as shown in the problem statements):

```python
# --- B1 ---
s = input("Enter a string: ")
print(f"Input:      {s!r}")
print(f"Length:     {len(s)}")
print(f"Type:       {type(s)}")
try:
    print(f"As int:     {int(s)}")
except ValueError:
    print("As int:     not a valid integer")
try:
    print(f"As float:   {float(s)}")
except ValueError:
    print("As float:   not a valid float")
print(f"Truthy:     {bool(s)}")
print(f"First char: {s[0]!r}" if s else "First char: (none - empty string)")
print(f"Last char:  {s[-1]!r}" if s else "Last char:  (none - empty string)")

# --- B3 ---
n = int(input("Enter a positive integer: "))
print(f"Number:      {n}")
print(f"Binary:      {n:b}")
print(f"Hexadecimal: {n:x}")
print(f"Bits needed: {len(f'{n:b}')}")
print(f"Parity:      {'even' if n & 1 == 0 else 'odd'}")
# A power of two has exactly one 1-bit; n - 1 turns that bit off and every bit below it on,
# so n & (n - 1) is 0. Guard n > 0: 0 & -1 is also 0.
print(f"Power of 2:  {'yes' if n > 0 and n & (n - 1) == 0 else 'no'}")
print(f"Times 8:     {n << 3}")     # shifting left by k multiplies by 2**k
print(f"Halved:      {n >> 1}")     # shifting right by 1 is floor division by 2

# --- B4 ---
raw_p = input("Principal: ")
raw_r = input("Annual rate (%): ")
raw_y = input("Years: ")
try:
    principal = float(raw_p)
    annual_rate = float(raw_r)
    years = int(raw_y)
except ValueError:
    print("Please enter numbers only.")
else:
    r = annual_rate / 12 / 100
    n = years * 12
    monthly = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    total = monthly * n
    print(f"Monthly payment: ${monthly:,.2f}")
    print(f"Total paid:      ${total:,.2f}")
    print(f"Total interest:  ${total - principal:,.2f}")
    print(f"Interest / principal: {(total - principal) / principal:.2%}")
```

Further verified cases: B1 with empty input prints `Truthy: False` and both `(none - empty string)`
lines. B3 with `64` → `1000000`, `40`, 7 bits, power of 2 `yes`; with `1` → power of 2 `yes`, halved `0`.
B4 with 200000, 5, 15 → `$1,581.59`, `$284,685.71`, `$84,685.71`, `42.34%`; non-numeric input prints
the message only. Accepting `$682,632.00` for the total (rounded payment × 360) is fine if stated.

**B1 (18):** 4 header fields, 4 each int/float attempts with `except ValueError`, 2 truthiness, 4 empty-string-safe first/last.
Deduct 2 for a bare `except:`.

**B2 (16):** 2 pts each; values must be exact.

| # | Expression | Value |
|---|---|---|
| 1 | `2 ** 32` | `4294967296` |
| 2 | `365 * 24 * 60 * 60` | `31536000` |
| 3 | `1_000_000_007 % 997` | `34` |
| 4 | `int(2 ** 0.5)` | `1` |
| 5 | `17 % 2 == 0` | `False` |
| 6 | `(2023 % 4 == 0 and 2023 % 100 != 0) or 2023 % 400 == 0` | `False` |
| 7 | `len(str(2 ** 100))` | `31` |
| 8 | `"racecar" == "racecar"[::-1]` | `True` |

#6: a bare `2023 % 4 == 0` earns 0 — the century rules must appear.

**B3 (20):** 6 the three representations, 2 bit count, 3 parity via `& 1` (`% 2` earns 0), 5 power-of-2
with a correct comment, 4 the shifts with comments.

**B4 (22):** 6 `try`/`except`/`else` handling, 8 correct `M` (commonest error: forgetting `/ 100`, which
gives a payment near $150,000), 4 the three summary figures, 4 formatting.

---

*CS 101 · Week 1 · Problem Set 1 · Due Friday 9 October 2026, 17:00 · © CSE Department*
