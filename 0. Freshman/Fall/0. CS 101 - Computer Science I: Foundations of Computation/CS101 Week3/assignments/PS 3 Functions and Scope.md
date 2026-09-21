# CS 101 · Problem Set 3
## Functions, Scope, and the Call Stack

**Released:** Friday 16 October 2026, 10:00 (after L12) · Week 3
**Due:** Friday 23 October 2026, 17:00 · Week 4 — late penalty from 17:01
**Submission:** `ps3.py` (Part B) and your answer sheet (Part A) in `"$CS101/week3"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 4 hours

---

## What this problem set uses

Weeks 0–3: everything in PS 1–2, plus `def`, parameters and return values, docstrings and `assert`
preconditions (L10), scope and LEGB, the call stack, default parameters, `nonlocal`, `lambda`
(L11), decomposition, pure functions, and the recursion preview's three-step method (L12 §5–6).

**Not needed and not expected:** dictionaries (Week 8), `raise` (Week 10 — use `assert` for
preconditions), recursion on lists (Week 4).

---

## Part A: Written (36 points)

### A1: Call Stack Trace (10 points)

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

### A2: Scope (12 points)

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

### A3: Specifications (8 points)

Write a complete docstring — what it does, parameters and types, return value, preconditions, and
two examples — for each. Do not implement them.

**(a)** `insert_position(lst, target)`: given a list sorted in ascending order, return the index at
which `target` could be inserted to keep it sorted (`[1, 3, 5, 7]`, `4` → `2`; `9` → `4`).

**(b)** `run_length_decode(encoded)`: `"3a2b1c"` → `"aaabbc"`.

### A4: Critique (6 points)

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

## Part B: Python (`ps3.py`) (64 points)

Every function needs a docstring and at least two `assert` tests written below it. No `print`
inside functions except `print_report`.

### B1: Math Library (14 points)

Pure functions only.

**(a)** `clamp(value, lo, hi)` — restrict `value` to `[lo, hi]`; `assert lo <= hi` as a precondition.
`clamp(5, 0, 10)` → `5`, `clamp(-3, 0, 10)` → `0`, `clamp(15, 0, 10)` → `10`.

**(b)** `lerp(a, b, t)` — linear interpolation `a + (b - a) * t`; precondition `0 <= t <= 1`.
`lerp(0, 10, 0.5)` → `5.0`.

**(c)** `normalize(value, src_min, src_max, dst_min=0.0, dst_max=1.0)` — rescale from one range to
another **by calling `lerp`**. `normalize(75, 0, 100)` → `0.75`; `normalize(75, 0, 100, 0, 10)` → `7.5`.

**(d)** `smooth_step(t)` — `3t² − 2t³` for `t` in `[0, 1]`. Check `0.0 → 0.0`, `0.5 → 0.5`, `1.0 → 1.0`.

### B2: Strings (12 points)

**(a)** `title_case(text)` — without `.title()`: split, rebuild each word as its first letter upper
case plus the rest lower case, join. `"the quick brown FOX"` → `"The Quick Brown Fox"`.

**(b)** `count_substring(text, sub)` — count **non-overlapping** occurrences with a `while` loop and
slicing, without `.count()`. `("ababab", "ab")` → `3`; `("aaa", "aa")` → `1`.

**(c)** `is_palindrome_phrase(text)` — ignore case and spaces. `"Never odd or even"` → `True`.

### B3: Functions as Values (12 points)

**(a)** `apply_to_all(func, lst)` — a new list of `func(x)` for each `x`.
`apply_to_all(str.upper, ["hello", "world"])` → `["HELLO", "WORLD"]`.

**(b)** `keep_if(predicate, lst)` — a new list of the `x` with `predicate(x)` true.
`keep_if(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])` → `[2, 4, 6]`.

**(c)** `compose(f, g)` — return a function computing `f(g(x))`.
`compose(lambda x: x ** 2, lambda x: x * 2)(3)` → `36`. What does `compose(g, f)(3)` give, and why is it different?

### B4: Decomposition — Grade Report (16 points)

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

### B5: Recursion Preview (10 points)

Using L12's three-step method (base case, recursive case, trust the call), write recursively, with
the base case and the recursive step each explained in a comment:

**(a)** `power(base, exp)` for `exp >= 0`: `power(2, 10)` → `1024`, `power(3, 0)` → `1`.
**(b)** `gcd(a, b)` by Euclid's rule `gcd(a, b) = gcd(b, a % b)`, `gcd(a, 0) = a`: `gcd(48, 18)` → `6`.

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Call stack | 10 |
| A2 Scope | 12 |
| A3 Specifications | 8 |
| A4 Critique | 6 |
| B1 Math library | 14 |
| B2 Strings | 12 |
| B3 Functions as values | 12 |
| B4 Grade report | 16 |
| B5 Recursion preview | 10 |
| **Total** | **100** |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps3.py` below was run: every `assert` passes and
> the report prints exactly as shown in B4.

