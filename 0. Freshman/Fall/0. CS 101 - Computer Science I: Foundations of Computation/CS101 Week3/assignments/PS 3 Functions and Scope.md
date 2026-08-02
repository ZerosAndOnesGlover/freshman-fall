# CS 101 Problem Set 3
## Functions, Scope, and the Call Stack

**Released:** Friday, Week 3
**Due:** Friday, Week 4 at 11:59 PM
**Submission:** Upload `ps3.py` and `PS 3 Functions and Scope.md`
**Weight:** Part of the 30% Problem Sets grade

---

## Overview

This problem set covers:
- Function definitions, parameters, return values
- Scope, the LEGB rule, and the call stack
- Default parameters (including the mutable default trap)
- Function decomposition and the single responsibility principle
- Pure functions vs. functions with side effects
- First steps with recursion (preview of Week 4)
- Docstrings, assertions, and specifications

**Structure:**
- Part A: Written — conceptual and reasoning questions
- Part B: Python implementation — 7 problems
- Part C: Challenge (ungraded)

---

## Part A: Written (`PS 3 Functions and Scope.md`)

### A1: Call Stack Trace (8 points)

Trace the call stack for the following program. For each function call, draw the stack at its **deepest point** (the moment just before the innermost function returns).

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

**(a)** When `multiply(2**1, 3)` is executing (the first call to `multiply`), draw the complete call stack showing all frames and the variables in each frame.

**(b)** How many total calls to `multiply` are made during the entire execution?

**(c)** After `power_sum` returns, which variables from its frame still exist somewhere? Which are destroyed?

**(d)** What is the final value of `answer`? Show your work.

---

### A2: Scope Analysis (8 points)

For each code snippet, predict the output **without running it**. Then explain using the LEGB rule.

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

For (d): what is `add5`? What is `n` inside `adder` when `add5(3)` is called?

---

### A3: Specification Writing (6 points)

Write a complete docstring specification for each function. Include: what it does, args (with types), returns (type and meaning), preconditions, and at least 2 examples.

**(a)** A function `bisect(lst, target)` that, given a **sorted** list and a target value, returns the index where target should be inserted to maintain sorted order.
- `bisect([1, 3, 5, 7], 4)` → `2` (between index 1 and 2)
- `bisect([1, 3, 5, 7], 7)` → `3` (at the last element)
- `bisect([1, 3, 5, 7], 9)` → `4` (after all elements)

**(b)** A function `run_length_decode(encoded)` that decompresses a run-length encoded string.
- `run_length_decode("3a2b1c")` → `"aaabbc"`

---

### A4: Function Design Critique (4 points)

Critique this function. List at least **3 specific problems** and write a corrected version.

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

## Part B: Python Implementation (`ps3.py`)

All functions must have:
- A complete docstring
- At least 2 `assert` tests below the definition
- No `print()` calls (unless the function is explicitly a display function)

---

### B1: Mathematical Functions Library (12 points)

Implement a small math library. Every function must be **pure** (no side effects, no global variables).

**(a)** `clamp(value, lo, hi)` — restrict value to [lo, hi]
- `clamp(5, 0, 10)` → `5`
- `clamp(-3, 0, 10)` → `0`
- `clamp(15, 0, 10)` → `10`
- Raise `ValueError` if `lo > hi`

**(b)** `lerp(a, b, t)` — linear interpolation
- `lerp(0, 10, 0.5)` → `5.0`
- `lerp(0, 100, 0.25)` → `25.0`
- Raise `ValueError` if `t < 0` or `t > 1`

**(c)** `normalize(value, src_min, src_max, dst_min=0.0, dst_max=1.0)` — rescale from one range to another. Use `lerp`.
- `normalize(75, 0, 100)` → `0.75`
- `normalize(75, 0, 100, 0, 10)` → `7.5`

**(d)** `smooth_step(t)` — a smooth interpolation curve: `3t² - 2t³`
- Smoother than linear interpolation for animations
- `smooth_step(0.0)` → `0.0`
- `smooth_step(0.5)` → `0.5`
- `smooth_step(1.0)` → `1.0`
- The derivative (slope) at 0 and 1 is 0 — verify numerically

