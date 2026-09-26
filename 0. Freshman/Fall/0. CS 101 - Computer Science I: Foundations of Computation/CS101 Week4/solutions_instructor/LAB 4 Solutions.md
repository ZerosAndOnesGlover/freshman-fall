# CS 101 · Week 4
## LAB 4 Solutions (INSTRUCTOR ONLY)

> Lab sat Tuesday 27 October 2026. **All code below was executed and all stated outputs are real.**
> Students answer the "how does it grow" questions in words ("doubles when n rises by 1", "one more
> call when the list doubles"); the Big-O forms below are for the instructor — Big-O is taught in Week 6.

---

## Part 1 — Recursion Tree Drawing

### Exercise 1.1 — `count_up(5)`

Chain of calls: `count_up(5) → count_up(4) → count_up(3) → count_up(2) → count_up(1) → count_up(0)`

- **Nodes: 6** (arguments 5 down to 0 inclusive — n + 1 for input n).
- **Depth: 6.**
- **O(n) time, O(n) space** — the space is the call stack, and it is *not* O(1) even though the
  function stores nothing. This is linear recursion: one call per level, no branching.

### Exercise 1.2 — `fib(5)`

- **Nodes: 15.**
- **`fib(2)` is computed 3 times. `fib(1)` is computed 5 times.**

Full call census, verified by instrumenting the function:

| Argument | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Times called | 3 | **5** | **3** | 2 | 1 | 1 |

- **O(φⁿ) ≈ O(1.618ⁿ)** — exponential.

The closed form is **nodes = 2·fib(n+1) − 1**: here `fib(6) = 8`, and 2(8) − 1 = **15** ✓. The
tree has exactly `fib(n)` leaves, and a binary tree in which every internal node has two children
has one fewer internal node than leaves.

**The repeated work is the entire point.** `fib(1)` being computed 5 times for an input as small as
5 is what makes memoisation collapse this to Θ(n).

### Exercise 1.3 — `binary_search([1..8], 3, 0, 7)`

Searching for **3** (present): calls at ranges `[0,7] → [0,2] → [0,0]`, finds index 2.
**3 nodes, depth 3.**

Searching for a **missing** element (the worst case the question asks for):
**5 nodes, depth 5** on a list of length 8.

| List length n | Max depth |
|---|---|
| 8 | 5 |
| 16 | 6 |
| n | **⌊log₂ n⌋ + 2** |

- **O(log n).**

The depth exceeds ⌈log₂ 8⌉ = 3 because the recursion continues until `lo > hi` — the final call on
an *empty* range is what returns −1, and the ranges shrink 8 → 4 → 2 → 1 → 0. Students who answer
"3" have counted only the halvings and forgotten the terminating call. **Accept either if their
reasoning is stated**, but the measured node count for a missing element is 5.

### Exercise 1.4 — `tree_sum` on the given tree

```
        5
       / \
      3   8
     / \   \
    1   4   9
```

- **Sum = 30.**
- **Total calls: 13** — 6 on real nodes, **7 on `None`**.
- For a binary tree with n nodes, there are exactly **n + 1** `None`-calls. Here 6 + 1 = 7 ✓.

The n + 1 property is worth stating: every node has 2 child slots, giving 2n slots; n − 1 of them
hold real nodes (every node except the root has exactly one parent), so 2n − (n − 1) = **n + 1**
are empty.

- **O(n)** — each node visited once.

---

## Part 2 — Reference Implementations

*(Revised 2026-09-26: Exercises 2.1 `fast_power` and 2.2 `merge_sort` are no longer in the lab — they are
Problem Set 4 B3 — and neither is reflection Q3. Their notes below now apply to marking PS 4.)*

All verified against the docstring examples.

```python
def fast_power(base, exp):
    """base ** exp in O(log exp) via exponentiation by squaring."""
    if exp == 0:
        return 1
    half = fast_power(base, exp // 2)          # computed ONCE
    return half * half * base if exp % 2 else half * half

# fast_power(2, 10) -> 1024   ✓
# fast_power(2, 0)  -> 1      ✓
# fast_power(3, 4)  -> 81     ✓


def sum_fast(lst, i=0):
    """Sum via index recursion — O(n) time, O(n) stack, no slicing."""
    if i == len(lst):
        return 0
    return lst[i] + sum_fast(lst, i + 1)


def reverse_fast(lst, i=None, result=None):
    """Reverse via index recursion, accumulating into result — O(n)."""
    if i is None:
        i = len(lst) - 1
    if result is None:
        result = []
    if i < 0:
        return result
    result.append(lst[i])
    return reverse_fast(lst, i - 1, result)

# reverse_fast([1,2,3,4]) -> [4, 3, 2, 1]   ✓
# reverse_fast([])        -> []             ✓  (i starts at -1, base case fires immediately)


def count_occurrences(lst, target, i=0):
    """Count target in lst by index recursion."""
    if i == len(lst):
        return 0
    return (1 if lst[i] == target else 0) + count_occurrences(lst, target, i + 1)

# count_occurrences([1,2,3,2,1], 2) -> 2   ✓
```

> **`fast_power` must bind `half` to a variable.** Writing
> `return fast_power(base, exp//2) * fast_power(base, exp//2)` looks identical and is **O(exp)**,
> because the two calls are evaluated separately — the same overlapping-subproblem trap as `fib`,
> in a place where it is easy to miss. Check this line specifically; it is the point of the
> exercise.
>
> **`reverse_fast` uses two `None` sentinels**, not `result=[]`. The mutable-default bug from
> Lab 3 would make a second call return the first call's output appended to the new one. A student
> who wrote `result=[]` will pass a single test and fail on the second invocation — run it twice.

---

## Part 3 — The Slicing Anti-Pattern

`sum_slow(lst)` written as `lst[0] + sum_slow(lst[1:])` is **O(n²) time and O(n²) total
allocation**, because `lst[1:]` copies the remaining n−1 elements at every level: n + (n−1) + … + 1
copies.

`sum_fast(lst, i)` passes an **index** instead, touching each element once — **O(n) time**, with
O(n) stack in both cases.

The rule: **never slice to recurse.** Pass bounds. The same applies to strings, where `s[1:]` is
equally a copy, and to the `find` anti-pattern in L15 §6.

---

## Exercise 2.4 — `fib_counted`

Measured:

| n | fib(n) | calls |
|---|---|---|
| 5 | 5 | 15 |
| 10 | 55 | 177 |
| 15 | 610 | 1973 |
| 20 | 6765 | 21891 |
| 25 | 75025 | 242785 |

The count grows by about **11×** each time `n` rises by 5 (φ⁵ ≈ 11.1). Q1: the same sub-problems
are recomputed — `fib(2)` alone is computed `fib(n−1)` times — and **memoisation** (L14's closing
section) would compute each once. Students should *name* it, not implement it: dictionaries are Week 8.

---

## Marking Scheme

| Part | Points | Notes |
|---|---|---|
| 1 | 30 | 7.5 per tree: correct shape, correct counts, a sensible growth statement |
| 2 | 45 | tests pass (35); the `fib_counted` table matches the one above (10) |
| 3 | 15 | `slicing_fix.py` runs (5); `count_occurrences` index-based, no slicing (10) |
| Reflection | 10 | Q2's induction must show both base case and step |

---

*CS 101 · Week 4 · Lab 4 Solutions · Instructor only*
