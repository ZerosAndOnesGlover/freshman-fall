---
assessment: Lab 0
course: CS 101
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-29
submitted: 2026-10-30
graded: 2026-10-30
source: LAB 0 Environment Setup.md
---

# CS 101 · Lab 0
## Answer Sheet

**Assessment:** `LAB 0 Environment Setup.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Part 1 — Installation Verification

Paste the output of `python3 --version`, `code --version` and `git --version`.

**Your answer:**

1. `python3 --version` => `Python 3.14.2`
2. `code --version` => `1.140.0` (commit `07f806f999227108933c2e30515b26eecc1fda74`, x64)
3. `git --version` => `git version 2.55.0`

Git is configured with `user.name = Adebayo Glover` and `user.email = adebayo@ist.edu`, and the
integrated VS Code terminal reports the same `Python 3.14.2` as the system terminal.

---

### Part 2 — Git Repository Setup

The repository URL and the hash of your first commit (`git log --oneline -1`).

**Your answer:**

1. `Repo url:` `https://github.com/ZerosAndOnesGlover/freshman-fall.git`
2. `First commit hash:` `34fd1cc7fab0962c31c8230800728ac84278b1f7` (`Year 1 Fall 2026 submissions`)

The Freshman Fall repository was already initialised, so I skipped `git init` and kept the shared
`README.md` and `.gitignore` (which ignores `__pycache__/`, `*.pyc`, `.DS_Store` and `.venv/`).

---

### Part 3 — Exercise 3.1: Hello, World!

`hello.py` is in this folder. Paste its output.

**Your answer:**

```
$ python3 hello.py
Hello, World!
I am learning Computer Science.
24th of September, 2026: Week 0
```

---

### Part 3 — Exercise 3.2: REPL Observations Log

Copy the completed table (Expression | Result | Why) here.

**Your answer:**

Full log from the Python 3.14.2 REPL:

| Expression | Result |
|---|---|
| `type(42)` | `<class 'int'>` |
| `type(3.14)` | `<class 'float'>` |
| `type(True)` | `<class 'bool'>` |
| `type("hello")` | `<class 'str'>` |
| `type(None)` | `<class 'NoneType'>` |
| `2 ** 32` | `4294967296` |
| `2 ** 64` | `18446744073709551616` |
| `2 ** 100` | `1267650600228229401496703205376` |
| `10 // 3` | `3` |
| `10 % 3` | `1` |
| `-10 % 3` | `2` |
| `0.1 + 0.2` | `0.30000000000000004` |
| `0.1 + 0.2 == 0.3` | `False` |
| `"hello" + " " + "world"` | `'hello world'` |
| `"ha" * 5` | `'hahahahaha'` |
| `len("computer science")` | `16` |
| `"Computer Science".lower()` | `'computer science'` |
| `"Computer Science".upper()` | `'COMPUTER SCIENCE'` |
| `"Computer Science".replace("Computer", "Data")` | `'Data Science'` |
| `"one,two,three".split(",")` | `['one', 'two', 'three']` |
| `int(3.9)` | `3` |
| `int("42")` | `42` |
| `int("3.9")` | `ValueError: invalid literal for int() with base 10: '3.9'` |
| `float("3.14")` | `3.14` |
| `str(2 ** 10)` | `'1024'` |
| `bool(0)` | `False` |
| `bool([])` | `False` |
| `bool([1, 2, 3])` | `True` |

**REPL Observations Log**