**(e)** `map_range(value, src_min, src_max, dst_min, dst_max)` — map value from one range to another, clamping to destination range.
- `map_range(50, 0, 100, 0, 255)` → `127.5`
- `map_range(150, 0, 100, 0, 255)` → `255` (clamped)

**(f)** `moving_average(data, window)` — compute the moving average of a list with the given window size. Return a list of length `len(data) - window + 1`.
- `moving_average([1, 2, 3, 4, 5], 3)` → `[2.0, 3.0, 4.0]`

---

### B2: String Processing Functions (10 points)

**(a)** `title_case(text)` — convert to title case without using `.title()`.
- Every word's first letter is uppercase, rest lowercase.
- `title_case("the quick brown FOX")` → `"The Quick Brown Fox"`

**(b)** `wrap_text(text, width)` — wrap text at word boundaries so no line exceeds `width` characters. Return a list of lines.
- `wrap_text("The quick brown fox", 10)` → `["The quick", "brown fox"]`
- `wrap_text("a", 10)` → `["a"]`
- Words longer than width appear on their own line.

**(c)** `justify_line(text, width)` — pad spaces between words so the line is exactly `width` characters wide. If only one word, left-align.
- `justify_line("Hello world", 20)` → `"Hello          world"`
- Distribute extra spaces as evenly as possible from left to right.

**(d)** `count_substring(text, sub)` — count non-overlapping occurrences of `sub` in `text` without using `.count()`.
- `count_substring("ababab", "ab")` → `3`
- `count_substring("aaa", "aa")` → `1` (non-overlapping)

**(e)** `compress(text)` — compress text by replacing runs of 3+ identical characters with `count:char`.
- `compress("aaabbbccccdd")` → `"3:a3:b4:cdd"` — runs `aaa`→`3:a`, `bbb`→`3:b`, `cccc`→`4:c`; the final `dd` is a run of only 2, so it is left as-is
- `compress("hello")` → `"hello"` (no runs of 3+; `ll` is only 2)
- `compress("aaaa")` → `"4:a"`

---

### B3: Higher-Order Functions (10 points)

**(a)** `apply_to_all(func, lst)` — return a new list with `func` applied to each element.
- `apply_to_all(str.upper, ["hello", "world"])` → `["HELLO", "WORLD"]`

**(b)** `keep_if(predicate, lst)` — return a new list with only elements where `predicate(element)` is True.
- `keep_if(lambda x: x % 2 == 0, [1,2,3,4,5,6])` → `[2,4,6]`

**(c)** `reduce_with(func, lst, initial)` — combine all elements using `func`, starting from `initial`.
- `reduce_with(lambda a, b: a + b, [1,2,3,4], 0)` → `10`
- `reduce_with(lambda a, b: a * b, [1,2,3,4], 1)` → `24`

**(d)** `compose(f, g)` — return a new function that computes `f(g(x))`.
- `double_then_square = compose(lambda x: x**2, lambda x: x*2)`
- `double_then_square(3)` → `(3*2)**2 = 36`

**(e)** `memoize(func)` — return a new function that caches results.
- The first call to `memoized_func(x)` computes `func(x)` and stores it.
- Subsequent calls with the same `x` return the cached result.
- Demonstrate with a slow function (`import time; time.sleep(0.1)`).

---

### B4: Functional Decomposition — Grade Calculator (14 points)

Build a complete grade calculator using well-decomposed functions. The calculator:
- Takes a list of `(assignment_name, score, max_score, weight)` tuples
- Computes the weighted average grade
- Assigns a letter grade
- Produces a formatted report

```python
assignments = [
    ("Problem Set 1",  87,  100, 0.30),
    ("Problem Set 2",  92,  100, 0.30),
    ("Midterm",        78,  100, 0.25),
    ("Lab Average",    95,  100, 0.10),
    ("Participation",  100, 100, 0.05),
]
```

**Required functions (in this order — each calls the previous):**

