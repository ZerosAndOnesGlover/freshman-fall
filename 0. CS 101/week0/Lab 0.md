---
assessment: Lab 0
course: CS 101
component: Labs
possible: 100
score:
status: submitted
started: 2026-10-01
submitted: 2026-10-01
source: "LAB 0 Environment Setup.md"
---

# CS 101 · Lab 0
## Answer Sheet

**Assessment:** `LAB 0 Environment Setup.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Answer

**Completed:** Parts 1–5, all exercises including the absolute-zero challenge and the calculator
runs. The code and the reflection are in `week0/lab0/`.
**Machine:** Ubuntu 24.04.5 LTS, x86_64

#### Part 1: Installation Verification

| Check | Required | Installed | OK |
|---|---|---|---|
| `python3 --version` | 3.10 or higher | Python 3.14.2 | ✅ |
| `code --version` | any recent version | 1.138.0 (x64) | ✅ |
| Python extension | Microsoft's "Python" | `ms-python.python` (with Pylance and the debugger) | ✅ |
| `git --version` | 2.x | git version 2.55.0 | ✅ |
| `git config user.name` | my full name | Adebayo Glover | ✅ |
| `git config user.email` | university email | adebayo@ist.edu (set for this repository) | ✅ |

`python3 --version` gives the same `Python 3.14.2` in VS Code's integrated terminal
(`` Ctrl+` ``), so VS Code is using the same interpreter as my system terminal.

#### Part 2: Git Repository Setup

The Freshman Fall repository already existed, because PROG 101's Lab 0 created it earlier in the
week. So I skipped `git init` as the handout says, and I did not overwrite the existing README.

- **Repository root:** `"$FALL1"` (`5. Academic Registry/4. Submissions/Year1 Freshman/Fall/`),
  shared by all six courses. CS 101 lives in `"$CS101"` = `"$FALL1/0. CS 101"`.
- **README:** `"$FALL1/README.md"` lists all six courses and how each assessment is submitted.
  `"$CS101/README.md"` gives the CS 101 week-by-week layout.
- **First commit:** `34fd1cc Year 1 Fall 2026 submissions`.
- **GitHub:** remote `origin` → `https://github.com/ZerosAndOnesGlover/freshman-fall.git`, branch
  `main` tracking `origin/main`.

#### Part 3: Python Programs

##### Exercise 3.1: Hello, World! (`lab0/hello.py`)

```
$ python3 hello.py
Hello, World!
My name is Adebayo Glover.
I am beginning my study of Computer Science.
```

##### Exercise 3.2: REPL Type Exploration

I ran every expression in the Python 3.14.2 REPL:

| Expression | Result |
|---|---|
| `type(42)` / `type(3.14)` / `type(True)` | `<class 'int'>` / `<class 'float'>` / `<class 'bool'>` |
| `type("hello")` / `type(None)` | `<class 'str'>` / `<class 'NoneType'>` |
| `2 ** 32` | `4294967296` |
| `2 ** 64` | `18446744073709551616` |
| `2 ** 100` | `1267650600228229401496703205376`: no overflow, Python integers grow as needed |
| `10 // 3` / `10 % 3` | `3` / `1` |
| `-10 % 3` | `2` |
| `0.1 + 0.2` | `0.30000000000000004` |
| `0.1 + 0.2 == 0.3` | `False` |
| `"hello" + " " + "world"` | `'hello world'` |
| `"ha" * 5` | `'hahahahaha'` |
| `len("computer science")` | `16` (the space counts) |
| `.lower()` / `.upper()` | `'computer science'` / `'COMPUTER SCIENCE'` |
| `.replace("Computer", "Data")` | `'Data Science'` |
| `"one,two,three".split(",")` | `['one', 'two', 'three']` |
| `int(3.9)` | `3` |
| `int("42")` | `42` |
| `int("3.9")` | `ValueError: invalid literal for int() with base 10: '3.9'` |
| `float("3.14")` | `3.14` |
| `str(2 ** 10)` | `'1024'` |
| `bool(0)` / `bool([])` / `bool([1, 2, 3])` | `False` / `False` / `True` |

**REPL Observations Log**

| Expression | Result | Why (my explanation) |
|---|---|---|
| `0.1 + 0.2` | `0.30000000000000004` | Floats are stored in binary, and 0.1 and 0.2 have no exact binary form (like 1/3 in decimal), so each is stored slightly off. The two errors add up and the sum rounds to the float just above 0.3. |
| `0.1 + 0.2 == 0.3` | `False` | `==` compares the stored values exactly. `0.30000000000000004` and the float stored for `0.3` are different numbers, so floats should be compared with a tolerance, not `==`. |
| `-10 % 3` | `2` | Python's `%` takes the sign of the divisor. `//` rounds down, so `-10 // 3` is `-4`, and the remainder is `-10 - (3 × -4) = 2`. The rule `(a // b) * b + a % b == a` always holds. C would give `-1`. |
| `int(3.9)` | `3` | `int()` on a float **truncates toward zero**. It drops the fractional part and does not round, so 3.9 becomes 3 (and −3.9 becomes −3). |
| `int("3.9")` | `ValueError` | `int()` on a string only accepts text that looks like a whole number. `"3.9"` has a decimal point, so it is rejected. Converting in two steps, `int(float("3.9"))`, gives `3`. |
| `bool([])` | `False` | Empty containers are "falsy". Python treats `0`, `0.0`, `""`, `[]` and `None` as false, and any non-empty list such as `[1, 2, 3]` as true. |

