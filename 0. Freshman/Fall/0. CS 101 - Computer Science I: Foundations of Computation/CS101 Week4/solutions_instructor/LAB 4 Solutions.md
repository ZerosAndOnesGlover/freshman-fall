# CS 101 · Week 4
## LAB 4 Solutions (INSTRUCTOR ONLY)

> **All code below was executed and all stated outputs are real.** Where a benchmark appears,
> the absolute timings are machine-specific — grade the *ratios* and the conclusions, never the
> raw milliseconds.

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

## Part 4 — N-Queens

```python
def is_safe(board, row, col):
    """board[r] = column of the queen in row r; rows above `row` are filled."""
    for r in range(row):
        if board[r] == col or abs(board[r] - col) == row - r:
            return False
    return True


def solve_nqueens(n, row=0, board=None, solutions=None):
    if board is None:
        board = [-1] * n
    if solutions is None:
        solutions = []
    if row == n:
        solutions.append(board[:])          # COPY — see below
        return solutions
    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col                # choose
            solve_nqueens(n, row + 1, board, solutions)   # explore
            board[row] = -1                 # unchoose
    return solutions
```

Verified solution counts:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Solutions | 1 | 0 | 0 | **2** | 10 | 4 | 40 | **92** |

These match the known values; **n = 2 and n = 3 having zero solutions is a correct result**, not a
bug, and is a good sanity check that the student's `is_safe` is not too permissive.

### The three things that go wrong

1. **`solutions.append(board)` without `[:]`.** Every recorded solution then aliases the one shared
   `board`, and since backtracking restores it to all `-1`, the output is the right *number* of
   solutions, all identical and all empty. **Symptom: 92 identical rows for n = 8.** This is the
   single most common backtracking bug.
2. **Missing the unchoose.** Without `board[row] = -1`, stale queens from abandoned branches remain
   and `is_safe` rejects valid positions — the count comes out too low.
3. **Diagonal test wrong.** `abs(board[r] - col) == row - r` is the correct condition. Writing
   `abs(board[r] - col) == abs(row - r)` is equivalent here (since `r < row`) but `board[r] - col
   == row - r` without the `abs` checks only one diagonal and yields inflated counts.

The one-queen-per-row encoding (`board[r]` = column) makes row conflicts *structurally impossible*,
which is why `is_safe` only tests columns and diagonals. Reward students who articulate that the
representation eliminated a whole class of check.

---

## Marking Scheme

The lab is checkoff-graded against the criteria on the handout. Within each part:

- **Method (≈60%).** Correct approach, required loop/structure type actually used, edge cases
  considered, invariants stated where the handout asks for them.
- **Result (≈40%).** Code runs, produces the specified output, and the written answers are correct.

**Carry-through.** A wrong helper that is then used correctly downstream costs marks once.

**Watch for the two failure modes that matter:**
1. Code that produces the right answer for the sample input and is wrong in general — always run
   the edge cases listed under each exercise.
2. Written answers that restate the observation instead of explaining it. "0.1 + 0.2 isn't 0.3
   because floats are imprecise" earns nothing; the answer must reach binary representation.

---

*CS 101 · Week 4 · Lab Solutions · Instructor Copy · © CSE Department*