1. `percentage(score, max_score)` → `float` — score as a percentage (0–100)
2. `weighted_score(score, max_score, weight)` → `float` — weighted contribution
3. `weighted_average(assignments)` → `float` — overall weighted percentage
4. `letter_grade(percentage)` → `str` — "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"
5. `grade_points(letter)` → `float` — GPA points (A=4.0, A-=3.7, B+=3.3, B=3.0, etc.)
6. `format_assignment_row(name, score, max_score, weight, contribution)` → `str` — one formatted row
7. `print_grade_report(assignments)` — prints the complete report

Example output:
```
══════════════════════════════════════════════════════
  GRADE REPORT
══════════════════════════════════════════════════════
  Assignment           Score  Max  Weight  Contrib
  ─────────────────────────────────────────────────
  Problem Set 1         87   100   30.0%   26.10%
  Problem Set 2         92   100   30.0%   27.60%
  Midterm               78   100   25.0%   19.50%
  Lab Average           95   100   10.0%    9.50%
  Participation        100   100    5.0%    5.00%
  ─────────────────────────────────────────────────
  Weighted Average:                         87.70%
  Letter Grade:                             B+
  GPA Points:                               3.3
══════════════════════════════════════════════════════
```

---

### B5: Recursive Functions (10 points)

Implement each function recursively. State the loop invariant (or its recursive equivalent: base case + inductive step) in a comment.

**(a)** `power(base, exp)` — compute `base ** exp` for non-negative integer `exp`.
- `power(2, 10)` → `1024`
- `power(3, 0)` → `1`

**(b)** `gcd_recursive(a, b)` — Euclidean GCD using recursion.
- `gcd_recursive(48, 18)` → `6`
- **Inductive step:** `gcd(a, b) = gcd(b, a % b)` — why does this preserve the GCD?

**(c)** `flatten(lst)` — given a list that may contain nested lists, return a flat list of all non-list elements.
- `flatten([1, [2, [3, 4]], 5])` → `[1, 2, 3, 4, 5]`
- `flatten([])` → `[]`
- `flatten([[[1]]])` → `[1]`
- Hint: check `isinstance(item, list)` to decide whether to recurse or append.

**(d)** `binary_to_int(binary_str)` — convert a binary string to its integer value, recursively.
- `binary_to_int("101")` → `5`
- `binary_to_int("1")` → `1`
- `binary_to_int("0")` → `0`
- Recursive insight: `"101"` → `"10"` contributes `int("10" converted) * 2 + int("1")`.

**(e)** `merge_sorted(lst1, lst2)` — given two sorted lists, return a single merged sorted list, recursively.
- `merge_sorted([1, 3, 5], [2, 4, 6])` → `[1, 2, 3, 4, 5, 6]`
- `merge_sorted([], [1, 2])` → `[1, 2]`
- This is the key subroutine of merge sort (coming in Week 5).

---

### B6: Closures and Function Factories (10 points)

**(a)** `make_counter(start=0, step=1)` — return a function that, each time it's called, returns the next value in the sequence `start, start+step, start+2*step, ...`.
```python
c = make_counter(10, 5)
c()  # 10
c()  # 15
c()  # 20
```

**(b)** `make_validator(min_val, max_val, allow_none=False)` — return a function `validate(x)` that returns True if `x` is in [min_val, max_val], or (if allow_none) if x is None.
```python
validate_age = make_validator(0, 150)
validate_age(25)   # True
validate_age(-1)   # False
validate_age(None) # False

validate_score = make_validator(0, 100, allow_none=True)
validate_score(None)  # True
```

**(c)** `make_pipeline(*funcs)` — return a function that applies `funcs` in sequence, passing each result to the next.
```python
process = make_pipeline(str.strip, str.lower, str.split)
process("  Hello World  ")   # ['hello', 'world']
```

**(d)** `once(func)` — return a new function that calls `func` at most once. Subsequent calls return the first result without calling `func` again.
```python
expensive = once(lambda: print("computing...") or 42)
expensive()   # prints "computing...", returns 42
expensive()   # returns 42 (no print — func not called again)
```

---

### B7: Complete Decomposed Program — Polynomial Calculator (12 points)

