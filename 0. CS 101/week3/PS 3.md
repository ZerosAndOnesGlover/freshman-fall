---
assessment: PS 3
course: CS 101
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-19
submitted: 2026-10-23
graded: 2026-10-26
source: "PS 3 Functions and Scope.md"
---

# CS 101 · PS 3
## Answer Sheet

**Assessment:** `PS 3 Functions and Scope.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### A1 — Call Stack Trace  (12 points)

**Your answer:**

**(a)** Stack while the **first** call to `multiply` runs (top of stack first):

| Frame | Variables |
|-------|-----------|
| `multiply` | `a = 2`, `b = 3` |
| `power_sum` | `base = 2`, `exp = 3`, `n = 4`, `total = 0`, `i = 1` |
| `run` | *(none)* |
| module (global) | `multiply`, `power_sum`, `run` |

**(b)** **4** calls to `multiply` — one for each `i` in `range(1, 5)`.

**(c)** The frame is **popped** off the stack; its local variables (`total`, `i`) and its parameters
(`base`, `exp`, `n`) are discarded. Only the returned **value** survives, and it is bound to `result`
in `run`'s frame.

**(d)** Working:

```
i = 1:  multiply(2 ** 1, 3) = 2 * 3  = 6
i = 2:  multiply(2 ** 2, 3) = 4 * 3  = 12
i = 3:  multiply(2 ** 3, 3) = 8 * 3  = 24
i = 4:  multiply(2 ** 4, 3) = 16 * 3 = 48
total = 6 + 12 + 24 + 48 = 90
```

`answer == 90`.

_Marks: 12 / 12_

---

### A2 — Scope  (14 points)

**Your answer:**

**(a)** Prints `3`, then `2`, then `1`.
LEGB: each `x = …` creates a **new local** in its own function. Inside `g`, `x = 3` is local, so
`print(x)` → `3`. Back in `f`, its own local `x = 2` is printed → `2`. At module level the global
`x = 1` is printed → `1`. The inner assignments never touch the outer names.

**(b)** Raises **`UnboundLocalError`**.
Because `x = 20` appears anywhere in `f`, Python treats `x` as **local to `f` for the entire body**.
The `print(x)` runs *before* the local has been assigned, so there is no local value to read and no
fallback to the global.

**(c)** Prints `[9, 16]`.
`result.append(...)` **mutates** the object the global name already refers to; it does not rebind the
name `result`, so no `global` declaration is needed. After the two calls the list holds `9` and `16`.

**(d)** Prints `8`, `13`, `16`.
`make_adder` returns the inner `adder`, which **closes over** its enclosing `n`. `add5` remembers
`n = 5` and `add10` remembers `n = 10`. So `add5(3) = 8`, `add10(3) = 13`, and
`add5(add10(1)) = add5(11) = 16`.

_Marks: 14 / 14_

---

### A3 — Critique  (8 points)

**Your answer:**

Three specific problems with `def do_stuff(x, y=[], z=0):`:

1. **Mutable default argument.** `y=[]` is evaluated **once**, when the function is defined, so the
   same list is shared across every call. A second call `do_stuff(5)` would append to the list left
   over from the first, silently accumulating state.
2. **Side effects / mixed responsibilities.** The function `print`s while it computes (and prints
   `item`s as a side effect). A computing function should be *pure*; I/O should be separate, and the
   `print("computing...")`/`print(item)` calls make its behaviour hard to test.
3. **`z` is added once per item, and the list is returned by reference.** `total = total + item + z`
   adds `z` for **every** element, which is almost certainly not what was meant (you would expect the
   offset once). It also returns the caller's own (mutated) `y`, leaking aliasing.

**Corrected version:**

```python
def total_with_offset(values, offset=0):
    """Return the sum of values plus offset, added once."""
    total = 0
    for v in values:
        total += v
    return total + offset
```

_Marks: 8 / 8_

---

### B1 — Math Library  (16 points)

**Your answer:**

Reference `ps3.py` (submitted in `0. CS 101/week3/`), Part B1:

```python
def clamp(value, lo, hi):
    """Return value restricted to the closed interval [lo, hi]. Requires lo <= hi."""
    assert lo <= hi, "lo must not exceed hi"
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value

assert clamp(5, 0, 10) == 5
assert clamp(-3, 0, 10) == 0
assert clamp(15, 0, 10) == 10

def lerp(a, b, t):
    """Return the point a fraction t of the way from a to b. Requires 0 <= t <= 1."""
    assert 0 <= t <= 1, "t must be in [0, 1]"
    return a + (b - a) * t

assert lerp(0, 10, 0.5) == 5.0
assert lerp(0, 100, 0.25) == 25.0

def normalize(value, src_min, src_max, dst_min=0.0, dst_max=1.0):
    """Rescale value from [src_min, src_max] into [dst_min, dst_max], by calling lerp."""
    t = (value - src_min) / (src_max - src_min)
    return lerp(dst_min, dst_max, t)

assert normalize(75, 0, 100) == 0.75
assert normalize(75, 0, 100, 0, 10) == 7.5
assert normalize(50, 0, 100, 0, 1) == 0.5
```

`clamp(5,0,10) = 5`, `clamp(-3,0,10) = 0`, `clamp(15,0,10) = 10`; `lerp(0,10,0.5) = 5.0`;
`normalize(75,0,100) = 0.75` and `normalize(75,0,100,0,10) = 7.5` (both by calling `lerp`).

_Marks: 16 / 16_

---

### B2 — Strings  (14 points)

**Your answer:**

```python
def title_case(text):
    """Return text with each word's first letter upper case and the rest lower case."""
    words = text.split()
    result = []
    for w in words:
        result.append(w[0].upper() + w[1:].lower())
    return " ".join(result)

