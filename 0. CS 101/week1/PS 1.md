---
assessment: PS 1
course: CS 101
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-05
submitted: 2026-10-09
graded: 2026-10-12
source: "PS 1 Data Types and Expressions.md"
---

# CS 101 · PS 1

## Answer Sheet

**Assessment:** `PS 1 Data Types and Expressions.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Part A — Written Questions (18 points)

**Your answer:**

**A1. Mutable vs immutable.**

A **mutable** object can be changed in place after it is created — its identity stays the same and
operations like `append` change the object itself. A **immutable** object cannot be changed; any
operation that "modifies" it actually builds a **new** object and rebinds the name.

- Mutable example: a `list`, e.g. `[1, 2, 3]`.
- Immutable example: a `str`, e.g. `"hi"` (also `int`, `float`, `bool`, `tuple`).

Predicted output of the code:

```
[1, 2, 3, 4] hi
```

**Why.** `y = x` does not copy the list — it makes `y` point at the **same** list object (`x` and `y`
are aliases). `y.append(4)` mutates that one object in place, so `x` sees `[1, 2, 3, 4]` too. For the
string, `b = b + "!"` does not mutate `"hi"` (strings are immutable); it builds a **new** string
`"hi!"` and rebinds the name `b` to it. The name `a` still refers to the original `"hi"`, which is
unchanged. So the output is `[1, 2, 3, 4] hi`.

**A2. What `and` / `or` return.**

`or` returns the **first truthy** operand, or the last operand if none is truthy. `and` returns the
**first falsy** operand, or the last operand if all are truthy. Neither is forced to return a `bool`.

- **(a)** `0 or "default"` → `"default"` — `0` is falsy, so `or` moves on and returns the truthy `"default"`.
- **(b)** `"result" and None` → `None` — `"result"` is truthy, so `and` returns the second operand `None`.
- **(c)** `[] or "" or 0.0 or "finally"` → `"finally"` — `[]`, `""` and `0.0` are all falsy, so the last operand is returned.
- **(d)** `1 and 2 and 3` → `3` — `1` and `2` are truthy, so `and` returns the last operand `3` (not `True`).

**A3. Why `0.1 + 0.2 == 0.3` is `False`.**

- **(i) Root cause.** `0.1`, `0.2` and `0.3` have no exact finite binary representation, so each is
  stored as the nearest IEEE-754 double (already rounded). Adding the stored `0.1` and `0.2` gives
  `0.30000000000000004`, which is a **different double** from the one nearest `0.3`, so the two are
  not equal.
- **(ii) Correct comparison.** Compare with a tolerance, e.g. `math.isclose(a, b)` (optionally with
  `rel_tol`/`abs_tol`), or `abs(a - b) < 1e-9`.
- **(iii) Where it matters.** Money/financial arithmetic (cents silently accumulating error),
  navigation/GPS, and long scientific simulations where rounding compounds.

_Marks: 18 / 18_

---

### Part B — Python (`ps1.py`) (82 points)

**Your answer:**

The complete program, `ps1.py` (submitted in `0. CS 101/week1/`):

```python
#!/usr/bin/env python3
"""
ps1.py
CS 101 — Problem Set 1: Data, Types, and Expressions
Due Friday 9 October 2026, 17:00

Student: Adebayo Glover

Only Week 0-1 tools are used: expressions, f-strings, slicing, input(),
int()/float() with try/except ValueError, and the conditional expression
`a if condition else b`. No if-statements, loops or def.
"""

# --- B1: Type Inspector -------------------------------------------------------
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
# conditional expression keeps the empty string from crashing on s[0] / s[-1]
print(f"First char: {s[0]!r}" if s else "First char: (none - empty string)")
print(f"Last char:  {s[-1]!r}" if s else "Last char:  (none - empty string)")


# --- B2: Expression Evaluator --------------------------------------------------
print(f"{'2 ** 32':<30} {2 ** 32}")
print(f"{'365 * 24 * 60 * 60':<30} {365 * 24 * 60 * 60}")
leap_2023 = (2023 % 4 == 0 and 2023 % 100 != 0) or 2023 % 400 == 0
print(f"{'2023 leap year':<30} {leap_2023}")
print(f"{'len(str(2 ** 100))':<30} {len(str(2 ** 100))}")
print(f"{'racecar palindrome':<30} {'racecar' == 'racecar'[::-1]}")


# --- B3: Integer Dissector -----------------------------------------------------
n = int(input("Enter a positive integer: "))
print(f"Number:      {n}")
print(f"Binary:      {n:b}")
print(f"Hexadecimal: {n:x}")
print(f"Bits needed: {len(f'{n:b}')}")
# parity via the low bit: & 1 keeps only the ones bit, which is 1 for odd, 0 for even
print(f"Parity:      {'even' if n & 1 == 0 else 'odd'}")
# A power of two has exactly one 1-bit. Subtracting 1 flips that bit to 0 and turns every
# lower bit to 1, so the two numbers share no 1-bit and n & (n - 1) == 0. Guard n > 0 because
# 0 & (0 - 1) == 0 would otherwise report 0 as a power of two.
is_power_of_two = n > 0 and n & (n - 1) == 0
print(f"Power of 2:  {'yes' if is_power_of_two else 'no'}")
print(f"Times 8:     {n << 3}")      # shifting left by 3 multiplies by 2**3 = 8
print(f"Halved:      {n >> 1}")      # shifting right by 1 is floor division by 2