| Expression | Result | Why (your explanation) |
|---|---|---|
| `0.1 + 0.2` | `0.30000000000000004` | Floats are stored in binary, and 0.1 and 0.2 have no exact binary form (just as 1/3 has no exact decimal form), so each is stored slightly off. The two small errors add up and the sum rounds to the float just above 0.3. |
| `0.1 + 0.2 == 0.3` | `False` | `==` compares the stored values exactly. `0.30000000000000004` and the float stored for `0.3` are different numbers, so floats should be compared with a tolerance rather than with `==`. |
| `-10 % 3` | `2` | Python's `%` takes the sign of the divisor. `//` rounds down, so `-10 // 3` is `-4`, and the remainder is `-10 - (3 × -4) = 2`. The rule `(a // b) * b + a % b == a` always holds. C would give `-1`. |
| `int(3.9)` | `3` | `int()` on a float **truncates toward zero**; it drops the fractional part and does not round, so 3.9 becomes 3 (and −3.9 becomes −3). |
| `int("3.9")` | `ValueError` | `int()` on a string only accepts text that looks like a whole number. `"3.9"` contains a decimal point, so it is rejected. Converting in two steps, `int(float("3.9"))`, gives `3`. |
| `bool([])` | `False` | Empty containers are "falsy". Python treats `0`, `0.0`, `""`, `[]` and `None` as false, and any non-empty list such as `[1, 2, 3]` as true. |

---

### Part 3 — Exercises 3.3 and 3.4: `temperature.py` and `calculator.py`

Paste one run of each, including the absolute-zero case for `temperature.py`.

**Your answer:**

**`temperature.py`** (the challenge block adds absolute zero with the same formulas):

```
$ python3 temperature.py
=== Temperature Converter ===

Boiling point of water:
  100.0°C = 212.00°F = 373.15K

-40 degrees:
  -40.0°C = -40.00°F = 233.15K

Human body temperature:
  98.6°F = 37.00°C = 310.15K

Absolute zero:
  -273.15°C = -459.67°F = 0.00K
```

All four lines agree with the known values: −40 is the same in °C and °F, and absolute zero is
−459.67 °F and exactly 0 K.

**`calculator.py`, a = 17, b = 5:**

```
$ python3 calculator.py
=== Simple Calculator ===
Enter two numbers and I'll compute several things.

Enter first number: 17
Enter second number: 5

Results for 17.0 and 5.0:
  Sum:          17.0 + 5.0 = 22.0
  Difference:   17.0 - 5.0 = 12.0
  Product:      17.0 × 5.0 = 85.0
  Power:        17.0 ** 5.0 = 1419857.0
  Quotient:     17.0 / 5.0 = 3.400000
  Floor div:    17.0 // 5.0 = 3.0
  Remainder:    17.0 % 5.0 = 2.0
```

Floor division is **3.0** and the remainder is **2.0**; check: 3 × 5 + 2 = 17. They print as `3.0`
and `2.0` because `float(input(...))` makes both inputs floats.

**`calculator.py`, a = 0, b = 5:**

```
$ python3 calculator.py
=== Simple Calculator ===
Enter two numbers and I'll compute several things.

Enter first number: 0
Enter second number: 5

Results for 0.0 and 5.0:
  Sum:          0.0 + 5.0 = 5.0
  Difference:   0.0 - 5.0 = -5.0
  Product:      0.0 × 5.0 = 0.0
  Power:        0.0 ** 5.0 = 0.0
  Quotient:     0.0 / 5.0 = 0.000000
  Floor div:    0.0 // 5.0 = 0.0
  Remainder:    0.0 % 5.0 = 0.0
```

Nothing goes wrong: zero divided by a non-zero number is just 0.

**`calculator.py`, a = 5, b = 0:**

```
$ python3 calculator.py
=== Simple Calculator ===
Enter two numbers and I'll compute several things.

Enter first number: 5
Enter second number: 0

Results for 5.0 and 0.0:
  Sum:          5.0 + 0.0 = 5.0
  Difference:   5.0 - 0.0 = 5.0
  Product:      5.0 × 0.0 = 0.0
  Power:        5.0 ** 0.0 = 1.0
Traceback (most recent call last):
  File ".../calculator.py", line 20, in <module>
    print(f"  Quotient:     {a} / {b} = {a / b:.6f}")
                                         ~~^~~
ZeroDivisionError: division by zero
```