A polynomial can be represented as a list of coefficients where `coeffs[i]` is the coefficient of x^i.

Example: `[2, -3, 1]` represents `2 - 3x + x²`

Implement:

**(a)** `poly_eval(coeffs, x)` — evaluate the polynomial at x.
- `poly_eval([2, -3, 1], 2)` → `2 - 6 + 4 = 0`

**(b)** `poly_add(p, q)` — add two polynomials.
- `poly_add([1, 2], [3, 0, 1])` → `[4, 2, 1]` (i.e., `4 + 2x + x²`)

**(c)** `poly_scale(p, scalar)` — multiply polynomial by a scalar.
- `poly_scale([1, 2, 3], 2)` → `[2, 4, 6]`

**(d)** `poly_multiply(p, q)` — multiply two polynomials.
- `poly_multiply([1, 1], [1, 1])` → `[1, 2, 1]` (i.e., `(1+x)² = 1 + 2x + x²`)

**(e)** `poly_derivative(p)` — compute the derivative.
- Derivative of `a₀ + a₁x + a₂x² + ...` is `a₁ + 2a₂x + 3a₃x² + ...`
- `poly_derivative([2, -3, 1])` → `[-3, 2]`

**(f)** `poly_to_string(coeffs)` — return a human-readable string.
- `poly_to_string([2, -3, 1])` → `"2 - 3x + x²"` (use Unicode ² for squared, ³ for cubed, etc.)

**(g)** `poly_roots_newton(coeffs, initial_guess, tolerance=1e-8, max_iter=100)` — find a root using Newton-Raphson.
- `poly_roots_newton([2, -3, 1], 2.5)` → approximately `2.0` (one root of `x² - 3x + 2`)

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|--------------|
| A1 Call Stack | 8 | Correct stack drawing, all variables named, answer shown |
| A2 Scope | 8 | All 4 snippets predicted correctly with LEGB explanation |
| A3 Specification | 6 | Complete docstrings with all required fields |
| A4 Critique | 4 | 3+ valid problems identified; correct fix |
| B1 Math library | 12 | All 6 functions, pure, tested |
| B2 Strings | 10 | All 5 functions, edge cases handled |
| B3 Higher-order | 10 | All 5 functions, including memoize |
| B4 Grade calculator | 14 | All 7 functions, correct output, formatted |
| B5 Recursive | 10 | All 5, base + inductive step commented |
| B6 Closures | 10 | All 4, closures work across multiple calls |
| B7 Polynomial | 12 | All 7, correct algebra |
| **Total** | **104** | |
| Style / docstrings | up to 5 bonus | |

---

## Part C: Challenge (Ungraded)

**C1: Decorator pattern**
Implement a `timer` decorator that prints how long a function takes to execute:
```python
@timer
def slow_function():
    import time; time.sleep(1)

slow_function()   # prints: "slow_function took 1.001s"
```

**C2: Trampoline for tail recursion**
Python doesn't optimize tail calls. Implement a `trampoline` function that makes tail-recursive functions run in O(1) stack space:
```python
def factorial_tr(n, acc=1):
    if n == 0:
        return acc
    return lambda: factorial_tr(n - 1, n * acc)   # returns a thunk instead of calling

result = trampoline(factorial_tr)(10000)   # won't overflow the stack!
```

**C3: Y combinator**
Implement the Y combinator in Python and use it to define a recursive factorial function without using `def`:
```python
Y = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))
factorial = Y(lambda f: lambda n: 1 if n == 0 else n * f(n - 1))
factorial(10)   # 3628800
```

Explain what the Y combinator is doing and why it enables recursion without names.

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading Rubric above (104 + up to 5 style).

### ⚠️ Errata — CORRECTED in the student-facing text above

| Location | Was (wrong) | Now |
|---|---|---|
| B2(e) `compress` | `"3:abbb4:cdd"` → **wait**: `"3:a3:b4:c2:d"` — shipped with the author's mid-sentence self-correction visible, and **neither** value satisfies the stated "runs of 3+" rule. The first leaves `bbb` (a run of 3) uncompressed; the second compresses `dd` (a run of only 2). | **`"3:a3:b4:cdd"`** — `aaa`→`3:a`, `bbb`→`3:b`, `cccc`→`4:c`, `dd` stays literal. Rewritten with the reasoning spelled out. |

