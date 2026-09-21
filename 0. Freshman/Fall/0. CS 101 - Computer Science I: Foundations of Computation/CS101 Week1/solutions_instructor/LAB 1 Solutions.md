# CS 101 · Week 1
## LAB 1 Solutions: INSTRUCTOR ONLY

> Lab sat Tuesday 6 October 2026. **All code below was executed and all stated outputs are real.**

---

## Part 1 — Python Tutor: Binding, Immutability, Aliasing (20)

One point in three forms: **names are labels on objects; assignment rebinds a label; mutation
changes an object.**

- **1.1** Two arrows point at one list. `append` mutates that list, so `x` sees `[1, 2, 3, 4]` and
  `x is y` is `True`. `b = b + 1` builds a new `int` and moves only `b`'s arrow: `a` is `10`, `b` is
  `11`, `a is b` is `False`.
- **1.2** `s.upper()` builds a new string and `s` is rebound to it; `t` still labels `"hello"`.
  `s is t` is `False`. Strings cannot change in place.
- **1.3** `b` is `[[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]` — three references to one list.

**Sentence to extract at checkoff:** *mutation is visible through every label; rebinding is visible
through one.* Award the 20 points for a diagram plus that idea in the student's own words.

---

## Part 2 — Predict, Then Run (30)

### 2.1 Conversions and truthiness

```
int(3.9) = 3        int(-3.9) = -3      int(True) = 1      int("  42  ") = 42
round(2.5), round(3.5), round(-2.5)          ->  2 4 -2
math.floor(-2.5), math.ceil(-2.5), int(-2.5) ->  -3 -2 -2
bool("False") True   bool("0") True   bool([False]) True   bool(0.0000001) True
bool("") False       bool(None) False
isinstance(True, int) True   isinstance(42, bool) False   True == 1 True   True+True+True 3
```

`int()` truncates toward zero; `floor` goes toward −∞. `round` is half-to-even (2.5 → 2, 3.5 → 4) —
the most surprising row; spend a minute on it. A non-empty string or list is truthy whatever it contains.

### 2.2 Precedence

```
14   512   -4   4   True   False   False   False   3   0   42   []
```

`-2 ** 2` is `-(2 ** 2)`: `**` binds tighter than unary minus. `1 < 2 > 3` is `1 < 2 and 2 > 3`.
`0 or "" or []` returns the last operand, `[]`, not `False`.

### 2.3 Bitwise

```
a = 180 = 10110100      b = 107 = 01101011
a & b  = 00100000 (32)  a | b = 11111111 (255)  a ^ b = 11011111 (223)
~a = -181               a << 2 = 720             a >> 2 = 45
```

`&` keeps a 1 only where both bits are 1. `<< 2` multiplies by 4; `>> 2` floor-divides by 4.
`~a` flips every bit, including the infinitely many leading zeros of a Python `int`, which reads as
`-a - 1` in two's complement.

Award 10 per file: runs, and every wrong prediction has a one-sentence explanation.

---

## Part 3 — f-String Formatting (20)

```python
print(f"{pi:.2f}")          # 3.14
print(f"{pi:.4f}")          # 3.1416
print(f"{pi:.6f}")          # 3.141593
print(f"{pi:.8f}")          # 3.14159265
print(f"{large:,.2f}")      # 1,234,567.89
print(f"{small:.3e}")       # 1.234e-05
print(f"{score:.1%}")       # 87.7%
print(f"{255:d} {255:x} {255:b}")   # 255 ff 11111111
print(f"{'Python':>12}|{'Python':<12}|{'Python':^12}|")
#       Python|Python      |   Python   |
```

2 points per line (10 lines).

---

## Part 4 — Converter (30)

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

Verified output: `42` → `26.0976 mi`, `67.5924 km`, `92.5942 lb`, `107.6 °F`, `315.15 K`;
`100` → `212 °F`; `-40` → `-40 °F`; `0` → `273.15 K`; `1` → `2.20462 lb`, `1.60934 km`;
`abc` → `'abc' is not a number.`

5 points per verification test (6 tests). Common error: `value * KG_PER_POUND` (kg → lb needs a divide).

---

## Reflection (required for checkoff, not scored)

- **Q1** Mutation vs rebinding — see Part 1.
- **Q2** No contradiction: `int` → `float` loses no meaning, so Python widens it; `str` + `int` has no
  single sensible meaning (concatenate? add?), so Python refuses rather than guess.
- **Q3** `x != 0 and 10 / x > 1` — the division never runs when `x` is `0`. Or
  `s and s[0] == "#"`, safe on the empty string.

---

*CS 101 · Week 1 · Lab 1 Solutions · Instructor only*
