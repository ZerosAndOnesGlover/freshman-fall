# CS 101 · Problem Set 3
## Functions, Scope, and the Call Stack

**Released:** Friday 16 October 2026, 10:00 (after L12) · Week 3
**Due:** Friday 23 October 2026, 17:00 · Week 4 — late penalty from 17:01
**Submission:** `ps3.py` (Part B) and your answer sheet (Part A) in `"$CS101/week3"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 3 hours

*(Revised 2026-09-26: cut from about four hours to three. The docstring-only question (A3), the
recursion preview (B5 — recursion is Week 4), `smooth_step`, `is_palindrome_phrase` and `compose` were
removed, and the answer key moved out of this handout.)*

---

## What this problem set uses

Weeks 0–3: everything in PS 1–2, plus `def`, parameters and return values, docstrings and `assert`
preconditions (L10), scope and LEGB, the call stack, default parameters, `nonlocal`, `lambda`
(L11), decomposition, pure functions, and the recursion preview's three-step method (L12 §5–6).

**Not needed and not expected:** dictionaries (Week 8), `raise` (Week 10 — use `assert` for
preconditions), recursion on lists (Week 4).

---

## Part A: Written (34 points)

### A1: Call Stack Trace (12 points)

```python
def multiply(a, b):
    return a * b

def power_sum(base, exp, n):
    total = 0
    for i in range(1, n + 1):
        total += multiply(base ** i, exp)
    return total

def run():
    result = power_sum(2, 3, 4)
    return result

answer = run()
```

**(a)** Draw the call stack, with each frame's variables, while the **first** call to `multiply` runs.
**(b)** How many calls to `multiply` are made in total?
**(c)** When `power_sum` returns, what happens to its frame and its local variables?
**(d)** What is `answer`? Show the working.

### A2: Scope (14 points)

Predict each output **without running it**, and explain with the LEGB rule.

**(a)**
```python
x = 1
def f():
    x = 2
    def g():
        x = 3
        print(x)
    g()
    print(x)
f()
print(x)
```

**(b)**
```python
x = 10
def f():
    print(x)
    x = 20
f()
```

**(c)**
```python
result = []
def add_square(n):
    result.append(n ** 2)
add_square(3)
add_square(4)
print(result)
```

**(d)**
```python
def make_adder(n):
    def adder(x):
        return x + n
    return adder

add5 = make_adder(5)
add10 = make_adder(10)
print(add5(3))
print(add10(3))
print(add5(add10(1)))
```

### A3: Critique (8 points)

List three specific problems with this function (L11 §6 and L12 §2–3 will help) and write a corrected version.

```python
def do_stuff(x, y=[], z=0):
    print("computing...")
    y.append(x)
    total = 0
    for item in y:
        total = total + item + z
        print(item)
    return total, y
```

---

## Part B: Python (`ps3.py`) (66 points)

Every function needs a docstring and at least two `assert` tests written below it. No `print`
inside functions except `print_report`.

### B1: Math Library (16 points)

Pure functions only.

**(a)** `clamp(value, lo, hi)` — restrict `value` to `[lo, hi]`; `assert lo <= hi` as a precondition.
`clamp(5, 0, 10)` → `5`, `clamp(-3, 0, 10)` → `0`, `clamp(15, 0, 10)` → `10`.

**(b)** `lerp(a, b, t)` — linear interpolation `a + (b - a) * t`; precondition `0 <= t <= 1`.
`lerp(0, 10, 0.5)` → `5.0`.

**(c)** `normalize(value, src_min, src_max, dst_min=0.0, dst_max=1.0)` — rescale from one range to
another **by calling `lerp`**. `normalize(75, 0, 100)` → `0.75`; `normalize(75, 0, 100, 0, 10)` → `7.5`.


### B2: Strings (14 points)

**(a)** `title_case(text)` — without `.title()`: split, rebuild each word as its first letter upper
case plus the rest lower case, join. `"the quick brown FOX"` → `"The Quick Brown Fox"`.

**(b)** `count_substring(text, sub)` — count **non-overlapping** occurrences with a `while` loop and
slicing, without `.count()`. `("ababab", "ab")` → `3`; `("aaa", "aa")` → `1`.

### B3: Functions as Values (12 points)

**(a)** `apply_to_all(func, lst)` — a new list of `func(x)` for each `x`.
`apply_to_all(str.upper, ["hello", "world"])` → `["HELLO", "WORLD"]`.

**(b)** `keep_if(predicate, lst)` — a new list of the `x` with `predicate(x)` true.
`keep_if(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])` → `[2, 4, 6]`.

### B4: Decomposition — Grade Report (24 points)

```python
assignments = [
    ("Problem Set 1", 87, 100, 0.30),
    ("Problem Set 2", 92, 100, 0.30),
    ("Midterm", 78, 100, 0.25),
    ("Lab Average", 95, 100, 0.10),
    ("Participation", 100, 100, 0.05),
]
```

Write these, each calling the one before where it can:

1. `percentage(score, max_score)` — the score as a percentage
2. `contribution(score, max_score, weight)` — percentage × weight
3. `weighted_average(assignments)` — the sum of the contributions (unpack each tuple in the `for`, as with `zip` in L09)
4. `letter_grade(pct)` — A ≥ 93, A- ≥ 90, B+ ≥ 87, B ≥ 83, B- ≥ 80, C+ ≥ 77, C ≥ 73, C- ≥ 70, D ≥ 60, else F
5. `print_report(assignments)` — prints:

```
  Assignment         Score   Max  Weight  Contrib
  Problem Set 1         87   100   30.0%   26.10%
  Problem Set 2         92   100   30.0%   27.60%
  Midterm               78   100   25.0%   19.50%
  Lab Average           95   100   10.0%    9.50%
  Participation        100   100    5.0%    5.00%
  Weighted average: 87.70%   Letter grade: B+
```

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Call stack | 12 |
| A2 Scope | 14 |
| A3 Critique | 8 |
| B1 Math library | 16 |
| B2 Strings | 14 |
| B3 Functions as values | 12 |
| B4 Grade report | 24 |
| **Total** | **100** |

---

*CS 101 · Week 3 · Problem Set 3 · Due Friday 23 October 2026, 17:00 · © CSE Department*