Accept either printed value from students holding a pre-correction copy; the rule as stated was genuinely unfollowable.

---

### Part A — Written (26 points)

**A1 Call Stack Trace (8 pts).**

**(a)** During the first `multiply` call the stack is four frames deep (module frame at the bottom):

```
┌─ multiply          a = 2   (i.e. 2**1)   b = 3
├─ power_sum         base = 2  exp = 3  n = 4  total = 0  i = 1
├─ run               (no locals bound yet — result is still unassigned)
└─ <module>          answer = <unassigned>
```

**(b)** **4 calls** — one per iteration of `range(1, 5)`.

**(c)** Every local of `power_sum` (`base`, `exp`, `n`, `total`, `i`) is destroyed when its frame pops. Only the **returned value** survives, bound to `result` in `run`'s frame and then to `answer` at module level. Nothing else persists.

**(d)** `answer = 90`:

| i | `base ** i` | `multiply(base**i, 3)` | running `total` |
|---|---|---|---|
| 1 | 2 | 6 | 6 |
| 2 | 4 | 12 | 18 |
| 3 | 8 | 24 | 42 |
| 4 | 16 | 48 | 90 |

*Grading: 3 pts (a) — all four frames, with `power_sum`'s locals named; deduct 1 if the `<module>` frame is omitted. 1 pt (b). 2 pts (c) — must distinguish the destroyed frame from the surviving return value. 2 pts (d) with the arithmetic shown.*
*Common error: answering (b) with 5 — `range(1, n+1)` with n=4 yields 4 iterations, not 5.*

**A2 Scope Analysis (8 pts).** 2 pts each.

- **(a)** prints `3`, then `2`, then `1`. Each `x` is a distinct binding in a distinct scope; the inner assignments never touch the outer ones (no `nonlocal`/`global`). LEGB resolves each `print(x)` to the nearest enclosing binding.
- **(b)** **Raises `UnboundLocalError`.** Because `x = 20` appears anywhere in `f`'s body, Python marks `x` local for the *whole* function at compile time; the `print(x)` then reads a local that has not yet been assigned. It does **not** fall back to the global.
- **(c)** prints `[9, 16]`. `result` is never rebound — only **mutated** via `.append()`, which needs no `global` declaration. This is the mutation-vs-rebinding distinction from PS1 A1.
- **(d)** prints `8`, `13`, `16`. `add5` is a **closure**: the function `adder` together with a captured reference to the enclosing `n`. When `add5(3)` runs, `n` is `5`, found in the **E** (enclosing) scope. `add5(add10(1))` = `add5(11)` = `16`.

*Grading: 1 pt correct output + 1 pt LEGB-grounded explanation, each part. For (b), an answer of `10` earns 0 — predicting the global read is exactly the misconception under test.*

**A3 Specification Writing (6 pts).** 3 pts each. A full-credit docstring:

```python
def bisect(lst, target):
    """Return the index at which target should be inserted to keep lst sorted.

    Args:
        lst (list[int | float]): a list sorted in non-decreasing order.
        target (int | float): the value to place.

    Returns:
        int: an index i in [0, len(lst)] such that all of lst[:i] <= target
             and all of lst[i:] > target. Equal elements are passed over, so
             target is inserted after any existing copies.

    Preconditions:
        lst is already sorted ascending; target is comparable with its elements.

    Examples:
        >>> bisect([1, 3, 5, 7], 4)
        2
        >>> bisect([1, 3, 5, 7], 9)
        4
    """
```

*Grading: ½ pt each for description / args-with-types / returns / preconditions, 1 pt for two valid examples. The `bisect([1,3,5,7], 7) → 3` case in the prompt is worth probing: it asks for insertion **before** the equal element (bisect_left), while the wording "should be inserted to maintain sorted order" also admits 4 (bisect_right). Accept either **if the docstring states the tie-breaking rule**; deduct 1 if ties go unmentioned, since resolving that ambiguity is the point of the exercise.*