# --- B4: Loan Calculator -------------------------------------------------------
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
    # convert the annual percentage rate to a monthly decimal rate
    monthly_rate = annual_rate / 12 / 100
    n_payments = years * 12
    growth = (1 + monthly_rate) ** n_payments
    monthly_payment = principal * (monthly_rate * growth) / (growth - 1)
    total_paid = monthly_payment * n_payments
    total_interest = total_paid - principal
    print(f"Monthly payment: ${monthly_payment:,.2f}")
    print(f"Total paid:      ${total_paid:,.2f}")
    print(f"Total interest:  ${total_interest:,.2f}")
    print(f"Interest / principal: {total_interest / principal:.2%}")
```

_Marks: 82 / 82_

---

### B1 — Type Inspector (20 points)

**Your answer:**

Reads one string and prints its representation (`!r`), length, type, its `int` and `float` values
(with `try`/`except ValueError`), truthiness, and first/last characters. The empty string is handled
by a **conditional expression** (`... if s else ...`), so `s[0]`/`s[-1]` are never reached when `s`
is empty.

Output for input `42`:

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

Empty-string case (`s = ""`) prints `Truthy: False` and `(none - empty string)` for both characters,
without crashing.

_Marks: 20 / 20_

---

### B2 — Expression Evaluator (15 points)

**Your answer:**

Each line prints the expression text (left-aligned, width 30) beside its value:

| # | Expression | Value |
|---|---|---|
| 1 | `2 ** 32` | `4294967296` |
| 2 | `365 * 24 * 60 * 60` | `31536000` |
| 3 | `(2023 % 4 == 0 and 2023 % 100 != 0) or 2023 % 400 == 0` | `False` |
| 4 | `len(str(2 ** 100))` | `31` |
| 5 | `"racecar" == "racecar"[::-1]` | `True` |

For (3), 2023 is not divisible by 4, so the whole expression is `False`. For (5), `[::-1]` reverses
the string, and `"racecar"` reads the same both ways.

_Marks: 15 / 15_

---

### B3 — Integer Dissector (22 points)

**Your answer:**

Reads a positive integer and prints its decimal, binary (`:b`), hexadecimal (`:x`) forms, the number
of bits (`len` of the binary string), parity via `& 1`, whether it is a power of two, and the two
shifts.

Output for input `42`:

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

**Why `n & (n - 1) == 0` tests a power of two.** A power of two has exactly one bit set. Subtracting
1 clears that bit and sets every bit below it, so `n` and `n - 1` share no set bit and their bitwise
AND is 0. Guard `n > 0`, since `0 & (0 - 1) == 0` would wrongly report 0 as a power of two.
**Parity:** `n & 1` keeps only the lowest bit (1 = odd, 0 = even), so no `%` is needed.
**Shifts:** `n << 3` shifts left by 3, multiplying by `2³ = 8`; `n >> 1` shifts right by 1, which is
floor division by 2.

_Marks: 22 / 22_

---

### B4 — Loan Calculator (25 points)

**Your answer:**

Reads principal, annual rate (%) and years, converts all three inside one `try`; on `ValueError` it
prints the message and computes nothing (`try`/`except`/`else`). Otherwise it uses
`r = annual_rate / 12 / 100` and `n = years * 12`, then
`M = P·r(1+r)ⁿ / ((1+r)ⁿ − 1)`, and prints the monthly payment, total paid, total interest, and the
interest as a percentage of the principal — every dollar figure with `:,.2f`.

Output for `300000`, `6.5`, `30`:

```
Monthly payment: $1,896.20
Total paid:      $682,633.47
Total interest:  $382,633.47
Interest / principal: 127.54%
```

Non-numeric input prints only `Please enter numbers only.` Another check (200000, 5, 15) gives
`$1,581.59`, `$284,685.71`, `$84,685.71`, `42.34%`.

_Marks: 25 / 25_

---

## Grading Summary

_Filled in by the grader._

|             |              |
| ----------- | ------------ |
| **Score**   | 100 / 100    |
| **Percent** | 100%         |
| **Graded**  | 2026-10-12   |

**Feedback:**
Full marks. Part A explains mutation vs rebinding precisely, gives the correct output
`[1, 2, 3, 4] hi`, and separates the two mechanisms; the `and`/`or` operands are all correct (no bare
`True` for `1 and 2 and 3`); and A3 names the binary-representation root cause, `math.isclose` as the
fix, and a concrete domain.

Part B runs cleanly on every example and edge case:

- **B1 (20).** All header fields present, both conversions use `except ValueError` (no bare `except`),
  and the empty string is handled with a conditional expression rather than a crash.
- **B2 (15).** All five expressions exact, including the full century rule in the leap-year test.
- **B3 (22).** Representations, bit count, `& 1` parity, and the power-of-two test with a correct
  comment; shifts documented.
- **B4 (25).** `try`/`except`/`else` correct, payment formula correct (monthly rate properly divided
  by 100), summary figures and `:,.2f` formatting correct.

Note: the answer sheet's "Part B" heading said 76 points, but the rubric's sub-parts (20+15+22+25)
sum to 82; the heading was corrected to 82 so the sheet totals 100.