##### Exercise 3.3: Temperature Converter (`lab0/temperature.py`)

For the challenge I added an absolute-zero block that uses the same formulas:

```python
# CHALLENGE: Add absolute zero (-273.15°C)
celsius = -273.15
fahrenheit = (celsius * 9/5) + 32
kelvin = celsius + 273.15

print(f"\nAbsolute zero:")
print(f"  {celsius}°C = {fahrenheit:.2f}°F = {kelvin:.2f}K")
```

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

All four lines agree with the known values. −40 is the same in °C and °F, and absolute zero is
−459.67 °F and exactly 0 K.

##### Exercise 3.4: Personal Calculator (`lab0/calculator.py`)

**a = 17, b = 5**

```
Results for 17.0 and 5.0:
  Sum:          17.0 + 5.0 = 22.0
  Difference:   17.0 - 5.0 = 12.0
  Product:      17.0 × 5.0 = 85.0
  Power:        17.0 ** 5.0 = 1419857.0
  Quotient:     17.0 / 5.0 = 3.400000
  Floor div:    17.0 // 5.0 = 3.0
  Remainder:    17.0 % 5.0 = 2.0
```

Floor division is **3.0** and the remainder is **2.0**. Check: (17 // 5) × 5 + (17 % 5) = 3 × 5 + 2 =
17. ✅ They are printed as `3.0` and `2.0`, not `3` and `2`, because `float(input(...))` makes both
inputs floats, and `//` and `%` on floats give floats.

**a = 0, b = 5**

```
Results for 0.0 and 5.0:
  Sum:          0.0 + 5.0 = 5.0
  Difference:   0.0 - 5.0 = -5.0
  Product:      0.0 × 5.0 = 0.0
  Power:        0.0 ** 5.0 = 0.0
  Quotient:     0.0 / 5.0 = 0.000000
  Floor div:    0.0 // 5.0 = 0.0
  Remainder:    0.0 % 5.0 = 0.0
```

Nothing goes wrong. Zero divided by a non-zero number is just 0, so every line prints normally.

**a = 5, b = 0**

The first four lines print (`5.0 ** 0.0 = 1.0`), and then the program stops at the quotient line.
The last line Python prints is:

```
ZeroDivisionError: division by zero
```

The traceback points at line 20, `{a / b:.6f}`. Python refuses to divide by zero, even for floats,
and because nothing handles the error the program ends there. The floor division and remainder lines
never run. Once we learn `if` in Week 2, the program can check `b == 0` before dividing.

**a = −7, b = 3**

```
Results for -7.0 and 3.0:
  Sum:          -7.0 + 3.0 = -4.0
  Difference:   -7.0 - 3.0 = -10.0
  Product:      -7.0 × 3.0 = -21.0
  Power:        -7.0 ** 3.0 = -343.0
  Quotient:     -7.0 / 3.0 = -2.333333
  Floor div:    -7.0 // 3.0 = -3.0
  Remainder:    -7.0 % 3.0 = 2.0
```

Modulo behaves the way I expected after the REPL exercise: `-7 % 3` is **2.0**, not −1. `//` rounds
**down** (towards −∞), so −2.33… becomes −3, not −2. The remainder that keeps the identity true is
−7 − (3 × −3) = 2. The result takes the divisor's sign, so with `b = 3` it is always 0, 1 or 2.

#### Part 4: Commit Everything

The lab files are committed in the Freshman Fall repository. `git log --oneline` shows the
commit as `CS 101: Lab 0 environment setup and first programs (Week 0)`.

#### Part 5: Reflection

My answers to the four reflection questions are in `week0/lab0/reflection.md`. In short:

1. **Type system.** Unlimited integers are needed for cryptography (RSA uses 2048-bit numbers).
   Fixed-size integers are better in performance- and memory-critical code like firmware or pixel
   buffers.
2. **Float imprecision.** 0.1 repeats forever in binary, so it is stored rounded, and the rounding
   errors add up. For money that means wrong totals and failed equality checks, so use integer cents
   or `Decimal`.
3. **Modulo.** `(d + N) % 7` always lands in 0–6, even going backwards in time. For example, ten
   days before Thursday is `(3 − 10) % 7 = 0`, Monday.
4. **Git.** Small commits give a readable history and can be reverted one at a time. They also let
   `git bisect` find bugs and make review easier.

#### Lab Completion Checklist

- [x] Python 3.10+ installed: `python3 --version` → Python 3.14.2
- [x] VS Code installed with Python extension
- [x] Git installed and configured with my name and email
- [x] `hello.py` created and running
- [x] REPL Observations Log filled out
- [x] `temperature.py` completed (including absolute zero)
- [x] `calculator.py` run with multiple inputs
- [x] `reflection.md` written
- [x] All files committed to Git
- [ ] TA has checked me off *(done in person at the lab)*

*Marks: ___ / 100*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | ___ / 100 |
| **Percent** | ___ |
| **Graded** | ___ |

**Feedback:**