assert title_case("the quick brown FOX") == "The Quick Brown Fox"
assert title_case("HELLO world") == "Hello World"

def count_substring(text, sub):
    """Count non-overlapping occurrences of sub in text. Requires sub != "" and no .count()."""
    assert sub != "", "sub must not be empty"
    count = 0
    i = 0
    while i <= len(text) - len(sub):
        if text[i:i + len(sub)] == sub:
            count += 1
            i += len(sub)          # skip the whole match so occurrences never overlap
        else:
            i += 1
    return count

assert count_substring("ababab", "ab") == 3
assert count_substring("aaa", "aa") == 1
assert count_substring("abc", "z") == 0
```

`title_case("the quick brown FOX")` → `"The Quick Brown Fox"`. `count_substring("ababab","ab")` → `3`;
`count_substring("aaa","aa")` → `1` (the match is skipped past, so occurrences are non-overlapping).

_Marks: 14 / 14_

---

### B3 — Functions as Values  (12 points)

**Your answer:**

```python
def apply_to_all(func, lst):
    """Return a new list holding func(x) for every x in lst."""
    result = []
    for x in lst:
        result.append(func(x))
    return result

assert apply_to_all(str.upper, ["hello", "world"]) == ["HELLO", "WORLD"]
assert apply_to_all(len, ["a", "bb", "ccc"]) == [1, 2, 3]

def keep_if(predicate, lst):
    """Return a new list of the elements x of lst for which predicate(x) is true."""
    result = []
    for x in lst:
        if predicate(x):
            result.append(x)
    return result

assert keep_if(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]) == [2, 4, 6]
assert keep_if(lambda x: x > 0, [-1, 0, 1, 2]) == [1, 2]
```

`apply_to_all(str.upper, ["hello","world"])` → `["HELLO","WORLD"]`;
`keep_if(lambda x: x % 2 == 0, [1,2,3,4,5,6])` → `[2,4,6]`.

_Marks: 12 / 12_

---

### B4 — Decomposition — Grade Report  (24 points)

**Your answer:**

```python
assignments = [
    ("Problem Set 1", 87, 100, 0.30),
    ("Problem Set 2", 92, 100, 0.30),
    ("Midterm", 78, 100, 0.25),
    ("Lab Average", 95, 100, 0.10),
    ("Participation", 100, 100, 0.05),
]

def percentage(score, max_score):
    """Return the score as a percentage of max_score."""
    return score / max_score * 100

assert percentage(87, 100) == 87.0
assert percentage(1, 2) == 50.0

def contribution(score, max_score, weight):
    """Return one assignment's weighted contribution (percentage times weight)."""
    return percentage(score, max_score) * weight

assert round(contribution(87, 100, 0.30), 2) == 26.10
assert contribution(100, 100, 0.05) == 5.0

def weighted_average(assignments):
    """Return the sum of the contributions of all the assignments."""
    total = 0
    for name, score, max_score, weight in assignments:
        total += contribution(score, max_score, weight)
    return total

assert round(weighted_average(assignments), 2) == 87.70
assert weighted_average([("x", 50, 100, 1.0)]) == 50.0

def letter_grade(pct):
    """Return the letter grade for a percentage, using the course cutoffs."""
    cutoffs = [(93, "A"), (90, "A-"), (87, "B+"), (83, "B"), (80, "B-"),
               (77, "C+"), (73, "C"), (70, "C-"), (60, "D")]
    for cutoff, letter in cutoffs:
        if pct >= cutoff:
            return letter
    return "F"

assert letter_grade(93) == "A" and letter_grade(92.99) == "A-"
assert letter_grade(87) == "B+" and letter_grade(59.99) == "F"

def print_report(assignments):
    """Print a formatted grade report and the final weighted average and letter grade."""
    print(f"  {'Assignment':<18}{'Score':>6}{'Max':>6}{'Weight':>8}{'Contrib':>9}")
    for name, score, max_score, weight in assignments:
        print(f"  {name:<18}{score:>6}{max_score:>6}{weight:>8.1%}{contribution(score, max_score, weight):>8.2f}%")
    avg = weighted_average(assignments)
    print(f"  Weighted average: {avg:.2f}%   Letter grade: {letter_grade(avg)}")

print_report(assignments)
```

Output (matches the spec to the column):

```
  Assignment         Score   Max  Weight  Contrib
  Problem Set 1         87   100   30.0%   26.10%
  Problem Set 2         92   100   30.0%   27.60%
  Midterm               78   100   25.0%   19.50%
  Lab Average           95   100   10.0%    9.50%
  Participation        100   100    5.0%    5.00%
  Weighted average: 87.70%   Letter grade: B+
```

_Marks: 24 / 24_

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-26 |

**Feedback:**
Full marks. A1 draws the stack correctly (four frames, `power_sum`'s `total=0, i=1` while the first
`multiply(2,3)` runs), counts 4 calls, explains the frame pop, and arrives at 90 with working shown.
A2 is correct on all four and reasons with LEGB (including the closure in (d) and the aliasing vs
rebinding distinction in (c)); (b)'s `UnboundLocalError` is correctly attributed to the assignment
making `x` local for the whole body. A3 names three real problems (shared mutable default, side
effects/mixed duties, per-item offset) and fixes them.

Part B: every function carries a docstring and at least two asserts, and there are no stray `print`s
inside pure functions. B1's `normalize` correctly delegates to `lerp`; B2 skips past each match so
`"aaa","aa"` → 1; B3 handles function values and a predicate; B4's report matches the required
layout exactly and the letter-grade cutoffs are inclusive as specified.
