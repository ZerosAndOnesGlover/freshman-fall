# CS 101 · Problem Set 1
## Data, Types, Expressions, and Variables

**Released:** Friday 2 October 2026, 10:00 (after L06) · Week 1
**Due:** Friday 9 October 2026, 17:00 · Week 2 — late penalty from 17:01
**Submission:** `ps1.py` (Part B) and your answer sheet (Part A) in `"$CS101/week1"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 3 hours

*(Revised 2026-09-26: cut to about three hours — written question A3 and three of the eight B2
expressions were removed, and the answer key moved out of this handout.)*

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

## Part A: Written Questions (18 points)

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

**A3. (6 points)** Explain why `0.1 + 0.2 == 0.3` is `False`. Give (i) the root cause in one or two
sentences, (ii) the correct way to compare floats, (iii) one domain where it matters.

---

## Part B: Python (`ps1.py`) (76 points)

Put all code in one file, `ps1.py`, with a comment line before each problem (`# --- B1 ---`).

### B1: Type Inspector (20 points)

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

### B2: Expression Evaluator (15 points)

Write one expression for each item, and print the expression text next to its value, lined up with
a width spec (e.g. `f"{'2 ** 32':<30} {2 ** 32}"`).

1. 2 raised to the power 32
2. The number of seconds in a 365-day year
3. Whether 2023 is a leap year — divisible by 4, except centuries, except every 400 years — as a single boolean expression
4. The number of digits in 2¹⁰⁰ (convert to `str`, take `len`)
5. Whether `"racecar"` is a palindrome, in one expression using slicing

### B3: Integer Dissector (22 points)

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

### B4: Loan Calculator (25 points)

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
| A1–A3 (written) | 18 |
| B1 Type Inspector | 20 |
| B2 Expressions | 15 |
| B3 Integer Dissector | 22 |
| B4 Loan Calculator | 25 |
| **Total** | **100** |

---

## Submission Checklist

- [ ] `ps1.py` runs without errors on the example inputs
- [ ] Part A answered on the answer sheet
- [ ] Descriptive variable names (`monthly_payment`, not `mp`)
- [ ] Committed and pushed from `"$CS101/week1"`

---

*CS 101 · Week 1 · Problem Set 1 · Due Friday 9 October 2026, 17:00 · © CSE Department*
