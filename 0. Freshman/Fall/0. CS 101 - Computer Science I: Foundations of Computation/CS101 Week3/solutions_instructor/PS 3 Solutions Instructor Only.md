# CS 101 · Problem Set 3 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps3.py` below was run: every `assert` passes and
> the report prints exactly as shown in B4.

### A1 (12)

(a) Top to bottom: `multiply` {a=2, b=3} · `power_sum` {base=2, exp=3, n=4, total=0, i=1} · `run` {} ·
module {multiply, power_sum, run}. *(5)*
(b) **4** calls. *(2)* (c) The frame is popped; `total`, `i` and the parameters are gone. Only the
returned **value** survives, bound to `result` in `run`'s frame. *(2)*
(d) 2·3 + 4·3 + 8·3 + 16·3 = 6 + 12 + 24 + 48 = **90**. *(3)*

### A2 (14: 3, 4, 3, 4)

(a) `3`, `2`, `1` — each `x =` creates a new local in its own function. (b) `UnboundLocalError`:
the assignment makes `x` local to `f` for the **whole** body, so `print(x)` reads an unassigned
local. (c) `[9, 16]` — `append` mutates the global list; it does not rebind the name, so no
`global` is needed. (d) `8`, `13`, `16`. `add5` is the inner function `adder`, closing over `n = 5`
from `make_adder`'s enclosing scope (L11 on closures).

### A3 (8)

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

assert clamp(5, 0, 10) == 5 and clamp(-3, 0, 10) == 0 and clamp(15, 0, 10) == 10
assert lerp(0, 10, 0.5) == 5.0 and lerp(0, 100, 0.25) == 25.0
assert normalize(75, 0, 100) == 0.75 and normalize(75, 0, 100, 0, 10) == 7.5

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

assert title_case("the quick brown FOX") == "The Quick Brown Fox"
assert count_substring("ababab", "ab") == 3 and count_substring("aaa", "aa") == 1 and count_substring("abc", "z") == 0

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

assert apply_to_all(str.upper, ["hello", "world"]) == ["HELLO", "WORLD"]
assert keep_if(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]) == [2, 4, 6]

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

print("all asserts passed")
```

**Marking.** B1 (16): 5/5/6 — `normalize` must call `lerp`. B2 (14): 7 each — `count_substring`
must skip past a match (`"aaa"` → 1, not 2). B3 (12): 6 each. B4 (24): 3/3/6/6/6 — the report must
match to the column.
Each function missing its docstring or two asserts: −1 (max −5).

---

*CS 101 · Week 3 · Problem Set 3 · Due Friday 23 October 2026, 17:00 · © CSE Department*