### A1 (10)

(a) Top to bottom: `multiply` {a=2, b=3} · `power_sum` {base=2, exp=3, n=4, total=0, i=1} · `run` {} ·
module {multiply, power_sum, run}. *(4)*
(b) **4** calls. *(2)* (c) The frame is popped; `total`, `i` and the parameters are gone. Only the
returned **value** survives, bound to `result` in `run`'s frame. *(2)*
(d) 2·3 + 4·3 + 8·3 + 16·3 = 6 + 12 + 24 + 48 = **90**. *(2)*

### A2 (12, 3 each)

(a) `3`, `2`, `1` — each `x =` creates a new local in its own function. (b) `UnboundLocalError`:
the assignment makes `x` local to `f` for the **whole** body, so `print(x)` reads an unassigned
local. (c) `[9, 16]` — `append` mutates the global list; it does not rebind the name, so no
`global` is needed. (d) `8`, `13`, `16`. `add5` is the inner function `adder`, closing over `n = 5`
from `make_adder`'s enclosing scope (L11 on closures).

### A3 (8, 4 each)

Needs all five elements. (a) Precondition: `lst` sorted ascending. Returns an int in
`0..len(lst)`; for equal elements either side is acceptable if stated. (b) Precondition: well-formed
pairs of a positive count and one character; returns a `str`.

### A4 (6)

Any three of: mutable default `y=[]` is shared between calls (L11 §6); prints inside a computing
function (side effect, L12 §3); does two jobs (L12 §2); `z` is added once **per item** — probably
not intended; meaningless names; returns the caller's mutated list. Fix:

```python
def total_with_offset(values, offset=0):
    """Return the sum of values plus offset once."""
    total = 0
    for v in values:
        total += v
    return total + offset
```

### Part B — reference `ps3.py`