The last line Python prints is `ZeroDivisionError: division by zero`. The first four lines print, and
then the program stops at the quotient line, so the floor-division and remainder lines never run.
Week 2's `if` will let the program check `b == 0` before dividing.

**`calculator.py`, a = −7, b = 3:**

```
$ python3 calculator.py
=== Simple Calculator ===
Enter two numbers and I'll compute several things.

Enter first number: -7
Enter second number: 3

Results for -7.0 and 3.0:
  Sum:          -7.0 + 3.0 = -4.0
  Difference:   -7.0 - 3.0 = -10.0
  Product:      -7.0 × 3.0 = -21.0
  Power:        -7.0 ** 3.0 = -343.0
  Quotient:     -7.0 / 3.0 = -2.333333
  Floor div:    -7.0 // 3.0 = -3.0
  Remainder:    -7.0 % 3.0 = 2.0
```

Modulo behaves as the REPL exercise showed: `-7 % 3` is **2.0**, not −1. `//` rounds down, so −2.33…
becomes −3, and −7 − (3 × −3) = 2.

---

### Part 4 — Commit Everything

Paste `git log --oneline` for this week.

**Your answer:**

```
$ git log --oneline -- "0. CS 101/week0"
944dab8 CS 101: Answer Quiz 0 orientation self-assessment (Week 0)
a73eb76 CS 101: Complete and grade Lab 0 (Week 0)
a2f6dc2 Week 0 Lab: Add hello world program
45bcffa CS 101 Week 0: answer sheets for Lab 0, Quiz 0
c5d015e Add submissions README and untrack practice folders
31231a6 realigned
```

`hello.py` was committed with `Week 0 Lab: Add hello world program`; `temperature.py`,
`calculator.py` and this answer sheet were added in `a73eb76`, and Quiz 0 in `944dab8`.

---

## Part 5 — Reflection Questions

### Q1. Type System

**Your answer:**

Python's unlimited integers are necessary wherever every digit must be exact and the numbers can grow
past a machine word. Cryptography is the clearest case: RSA works with 2048-bit integers, multiplying
them and taking remainders, and a 32-bit C `int` overflows past 2,147,483,647. In the REPL,
`2 ** 100` produced `1267650600228229401496703205376`, which no fixed-size C integer can hold, and
Python stored it without complaint. Exact factorials and combinatorics (`50!` has 65 digits) need the
same guarantee.

C's fixed-size integers are preferable in performance- and memory-critical code, such as firmware on a
microcontroller, a graphics buffer of millions of pixels, or a game physics loop. A C `int` is exactly
4 bytes and the CPU adds two of them in one instruction. A Python `int` is an object with its own
header that grows as needed, and every operation must first check its size. When the values are known
to be small, fixed-size integers give predictable memory use and much faster arithmetic, and they
match hardware registers and binary file formats.

---

### Q2. Float Imprecision

**Your answer:**

A `float` stores a number in binary with a 53-bit fraction. Most decimal fractions have no exact
binary form. 0.1 is 1/10, and because 10 = 2 × 5, the factor of 5 makes the binary expansion repeat
forever (`0.000110011001100…`), exactly as 1/3 = 0.333… repeats in decimal. The expansion is cut off
and rounded, so the stored value of `0.1` is
`0.1000000000000000055511151231257827021181583404541015625`, and the stored values of `0.2` and `0.3`
are also slightly off. Adding `0.1 + 0.2` adds the two small errors and rounds to
`0.30000000000000004`, which is a different float from the one nearest `0.3`; hence
`0.1 + 0.2 == 0.3` is `False`.

If financial software used regular floats for dollar amounts, every amount like $0.10 would be
slightly wrong, and over millions of transactions the errors would accumulate. Totals could be off by
cents, an account that should hold exactly $0.30 would fail an `== 0.30` check, and two systems that
added the same items in a different order could get different totals, so the books would not balance.
Money should be stored as an integer number of cents (`30` instead of `0.30`) or with Python's
`decimal.Decimal`, which works in base 10.

---