**A4 Function Design Critique (4 pts).** At least three of:

1. **Mutable default argument.** `y=[]` is evaluated **once** at definition time, so the list persists across calls and accumulates — the single most important Python gotcha. Repeated calls to `do_stuff(1)` return `1`, then `2`, then `3`.
2. **Side effects mixed with computation.** It prints while also computing and returning — untestable and unreusable.
3. **Mutates its argument.** `y.append(x)` modifies the caller's list in place.
4. **Meaningless name.** `do_stuff` says nothing; likewise `x`, `y`, `z`.
5. **Returns a heterogeneous tuple** `(total, y)`, one element of which is the mutated input.
6. `z` is added once per element, so it silently scales with `len(y)` — almost certainly not the intent.

```python
def accumulate_with_offset(value, values=None, offset=0):
    """Return the sum of values + [value], with offset added once per item."""
    items = list(values) if values is not None else []   # copy — never mutate the caller's list
    items.append(value)
    return sum(item + offset for item in items), items
```

*Grading: 1 pt per distinct valid problem up to 3, plus 1 pt for a fix that addresses the default-argument issue specifically (`None` sentinel + copy). A "fix" that keeps `y=[]` earns 0 for that point no matter how clean the rest is.*

---

### Part B — Coding (78 points)

**B1 Math Library (12 pts).** 2 pts each.

```python
def clamp(value, lo, hi):
    if lo > hi: raise ValueError(f"lo ({lo}) must not exceed hi ({hi})")
    return lo if value < lo else hi if value > hi else value

def lerp(a, b, t):
    if not 0 <= t <= 1: raise ValueError(f"t must be in [0,1], got {t}")
    return a + (b - a) * t

def normalize(value, src_min, src_max, dst_min=0.0, dst_max=1.0):
    if src_min == src_max: raise ValueError("empty source range")
    return lerp(dst_min, dst_max, (value - src_min) / (src_max - src_min))

def smooth_step(t):
    return 3*t**2 - 2*t**3

def map_range(value, src_min, src_max, dst_min, dst_max):
    frac = (value - src_min) / (src_max - src_min)
    return clamp(dst_min + (dst_max - dst_min) * frac, min(dst_min, dst_max), max(dst_min, dst_max))

def moving_average(data, window):
    if window <= 0 or window > len(data): raise ValueError("bad window")
    return [sum(data[i:i+window]) / window for i in range(len(data) - window + 1)]
```

Verified: `clamp(15,0,10)=10`, `lerp(0,10,.5)=5.0`, `normalize(75,0,100)=0.75`, `normalize(75,0,100,0,10)=7.5`, `smooth_step(.5)=0.5`, `map_range(50,0,100,0,255)=127.5`, `map_range(150,…)=255`, `moving_average([1,2,3,4,5],3)=[2.0,3.0,4.0]`.

*Note on (d): `smooth_step` derivative is `6t − 6t²`, which is 0 at both `t=0` and `t=1` — that is exactly why it is used for animation easing. A numeric check `(f(ε)−f(0))/ε → 0` earns the verification credit.*
*Common error: `normalize` re-deriving the interpolation instead of calling `lerp`, which the spec requires. Deduct 1 — the point is composition.*

**B2 String Functions (10 pts).** 2 pts each.

```python
def title_case(text):
    return " ".join(w[:1].upper() + w[1:].lower() for w in text.split(" "))

def wrap_text(text, width):
    lines, cur = [], ""
    for w in text.split():
        if not cur: cur = w
        elif len(cur) + 1 + len(w) <= width: cur += " " + w
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def justify_line(text, width):
    words = text.split()
    if len(words) <= 1: return text.ljust(width)
    gaps, extra = len(words) - 1, width - sum(len(w) for w in words)
    base, rem = divmod(extra, gaps)
    return "".join(w + " " * (base + (1 if i < rem else 0)) if i < gaps else w
                   for i, w in enumerate(words))

def count_substring(text, sub):
    n, i = 0, 0
    while (j := text.find(sub, i)) != -1:
        n += 1; i = j + len(sub)          # skip past — non-overlapping
    return n

def compress(text):
    out, i = "", 0
    while i < len(text):
        j = i
        while j < len(text) and text[j] == text[i]: j += 1
        run = j - i
        out += f"{run}:{text[i]}" if run >= 3 else text[i] * run
        i = j
    return out
```

