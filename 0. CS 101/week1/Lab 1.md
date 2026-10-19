---
assessment: Lab 1
course: CS 101
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-06
submitted: 2026-10-06
graded: 2026-10-09
source: "LAB 1 Type Exploration.md"
---

# CS 101 · Lab 1
## Answer Sheet

**Assessment:** `LAB 1 Type Exploration.md`
**Points available:** 100

Code in this folder: `type_experiments.py`, `precedence_test.py`, `bitwise_explore.py`,
`formatting_challenge.py`, `converter.py`.

---

## Part 1 — Python Tutor: Binding, Immutability, Aliasing (20)

**1.1 Binding vs. copying.**

1. After `y = x`, **two** arrows point at the one list object.
2. `x` changed because `y.append(4)` **mutated that shared object** in place — `x` and `y` are two
   names for the same list, so the change is visible through both.
3. `a` did **not** change because `b = b + 1` builds a **new** `int` (11) and moves only `b`'s arrow;
   `a` still labels `10`.

Output: `x` and `y` are `[1, 2, 3, 4]`, and `x is y` is `True`; `a` is `10`, `b` is `11`, and
`a is b` is `False`.

**1.2 Immutability in action.**

The original string did **not** change. `s.upper()` returns a **new** string (`"HELLO"`) and `s` is
rebound to it; `t` still labels the original `"hello"`. So `print(s)` → `HELLO`, `print(t)` → `hello`,
and `s is t` is `False`. Strings cannot be changed in place.

**1.3 The aliasing trap.**

`b` is `[[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]` — the list literal `[a, a, a]` stored three
**references to the same list**, so the single `append` shows up three times. Mutable objects can be
reached through many names, and mutating one mutates them all.

_Marks: 20 / 20_

---

## Part 2 — Predict, Then Run (30)

### 2.1 Conversions and truthiness — `type_experiments.py`

```
-3
42
2 4 -2
True
True
True
3
```

**Prediction I got wrong:** I expected `round(2.5)` to be `3`. Python's `round` is **half-to-even**
(banker's rounding), so `round(2.5)` is `2` and `round(-2.5)` is `-2`, while `round(3.5)` is `4`.
`int()` instead **truncates toward zero** (`int(-3.9) = -3`). A non-empty string or list (`"False"`,
`"0"`, `[False]`) is truthy whatever it contains, and `True + True + True` is `3` because `bool` is a
subclass of `int`.

### 2.2 Precedence gauntlet — `precedence_test.py`

```
512
-4
False
False
3
42
[]
```

`2 ** 3 ** 2` is `2 ** 9 = 512` (right-associative). `-2 ** 2` is `-(2 ** 2) = -4` because `**` binds
tighter than unary minus. `1 < 2 > 3` is the chained `1 < 2 and 2 > 3` → `False`. `1 and 2 and 3`
returns `3`, and `0 or "" or [] or 42` returns `42` (the operands themselves, not `True`/`False`).
When every operand is falsy, `or` returns the **last** one: `0 or "" or []` → `[]`.

### 2.3 Bitwise operations — `bitwise_explore.py`

```
a = 180 = 10110100      b = 107 = 01101011
a & b  = 00100000 (32)   a | b = 11111111 (255)   a ^ b = 11011111 (223)
~a     = -181            a << 2 = 720             a >> 2 = 45
```

1. `&` compares each bit position and keeps a `1` **only where both** operands have a `1`; otherwise
   the result bit is `0`.
2. `a << 2 = 720` **multiplies by `2² = 4`**; `a >> 2 = 45` **floor-divides by 4**.
3. `~a` is negative because it flips **every** bit of the (conceptually infinitely long) two's-complement
   representation, including the leading zeros of a Python `int`. Flipping all bits computes `-a - 1`,
   so `~180 = -181`.

_Marks: 30 / 30_

---

## Part 3 — f-String Formatting (20) — `formatting_challenge.py`

```python
print(f"{pi:.2f}")                                   # 3.14
print(f"{pi:.4f}")                                   # 3.1416
print(f"{pi:.6f}")                                   # 3.141593
print(f"{pi:.8f}")                                   # 3.14159265
print(f"{large:,.2f}")                               # 1,234,567.89
print(f"{small:.3e}")                                # 1.234e-05
print(f"{score:.1%}")                                # 87.7%
print(f"{255:d} {255:x} {255:b}")                    # 255 ff 11111111
print(f"{'Python':>12}|{'Python':<12}|{'Python':^12}|")
```

Output:

```
3.14
3.1416
3.141593
3.14159265
1,234,567.89
1.234e-05
87.7%
255 ff 11111111
      Python|Python      |   Python   |
```

_Marks: 20 / 20_

---

## Part 4 — Build a Converter (30) — `converter.py`

```python
KM_PER_MILE = 1.609344
KG_PER_POUND = 0.453592

raw = input("Enter a value: ")

try:
    value = float(raw)
except ValueError:
    print(f"{raw!r} is not a number.")
else:
    print(f"{value} km = {value / KM_PER_MILE:.6g} mi")
    print(f"{value} mi = {value * KM_PER_MILE:.6g} km")
    print(f"{value} kg = {value / KG_PER_POUND:.6g} lb")
    print(f"{value} °C = {value * 9 / 5 + 32:.6g} °F")
    print(f"{value} °C = {value + 273.15:.6g} K")
```

Verification tests (using the `:.6g` format spec):

| Input | Output |
|-------|--------|
| `42` | `26.0976 mi`, `67.5924 km`, `92.5942 lb`, `107.6 °F`, `315.15 K` |
| `100` | `212 °F` |
| `-40` | `-40 °F` |
| `0` | `273.15 K` |
| `1` | `2.20462 lb`, `1.60934 km` |
| `abc` | `'abc' is not a number.` |

_Marks: 30 / 30_

---

## Reflection

**Q1.** Changing `y` affected `x` because `y = x` only copied the **reference**, so both names label
one list object; `append` **mutates** that object, and the change is visible through every label.
Changing `b` did not affect `a` because `b = b + 1` builds a **new** `int` and **rebinds** only the
name `b`; `a` keeps labelling the original `10`. **Mutation is visible through every label; rebinding
is visible through one.**

**Q2.** Not a contradiction. `int` widens to `float` with **no loss of meaning or information**, so
Python performs the conversion automatically. `str + int` has **no single sensible meaning** — should
`"5" + 3` concatenate, producing `"53"`, or add numerically, producing `8`? Rather than guess, Python
refuses and raises `TypeError`. `1 + 1.0` is allowed because the numeric interpretation is
unambiguous.

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-09 |

**Feedback:**
Full marks. Part 1 explains mutation vs rebinding correctly (two arrows after `y = x`; the new-`int`
rebind for `b`) and predicts the aliasing trap `[[1,2,3,4]]*3` exactly. All three Part 2 files run and
match the reference, the one wrong prediction (`round(2.5)`) is corrected to half-to-even, and the
bitwise questions are answered correctly (`&` needs both bits; `<<2`/`>>2` are ×4 and ÷4; `~a = -a-1`).
Part 3 matches every format spec, including the `^12` centring. `converter.py` passes all six
verification tests, including the `'abc' is not a number.` path. Both reflections are correct.
