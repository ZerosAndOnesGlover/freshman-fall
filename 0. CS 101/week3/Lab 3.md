---
assessment: Lab 3
course: CS 101
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-20
submitted: 2026-10-20
graded: 2026-10-23
source: "LAB 3 Stack Frames and Functions.md"
---

# CS 101 · Lab 3
## Answer Sheet

**Assessment:** `LAB 3 Stack Frames and Functions.md`
**Points available:** 100

Code in this folder: `scope_bugs.py` (Part 2), `text_statistics.py` (Part 3), `recursion_intro.py`
(Part 4).

---

## Part 1 — Stack Frame Visualization (30)

### Exercise 1.1 — The fundamental call stack

1. **Three** frames exist while `square(3)` runs.
2. Bottom to top: **`<module>` → `sum_of_squares` → `square`**. (The module frame is real and holds
   `answer`; students often forget it.)
3. When `square(3)` returns, the value `9` goes to the **point of call** — it becomes the value of the
   expression `square(a)`, which is bound to `sq_a` in `sum_of_squares`'s frame. It does not go into
   `square`'s frame, which is destroyed at that instant.
4. **No.** `x` exists only in `square`'s own frame. Each call gets a **fresh frame** with its own `x` —
   which is exactly why recursion works at all.
5. After `sum_of_squares` returns, `sq_a` and `sq_b` are **destroyed** with its frame. Only the
   returned value survives, bound to `answer` in the module frame.

*A frame is created per **call**, not per function.*

### Exercise 1.3 — The mutable default trap

1. It prints `['apple', 'banana', 'cherry']` **three times** — `r1 is r2 is r3` is `True`; all three
   names label the **same** list object.
2. The default `[]` is created **when the `def` statement executes** (function-definition time), not at
   call time.
3. **Exactly once**, for the life of the program. You can see it stored on the function itself:
   `add_item.__defaults__` shows `(['apple', 'banana', 'cherry'],)`.

4. Corrected version:

```python
def add_item(item, collection=None):
    if collection is None:
        collection = []
    collection.append(item)
    return collection
```

(Use `is None`, not `if not collection` — the latter would wrongly replace a caller's *deliberately*
empty list.)

### Exercise 1.5 — Return values vs. print

1. `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`. `double_print` prints `10`
   and then falls off the end, returning `None`; `None + 1` is a type error. (Note the `10` **is**
   printed before the error — the side effect happens, but the value does not exist.)
2. `double_return(5)` returns `10`, so `b == 11`.
3. Because **only a returned value can participate in an expression**. Printing sends characters to a
   stream and produces no value for the caller; the diagnostic question is *"could I assign the result
   to a variable and use it later?"*

_Marks: 30 / 30_

---

## Part 2 — Scope Bug Hunt (20)

| Case | What happens | Why | Fix |
|------|--------------|-----|-----|
| **1** `accumulate` | `UnboundLocalError` | `running_total += n` **assigns**, so `running_total` is local to the whole body (LEGB); the read finds no local value | `global running_total`, or (better) pass the total in and return the new one |
| **2** `append_copy` | `original` becomes `[1, 2, 3, 4]` | `lst` and `original` name one list; `append` **mutates** it | `return lst + [item]` builds a new list |
| **3** `safe_max` | **no bug** | `default=0` is an **immutable** `int`; a shared default is only dangerous when it is **mutable and mutated** (`[]`) | — (the explanation earns the points) |
| **4** `analyze` | works here, but `len` is now a local `int` | the local name **shadows the built-in** inside `analyze`; any `len(...)` here would raise `TypeError: 'int' object is not callable` | rename to `count` |

Fixed code in `scope_bugs.py` (all its asserts pass).

_Marks: 20 / 20_

---

## Part 3 — Function Design Workshop (35) — `text_statistics.py`

Every function has a full docstring; helpers are prefixed with `_`; `display_report` is the only
printing function and calls the others (no re-implemented logic). `run_tests()` passes and the report
prints:

```
==================================================
TEXT ANALYSIS REPORT
==================================================
  Word count:          29
  Sentence count:      4
  Avg word length:     4.55
  Longest word:        vexingly
  Reading level:       Elementary
==================================================
```

`average_word_length("")` returns `0.0` rather than raising `ZeroDivisionError`.

_Marks: 35 / 35_

---

## Part 4 — Recursion First Look (15) — `recursion_intro.py`

```python
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

def sum_digits(n):
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)
```

All handout asserts pass (`power(3, 4) == 81`, `sum_digits(9999) == 36`).

**Python Tutor task:** at its deepest, `factorial(5)` has **7 frames** — the module frame plus the six
calls `n = 5, 4, 3, 2, 1, 0`. With Python's default recursion limit of **1000**, each call adds one
frame, so `factorial(n)` works up to about **n = 998**; beyond that it raises `RecursionError`.

_Marks: 15 / 15_

---

## Reflection

**Q1.** Python evaluates default-argument expressions **once**, when the `def` statement runs and
creates the function object — not on each call. The resulting object is stored on the function (in
`__defaults__`) and reused by every call that omits the argument. Because a `def` is an executable
statement, it runs once at definition time, so a mutable default like `[]` persists and accumulates
changes across calls.

**Q2.** Keeping `display_report` as the only printer makes every other function **pure**: it returns a
value instead of emitting text, so it can be tested with a plain `assert` (no capturing of stdout),
reused by other callers, or wired to a different output (a file, a web page) without change. If every
function printed its own output, the results would be interleaved and impossible to test or reuse, and
computation would be tangled with presentation.

**Q3.** The **recursive** version is preferable when the problem is naturally recursive and shallow —
tree or graph traversal, parsing, or divide-and-conquer — where the recursive form reads closer to the
definition. The **iterative** version is preferable when the depth could be large (recursion would hit
the ~1000-frame limit and raise `RecursionError`), when performance/memory matters (calls have
overhead), or when a simple loop is simply clearer.

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-23 |

**Feedback:**
Full marks. Part 1 correctly counts three frames and names them, traces the return value to the point
of call, and explains the per-call frame; the mutable-default trap is diagnosed (default built once at
`def` time, shared via `__defaults__`) and fixed with `None`; return-vs-print gives the exact
`NoneType` `TypeError` and `b == 11`. Part 2 finds all three bugs plus the trick no-bug case, each
with the right cause and fix. `text_statistics.py` implements every function with docstrings, keeps
printing in `display_report` alone, avoids the empty-text `ZeroDivisionError`, and reproduces the
report. `recursion_intro.py` passes; 7 frames for `factorial(5)` is correct.