Verified: `justify_line("Hello world",20)` → `"Hello          world"` (5+14+5=20). `count_substring("aaa","aa")` → `1`. `compress("aaabbbccccdd")` → `"3:a3:b4:cdd"`.

*Common errors: (d) advancing `i` by 1 instead of `len(sub)` gives **overlapping** counts — `"aaa","aa"` → 2 instead of 1; this is the specific case the spec tests. (a) using `.split()` instead of `.split(" ")` collapses runs of spaces, changing the output for double-spaced input.*

**B3 Higher-Order Functions (10 pts).** 2 pts each.

```python
def apply_to_all(func, lst):        return [func(x) for x in lst]
def keep_if(predicate, lst):        return [x for x in lst if predicate(x)]
def reduce_with(func, lst, initial):
    acc = initial
    for x in lst: acc = func(acc, x)
    return acc
def compose(f, g):                  return lambda x: f(g(x))
def memoize(func):
    cache = {}                       # closed over — one cache per decorated function
    def wrapper(*args):
        if args not in cache: cache[args] = func(*args)
        return cache[args]
    return wrapper
```

*Grading for `memoize`: 1 pt cache stored in the closure (not a global), 1 pt correct hit/miss behaviour. Demonstrating with `time.sleep(0.1)` should show the second call returning near-instantly.*
*Common error: `compose(f, g)` returning `g(f(x))`. The spec fixes the order — `double_then_square(3)` must be `36`, not `(3**2)*2 = 18`. Check that value specifically.*

**B4 Grade Calculator (14 pts).** Verified against the sample — the report reproduces exactly:

| Assignment | Score | Max | Weight | Contribution |
|---|---|---|---|---|
| Problem Set 1 | 87 | 100 | 30.0% | 26.10% |
| Problem Set 2 | 92 | 100 | 30.0% | 27.60% |
| Midterm | 78 | 100 | 25.0% | 19.50% |
| Lab Average | 95 | 100 | 10.0% | 9.50% |
| Participation | 100 | 100 | 5.0% | 5.00% |
| **Weighted Average** | | | | **87.70%** |

→ Letter **B+**, GPA **3.3**.

*Grading: 1 pt each for functions 1–3 and 5–6 (5), 3 pts `letter_grade` (full band table), 2 pts `print_grade_report` formatting, 4 pts for correct decomposition — each function actually calling the previous rather than one monolith. Deduct all 4 if `print_grade_report` recomputes everything inline.*
*Boundary check: 87.70 must land in B+ under the student's own stated band table. Any coherent scale is acceptable, but it must be documented and applied consistently.*

**B5 Recursive Functions (10 pts).** 2 pts each.

```python
def power(base, exp):
    # base: exp == 0 -> 1.  step: base**exp == base * base**(exp-1)
    return 1 if exp == 0 else base * power(base, exp - 1)

def gcd_recursive(a, b):
    # base: b == 0 -> a.  step: gcd(a,b) == gcd(b, a % b)
    return a if b == 0 else gcd_recursive(b, a % b)

def flatten(lst):
    out = []
    for item in lst:
        out.extend(flatten(item)) if isinstance(item, list) else out.append(item)
    return out

def binary_to_int(s):
    # base: single char.  step: value(s) == value(s[:-1])*2 + last bit
    return int(s) if len(s) == 1 else binary_to_int(s[:-1]) * 2 + int(s[-1])

def merge_sorted(a, b):
    if not a: return list(b)
    if not b: return list(a)
    return ([a[0]] + merge_sorted(a[1:], b)) if a[0] <= b[0] else ([b[0]] + merge_sorted(a, b[1:]))
```

