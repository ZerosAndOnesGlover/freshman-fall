# CS 101 · Problem Set 1 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** All code below was run; the outputs shown are real.

### Part A (18 points, 6 each)

**A1.** Mutable objects can be changed in place (`list`); immutable objects cannot — any "change"
builds a new object (`str`, `int`, `tuple`). Output: `[1, 2, 3, 4] hi`. `y = x` puts a second name on
the **same** list, and `append` changes that one object, so `x` sees it. `b = b + "!"` builds a new
string and rebinds only `b`; `a` still names `"hi"`.
*2 pts definitions + examples, 2 pts correct output, 2 pts explanation that separates mutation from rebinding.*

**A2.** `or` returns the first truthy operand (else the last); `and` returns the first falsy operand (else the last).
(a) `"default"` (b) `None` (c) `"finally"` — `[]`, `""` and `0.0` are all falsy (d) `3`.
*1.5 pts each. A bare `True` for (d) earns 0 — that is the misconception being tested.*

**A3.** (i) `0.1` and `0.2` have no exact binary representation, so each is stored rounded, and the
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

**B1 (20):** 6 header fields, 4 each int/float attempts with `except ValueError`, 2 truthiness, 4 empty-string-safe first/last.
Deduct 2 for a bare `except:`.

**B2 (15):** 3 pts each; values must be exact.

| # | Expression | Value |
|---|---|---|
| 1 | `2 ** 32` | `4294967296` |
| 2 | `365 * 24 * 60 * 60` | `31536000` |
| 3 | `(2023 % 4 == 0 and 2023 % 100 != 0) or 2023 % 400 == 0` | `False` |
| 4 | `len(str(2 ** 100))` | `31` |
| 5 | `"racecar" == "racecar"[::-1]` | `True` |

#3: a bare `2023 % 4 == 0` earns 0 — the century rules must appear.

**B3 (22):** 6 the three representations, 2 bit count, 3 parity via `& 1` (`% 2` earns 0), 7 power-of-2
with a correct comment, 4 the shifts with comments.

**B4 (25):** 6 `try`/`except`/`else` handling, 11 correct `M` (commonest error: forgetting `/ 100`, which
gives a payment near $150,000), 4 the three summary figures, 4 formatting.

---

*CS 101 · Week 1 · Problem Set 1 · Due Friday 9 October 2026, 17:00 · © CSE Department*