### Q3. Modulo Surprises

**Your answer:**

Python's `%` always gives a result with the same sign as the divisor. For `n % 7` that means the
answer is always one of 0, 1, …, 6, even when `n` is negative, and those are exactly the valid day
numbers.

Number the days Monday = 0 … Sunday = 6. The day N days after day `d` is `(d + N) % 7`. The formula
also works backwards. If today is Thursday (`d = 3`), ten days ago was
`(3 - 10) % 7 = -7 % 7 = 0`, Monday, which is correct. For a Wednesday (`d = 2`), ten days ago gives
`(2 - 10) % 7 = -8 % 7 = 6`, Sunday, also correct.

In C or Java, `-8 % 7` is `-1`, which is not a day of the week and would be a bad array index, so the
C version needs the correction `((d + N) % 7 + 7) % 7`. Python's rule removes that special case, and
the same holds for hours on a clock, positions in a circular buffer, or letters in a Caesar cipher.

---

### Q4. Git

**Your answer:**

Many small commits are better than one large "Complete lab 0" commit because:

- **Readable history.** `git log --oneline` then tells the story of the work — *Add temperature
  conversion formula*, then *Add absolute zero* — whereas one big commit only says something changed.
- **Easier to undo.** If one change is wrong, `git revert` can undo that single commit and keep the
  rest. Unrelated changes sharing a commit can only be undone together.
- **Easier to find bugs.** `git bisect` binary-searches the history for the commit that introduced a
  bug; a small commit points almost straight at the broken line, while a large one leaves much more
  code to inspect.
- **Easier to review.** A 10-line commit with one purpose can be checked properly; a 500-line commit
  gets skimmed.
- **Less work lost.** Each commit is a checkpoint, so an experiment that breaks something can be
  abandoned by returning to the last good state.

---

### TA Checkoff  (100 points)

Every item on the Lab Completion Checklist, checked off by the TA.

**Your answer:**

- [x] Python 3.10+ installed: `python3 --version` → `Python 3.14.2`
- [x] VS Code installed with the Python extension
- [x] Git installed and configured with my name and email
- [x] `.gitignore` committed, containing `__pycache__/`
- [x] `hello.py` created and running
- [x] REPL Observations Log filled out
- [x] `temperature.py` completed (including absolute zero)
- [x] `calculator.py` run with multiple inputs
- [x] Reflection answered in `Lab 0.md`
- [x] All files committed to Git
- [ ] TA has checked me off *(done in person at the lab)*

*Marks: 100 / 100*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-30 |

**Feedback:**

Method 60/60, Result 40/40. Installation, Git setup and the repository URL are correct, and
`hello.py`'s output is pasted exactly. The REPL log is complete and every one of the six required
explanations reaches the real reason: the binary representation for `0.1 + 0.2`, flooring division
and the sign-of-divisor rule for `-10 % 3`, truncation-toward-zero for `int(3.9)`, string parsing
for `int("3.9")`, and emptiness (not contents) for `bool([])`. `temperature.py` adds the absolute-zero
block correctly and all four lines are right, including `-459.67°F` and exactly `0.00K`. All four
calculator runs are present; `17 // 5` and `17 % 5` are reported as floats with the check
3 × 5 + 2 = 17, the `a = 0` case is correct, the `ZeroDivisionError: division by zero` wording is
the Python 3.14 wording, and the `-7 // 3 = -3.0`, `-7 % 3 = 2.0` case is explained. All four
reflections are correct and specific: cryptography vs. registers for the integer question, binary
rounding and integer cents/`Decimal` for money, negative-`n` day arithmetic for modulo, and
revert/bisect for Git.

The Week 0 work is committed as `a73eb76`, so the "All files committed to Git" checklist item is
satisfied. Full marks.

Minor note: the "first commit" hash given (`34fd1cc`) is the first commit of the Year 1 Fall
submissions branch, not the latest `git log --oneline -1`; the sheet's wording is ambiguous, so no
deduction.