**Why `gcd(a,b) = gcd(b, a%b)` preserves the GCD** (asked explicitly in (b)): write `a = qb + r`. Any `d` dividing both `a` and `b` divides `r = a − qb`, so it is a common divisor of `(b, r)`. Conversely any `d` dividing `b` and `r` divides `a = qb + r`. The two pairs therefore have *identical* sets of common divisors, hence the same greatest one.

*Grading: 1 pt code + 1 pt base-case/inductive-step comment, each part — the rubric requires the comment, so code alone caps at 1.*
*Common error: `flatten` using `out.append(flatten(item))` instead of `extend`, producing nested output. Test `flatten([[[1]]])` → must be `[1]`, not `[[1]]`.*

**B6 Closures (10 pts).**

```python
def make_counter(start=0, step=1):
    current = start
    def counter():
        nonlocal current             # nonlocal is essential — rebinding, not mutating
        value = current
        current += step
        return value
    return counter

def make_validator(min_val, max_val, allow_none=False):
    def validate(x):
        if x is None: return allow_none
        return min_val <= x <= max_val
    return validate

def make_pipeline(*funcs):
    def run(value):
        for f in funcs: value = f(value)
        return value
    return run

def once(func):
    done, result = False, None
    def wrapper(*a, **kw):
        nonlocal done, result
        if not done: result, done = func(*a, **kw), True
        return result
    return wrapper
```

*Grading: 2 pts (a) — **`nonlocal` is the whole point**; without it the counter raises `UnboundLocalError` on the second statement. 2 pts (b) including the `None` branch. 3 pts (c). 3 pts (d) — must not call `func` again, and must still return the cached result.*
*Verify (a) returns `10, 15, 20` — a counter that returns `current` **after** incrementing yields `15, 20, 25` and loses the start value.*

**B7 Polynomial Calculator (12 pts).** Verified: `poly_eval([2,-3,1],2)=0`; `poly_multiply([1,1],[1,1])=[1,2,1]`; `poly_derivative([2,-3,1])=[-3,2]`; Newton from 2.5 converges to `2.0000000000`.

```python
def poly_eval(c, x):  return sum(a * x**i for i, a in enumerate(c))
def poly_add(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]
def poly_scale(p, k): return [a * k for a in p]
def poly_multiply(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): r[i+j] += a * b
    return r
def poly_derivative(p): return [i * a for i, a in enumerate(p)][1:]
def poly_roots_newton(c, x, tolerance=1e-8, max_iter=100):
    d = poly_derivative(c)
    for _ in range(max_iter):
        fx = poly_eval(c, x)
        if abs(fx) < tolerance: return x
        dfx = poly_eval(d, x)
        if dfx == 0: raise ValueError("zero derivative — Newton stalled")
        x -= fx / dfx
    raise ValueError("did not converge")
```

*Grading: 1 pt each (a)(c)(e), 2 pts (b) (unequal lengths), 2 pts (d), 2 pts (f), 3 pts (g).*
*(f) is the fiddly one — require correct handling of: coefficient `1` printed as `x` not `1x`; negative coefficients rendered as `- 3x` not `+ -3x`; zero coefficients omitted; the constant term carrying no `x`. `poly_to_string([2,-3,1])` → `"2 - 3x + x²"`.*
*(g) must guard `dfx == 0`; an unguarded version raises `ZeroDivisionError` on a stationary start point. Deduct 1 if absent.*

---

### Part C — Challenge (ungraded)

- **C1/C2 Trampolining** sidesteps Python's ~1000-frame recursion limit by returning thunks and driving them from a loop — CPython has no tail-call optimisation, so this is the only pure-Python route to deep recursion.
- **C3 Y combinator** achieves recursion without self-reference: `Y(f)` produces a fixed point of `f`, so the function receives *itself* as an argument rather than looking itself up by name. The `lambda v: x(x)(v)` wrapper is the eta-expansion needed to keep it lazy under applicative-order evaluation — without it, Python evaluates `x(x)` eagerly and recurses forever.

---

*CS 101 · Week 3 · Problem Set 3 · Due Friday Week 4 · © CSE Department*