```python
# --- B1 ---
def clamp(value, lo, hi):
    """Return value restricted to the interval [lo, hi]. Requires lo <= hi."""
    assert lo <= hi, "lo must not exceed hi"
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value

def lerp(a, b, t):
    """Return the point a fraction t of the way from a to b. Requires 0 <= t <= 1."""
    assert 0 <= t <= 1, "t must be in [0, 1]"
    return a + (b - a) * t

def normalize(value, src_min, src_max, dst_min=0.0, dst_max=1.0):
    """Rescale value from [src_min, src_max] to [dst_min, dst_max], using lerp."""
    t = (value - src_min) / (src_max - src_min)
    return lerp(dst_min, dst_max, t)

def smooth_step(t):
    """Return 3t^2 - 2t^3 for t in [0, 1]."""
    assert 0 <= t <= 1
    return 3 * t ** 2 - 2 * t ** 3

assert clamp(5, 0, 10) == 5 and clamp(-3, 0, 10) == 0 and clamp(15, 0, 10) == 10
assert lerp(0, 10, 0.5) == 5.0 and lerp(0, 100, 0.25) == 25.0
assert normalize(75, 0, 100) == 0.75 and normalize(75, 0, 100, 0, 10) == 7.5
assert smooth_step(0.0) == 0.0 and smooth_step(0.5) == 0.5 and smooth_step(1.0) == 1.0

# --- B2 ---
def title_case(text):
    """Return text with each word's first letter upper case and the rest lower case."""
    words = text.split()
    result = []
    for w in words:
        result.append(w[0].upper() + w[1:].lower())
    return " ".join(result)

def count_substring(text, sub):
    """Count non-overlapping occurrences of sub in text, without .count(). Requires sub != ''."""
    assert sub != ""
    count = 0
    i = 0
    while i <= len(text) - len(sub):
        if text[i:i + len(sub)] == sub:
            count += 1
            i += len(sub)
        else:
            i += 1
    return count

def is_palindrome_phrase(text):
    """True if text reads the same backwards, ignoring case and spaces."""
    letters = "".join(text.lower().split())
    return letters == letters[::-1]

assert title_case("the quick brown FOX") == "The Quick Brown Fox"
assert count_substring("ababab", "ab") == 3 and count_substring("aaa", "aa") == 1 and count_substring("abc", "z") == 0
assert is_palindrome_phrase("Never odd or even") and not is_palindrome_phrase("hello")

# --- B3 ---
def apply_to_all(func, lst):
    """Return a new list holding func(x) for each x in lst."""
    result = []
    for x in lst:
        result.append(func(x))
    return result

def keep_if(predicate, lst):
    """Return a new list of the elements x of lst with predicate(x) true."""
    result = []
    for x in lst:
        if predicate(x):
            result.append(x)
    return result

def compose(f, g):
    """Return a function computing f(g(x))."""
    return lambda x: f(g(x))

assert apply_to_all(str.upper, ["hello", "world"]) == ["HELLO", "WORLD"]
assert keep_if(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]) == [2, 4, 6]
assert compose(lambda x: x ** 2, lambda x: x * 2)(3) == 36
assert compose(lambda x: x * 2, lambda x: x ** 2)(3) == 18

# --- B4 ---
def percentage(score, max_score):
    return score / max_score * 100

def contribution(score, max_score, weight):
    return percentage(score, max_score) * weight

def weighted_average(assignments):
    total = 0
    for name, score, max_score, weight in assignments:
        total += contribution(score, max_score, weight)
    return total

def letter_grade(pct):
    cutoffs = [(93, "A"), (90, "A-"), (87, "B+"), (83, "B"), (80, "B-"),
               (77, "C+"), (73, "C"), (70, "C-"), (60, "D")]
    for cutoff, letter in cutoffs:
        if pct >= cutoff:
            return letter
    return "F"

def print_report(assignments):
    print(f"  {'Assignment':<18}{'Score':>6}{'Max':>6}{'Weight':>8}{'Contrib':>9}")
    for name, score, max_score, weight in assignments:
        print(f"  {name:<18}{score:>6}{max_score:>6}{weight:>8.1%}{contribution(score, max_score, weight):>8.2f}%")
    avg = weighted_average(assignments)
    print(f"  Weighted average: {avg:.2f}%   Letter grade: {letter_grade(avg)}")

assignments = [
    ("Problem Set 1", 87, 100, 0.30),
    ("Problem Set 2", 92, 100, 0.30),
    ("Midterm", 78, 100, 0.25),
    ("Lab Average", 95, 100, 0.10),
    ("Participation", 100, 100, 0.05),
]
assert letter_grade(93) == "A" and letter_grade(92.99) == "A-" and letter_grade(59) == "F"
print_report(assignments)

# --- B5 ---
def power(base, exp):
    """Return base ** exp for exp >= 0, recursively."""
    if exp == 0:          # base case: b^0 = 1
        return 1
    return base * power(base, exp - 1)   # b^e = b * b^(e-1)

def gcd(a, b):
    """Return gcd(a, b) by Euclid's rule, recursively."""
    if b == 0:            # base case: gcd(a, 0) = a
        return a
    return gcd(b, a % b)  # any common divisor of a and b also divides a % b

assert power(2, 10) == 1024 and power(3, 0) == 1
assert gcd(48, 18) == 6 and gcd(1071, 462) == 21
print("all asserts passed")
```

B3(c): `compose(g, f)(3)` squares first then doubles: `18`. Order matters: `f(g(x))` ≠ `g(f(x))` in general.

**Marking.** B1 (14): 3/3/4/4 — `normalize` must call `lerp`. B2 (12): 4 each — `count_substring`
must skip past a match (`"aaa"` → 1, not 2). B3 (12): 4 each. B4 (16): 2/2/4/4/4 — the report must
match to the column. B5 (10): 5 each including correct base-case and step comments.
Each function missing its docstring or two asserts: −1 (max −5).

---

*CS 101 · Week 3 · Problem Set 3 · Due Friday 23 October 2026, 17:00 · © CSE Department*
