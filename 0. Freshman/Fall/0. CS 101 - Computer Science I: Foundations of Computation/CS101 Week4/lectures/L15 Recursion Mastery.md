# CS 101 · Lecture 15 (Week 4, Lecture 3)
## Recursion: Stack Depth, Tail Calls, and Design Mastery

**Week 4 · Friday**
*"Recursion requires trusting the inductive hypothesis — and that trust is earned by proof, not intuition." — CS 101*

**Date:** Friday 18 September 2026 · 09:00–09:50 · Week 4

---

## 0. Week Synthesis

Wednesday: what recursion is and why it's correct (induction).
Thursday: recursion trees, merge sort, tree recursion, iterative conversion.
Today: the practical constraints (stack depth, Python's limit), tail recursion in depth, the five recursive design patterns, and a complete design walkthrough that connects everything.

---

## 1. The Call Stack Revisited: Why Depth Matters

Each recursive call pushes a frame onto the call stack. The frame holds:
- All local variables
- The return address
- A reference to the calling frame

In CPython, a default stack frame is roughly **1–3 KB**. Python's default recursion limit is **1,000 frames**. So the recursive call stack consumes at most ~3 MB — well within typical memory limits.

The limit exists not because of memory, but because:
1. **Infinite recursion detection**: a limit of 1,000 catches infinite loops early, before exhausting all memory
2. **Traceback quality**: deep stacks produce unreadable tracebacks
3. **Deliberate design**: Guido van Rossum explicitly rejected tail call optimization to preserve tracebacks

```python
import sys

# Check the limit:
print(sys.getrecursionlimit())    # 1000

# Change it (use with caution):
sys.setrecursionlimit(10000)

# What the error looks like:
def too_deep(n):
    return too_deep(n + 1)

try:
    too_deep(0)
except RecursionError as e:
    print(f"RecursionError: {e}")
    # RecursionError: maximum recursion depth exceeded
```

**When to raise the limit:** Almost never. If your recursive function legitimately needs more than 1,000 frames, convert it to iterative with an explicit stack instead — it will also be faster.

---

## 2. Tail Recursion: The Complete Story

A function is **tail recursive** if its recursive call is in **tail position** — the very last operation, with no work remaining after the call returns.

```python
# NOT tail recursive — multiplication happens AFTER the call:
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
    # After factorial(n-1) returns, we still need to multiply by n.
    # The frame must be kept alive to hold n.

# Tail recursive — accumulator carries the state:
def factorial_tr(n, acc=1):
    if n == 0:
        return acc
    return factorial_tr(n - 1, n * acc)
    # The recursive call IS the return value.
    # No computation happens after it returns.
    # The frame could theoretically be discarded.
```

In a language with **tail call optimization (TCO)** — Scheme, Haskell, Erlang, Scala — the tail-recursive version runs in O(1) stack space. The compiler reuses the current frame instead of pushing a new one.

Python **does not** implement TCO. Both versions use O(n) stack frames in Python.

**Simulating TCO in Python with a trampoline:**

```python
def trampoline(f):
    """Execute a trampolined recursive function in O(1) stack space."""
    def trampolined(*args):
        result = f(*args)
        while callable(result):   # if result is a thunk (unevaluated call)
            result = result()     # evaluate it
        return result
    return trampolined


def factorial_thunk(n, acc=1):
    """Trampolined factorial — returns thunks instead of calling recursively."""
    if n == 0:
        return acc
    return lambda: factorial_thunk(n - 1, n * acc)   # return a thunk


safe_factorial = trampoline(factorial_thunk)
print(safe_factorial(10000))   # Computes 10000! in O(1) stack space
```

The trampoline drives the computation from a `while` loop instead of the call stack. Each "recursive call" is deferred as a lambda (a thunk) and invoked by the trampoline. This is purely for demonstration — in practice, just write an iterative loop.

---

## 3. Five Recursive Design Patterns

After studying many recursive algorithms, five patterns emerge. Recognizing which pattern applies is the key skill.

### Pattern 1: Linear Decrease

**Structure:** One recursive call on input reduced by a fixed amount (usually n-1).
**Complexity:** O(n) calls.
**Examples:** factorial, sum, reverse, sequential search.

```python
def my_sum(lst):
    if not lst: return 0
    return lst[0] + my_sum(lst[1:])
```

**Rule of thumb:** If you'd write a `while` loop with a counter, this is the iterative equivalent. Use iteration instead unless you need the recursive style for clarity.

### Pattern 2: Binary Decrease (Exponential)

**Structure:** Two recursive calls, each on n-1 (or similar).
**Complexity:** O(2^n) calls — dangerous.
**Examples:** Naïve Fibonacci, naïve subset enumeration.

```python
def fib_naive(n):
    if n <= 1: return n
    return fib_naive(n-1) + fib_naive(n-2)
```

**Rule of thumb:** Always suspect exponential blowup when you make two recursive calls on input that decreases by 1. Add memoization or convert to dynamic programming.

### Pattern 3: Divide and Conquer (Logarithmic Depth)

**Structure:** Two recursive calls, each on input of size n/2.
**Complexity:** Depth O(log n); total work depends on combine step.
**Examples:** Merge sort O(n log n), binary search O(log n), exponentiation O(log n).

```python
def fast_power(base, exp):
    """Compute base**exp in O(log exp) multiplications."""
    if exp == 0: return 1
    if exp % 2 == 0:
        half = fast_power(base, exp // 2)
        return half * half           # only ONE recursive call!
    return base * fast_power(base, exp - 1)
```

**Rule of thumb:** Cutting the problem in half → logarithmic depth. This is almost always fast enough for any reasonable input size.

### Pattern 4: Tree Recursion (Structural)

**Structure:** One call per child in a recursive data structure.
**Complexity:** O(n) where n is the number of nodes.
**Examples:** All tree operations, directory traversal, expression evaluation.

```python
def tree_depth(node):
    if node is None: return 0
    return 1 + max(tree_depth(node.left), tree_depth(node.right))
```

**Rule of thumb:** The structure of the recursion mirrors the structure of the data. If the data is a tree, the recursion is tree-shaped — one call per subtree.

### Pattern 5: Backtracking (Combinatorial)

**Structure:** Try an option; if it fails, undo it and try the next one.
**Complexity:** Worst case O(b^d) where b = branching factor, d = depth. Pruning reduces this dramatically.
**Examples:** Maze solving, N-Queens, Sudoku solver, constraint satisfaction.

```python
def solve_maze(maze, row, col, path):
    """Find a path through a maze from (row,col) to the exit."""
    rows, cols = len(maze), len(maze[0])

    # Base cases:
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return False    # out of bounds
    if maze[row][col] == 'X':
        return False    # wall
    if maze[row][col] == 'E':
        path.append((row, col))
        return True     # found exit!
    if maze[row][col] == 'V':
        return False    # already visited

    # Mark as visited (choose):
    maze[row][col] = 'V'
    path.append((row, col))

    # Try all four directions (explore):
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        if solve_maze(maze, row+dr, col+dc, path):
            return True

    # Undo (unchoose — backtrack):
    maze[row][col] = ' '
    path.pop()
    return False
```

**Rule of thumb:** If you find yourself making a choice, recursing, then "undoing" the choice on failure — you're backtracking. This pattern appears constantly in AI and constraint satisfaction.

---

## 4. The Choose-Explore-Unchoose Framework

Backtracking recursion always follows this structure:

```
for each option:
    CHOOSE the option (modify state)
    EXPLORE (recurse)
    if exploration succeeded: return success
    UNCHOOSE (restore state — backtrack)
return failure
```

```python
def permutations(lst):
    """Return all permutations of lst."""
    if len(lst) <= 1:
        return [lst[:]]

    result = []
    for i in range(len(lst)):
        # CHOOSE: put element i first
        lst[0], lst[i] = lst[i], lst[0]

        # EXPLORE: permute the rest
        for perm in permutations(lst[1:]):
            result.append([lst[0]] + perm)

        # UNCHOOSE: restore the swap
        lst[0], lst[i] = lst[i], lst[0]

    return result


assert sorted(permutations([1,2,3])) == sorted([
    [1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]
])
```

---

## 5. A Complete Design Walkthrough: Recursive Power Set

The **power set** of a set S is the set of all subsets of S.
- Power set of {1,2,3} = {∅, {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}}
- A set of size n has 2^n subsets.

**Step 1: Identify the recursive structure.**
Every subset of {1, 2, ..., n} either:
- Contains element n, OR
- Does not contain element n

So: `power_set({1,...,n})` = all subsets of `{1,...,n-1}` + all those subsets with n added.

**Step 2: Identify the base case.**
`power_set({})` = `{∅}` — the empty set has exactly one subset: itself (the empty set).

**Step 3: Write the recursive case.**
```
power_set(S) = power_set(S without last element)
             ∪ {subset ∪ {last element} : subset ∈ power_set(S without last element)}
```

**Step 4: Implement.**

```python
def power_set(lst):
    """
    Return a list of all subsets of lst (as lists).

    Base case: power_set([]) = [[]]
    Inductive step: power_set(lst) = power_set(lst[:-1])
                                   + [s + [lst[-1]] for s in power_set(lst[:-1])]

    Correctness: by induction. Base case: only subset of [] is []. ✓
    Step: assuming power_set(lst[:-1]) returns all 2^(n-1) subsets of the
    first n-1 elements, power_set(lst) returns each of those subsets
    (without lst[-1]) and each with lst[-1] appended — exactly 2^n subsets. ✓
    """
    if not lst:
        return [[]]                        # base case: one subset — the empty set

    rest = power_set(lst[:-1])             # all subsets of all-but-last
    with_last = [s + [lst[-1]] for s in rest]  # add last element to each
    return rest + with_last


ps = power_set([1, 2, 3])
assert len(ps) == 8        # 2^3 = 8 subsets
assert [] in ps             # empty set is a subset
assert [1,2,3] in ps        # full set is a subset
print(power_set([1, 2, 3]))
# [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
```

**Step 5: Verify complexity.**
- Recursion tree: depth n, each level doubles the number of subsets.
- Total subsets generated: 2^n (unavoidable — output size is 2^n).
- Total work: O(2^n) — optimal, since we must produce 2^n subsets.

---

## 6. Recursion Anti-Patterns

### Anti-pattern 1: Missing base case

```python
def countdown(n):
    print(n)
    countdown(n - 1)    # No base case → RecursionError
```

Fix: always write the base case first.

### Anti-pattern 2: Not making progress

```python
def broken(n):
    if n == 0:
        return 0
    return broken(n)    # same input! → infinite recursion
```

Fix: the recursive call must use a strictly smaller input.

### Anti-pattern 3: Exponential without memoization

```python
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)   # O(2^n) — never call with n > 35
```

Fix: add memoization or use dynamic programming.

### Anti-pattern 4: Slicing strings/lists in every call

```python
def sum_recursive(lst):
    if not lst: return 0
    return lst[0] + sum_recursive(lst[1:])   # lst[1:] creates a NEW list each time
```

`lst[1:]` is O(n) — creating a slice of length n-1. This makes the total work O(n²).

Fix: pass indices instead of creating new lists:

```python
def sum_recursive(lst, i=0):
    if i == len(lst): return 0
    return lst[i] + sum_recursive(lst, i + 1)   # O(1) per call, O(n) total
```

### Anti-pattern 5: Using global variables to communicate between recursive calls

```python
count = 0   # global — fragile!

def count_nodes(tree):
    global count
    if tree is None: return
    count += 1
    count_nodes(tree.left)
    count_nodes(tree.right)
```

Fix: return the count (pure function):

```python
def count_nodes(tree):
    if tree is None: return 0
    return 1 + count_nodes(tree.left) + count_nodes(tree.right)
```

---

## 7. Recursion and Iteration: Choosing Wisely

| Situation | Prefer |
|-----------|--------|
| Linear problem (sum, factorial, search) | **Iteration** — simpler, faster, no stack limit |
| Tree structure | **Recursion** — mirrors structure, clearest |
| Divide and conquer | **Recursion** — natural expression |
| Backtracking | **Recursion** — choose/explore/unchoose is clearest |
| Depth > 900 in Python | **Iteration** with explicit stack |
| Already have a loop that uses a stack | Consider **recursion** for clarity |

---

## 8. Summary of Week 4

| Concept | What it is | When it applies |
|---------|-----------|----------------|
| Three laws | Base case; progress; self-call | Every recursive function |
| Inductive proof | Base + step → correct for all inputs | Correctness argument |
| Recursion tree | Visualizes calls; count for complexity | Analyzing runtime |
| Linear recursion | One call, n-1 depth | Simple problems; use loop instead |
| Binary recursion | Two calls, exponential — beware | Fibonacci, subsets |
| Divide and conquer | Two calls on n/2 — logarithmic | Merge sort, binary search |
| Tree recursion | One call per child | All tree operations |
| Backtracking | Choose/explore/unchoose | Constraint satisfaction |
| Tail recursion | Last action is the call | Enable TCO (not in Python) |
| Memoization | Cache subproblem results | Fix exponential recursion |
| Iterative conversion | Explicit stack simulates call stack | Deep recursion in Python |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Trace the power-set function on `[1, 2, 3]` and give the output **in the order the function actually produces it**.

```python
def powerset(xs):
    if not xs:
        return [[]]
    rest = powerset(xs[1:])
    return rest + [[xs[0]] + r for r in rest]
```

**2. (Explain.)** These two backtracking functions differ by four characters. One returns six permutations and the other returns six empty lists. Explain the mechanism precisely.

```python
# A: out.append(cur)
# B: out.append(cur[:])
def perms(xs):
    out, cur = [], []
    def go(rem):
        if not rem:
            out.append(cur)      # or cur[:]
            return
        for i, v in enumerate(rem):
            cur.append(v)
            go(rem[:i] + rem[i+1:])
            cur.pop()
    go(xs)
    return out
```

**3. (Build.)** Write `subsets_summing_to(xs, target)` using choose-explore-unchoose, returning every subset whose sum equals the target. Then add one pruning rule and say what it buys.

**4. (Stretch.)** §6 lists recursion anti-patterns. This function has three separate problems. Find all three.

```python
def find(xs, target, seen=[]):
    if xs == []:
        return False
    if xs[0] == target:
        seen.append(target)
        return True
    return find(xs[1:], target)
```


### Answers

**1.** `[[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]]`

Working bottom-up: `powerset([])` = `[[]]`; `powerset([3])` = `[[], [3]]`; `powerset([2, 3])` = `[[], [3]]` + `[[2], [2, 3]]`; and the top level prepends `1` to each of those four.

The order is not alphabetical or by size — it is **every subset without the first element, then every subset with it**, applied recursively. Reading the output as binary tells you why: index 0 = `000`, index 1 = `001` = {3}, index 2 = `010` = {2}, index 3 = `011` = {2,3}, index 4 = `100` = {1}. The function is enumerating bit patterns, with bit *i* deciding whether element *i* is included.

That correspondence is the reason a power set has exactly 2ⁿ members, and it gives you the iterative version for free: loop `mask` from 0 to 2ⁿ−1 and select the elements whose bit is set.

**2.** **A returns `[[], [], [], [], [], []]`. B returns the six permutations correctly.**

`cur` is a single list object reused across the whole search — that is the point of choose-explore-unchoose, and it is what makes backtracking cheap. `out.append(cur)` appends a **reference** to that one object, not a snapshot. So `out` ends up holding six references to the same list, and by the time the search finishes, every `cur.append` has been undone by a matching `cur.pop`, leaving that list empty. All six entries show it empty because all six *are* it.

`cur[:]` takes a shallow copy at the moment of recording, freezing the state. Any of `list(cur)`, `cur.copy()`, or `tuple(cur)` works identically.

This is the single most common backtracking bug, and its signature is unmistakable: the right *number* of results, all identical, usually all empty. Whenever you record a mutable accumulator inside a search, **copy it at the moment of recording**.

**3.**

```python
def subsets_summing_to(xs, target):
    out, cur = [], []
    def go(i, remaining):
        if remaining == 0:
            out.append(cur[:])   # copy!
            return
        if i == len(xs) or remaining < 0:
            return
        cur.append(xs[i]);  go(i + 1, remaining - xs[i]);  cur.pop()   # choose / explore / unchoose
        go(i + 1, remaining)                                          # skip xs[i]
    go(0, target)
    return out
```

The pruning rule is **`remaining < 0`**: once the running total has overshot, no further element can bring it back, so the entire subtree below that point is abandoned unexplored. For all-positive `xs` this is sound and often cuts the search dramatically.

What it buys is a **constant-factor-to-large speedup on typical inputs, but no change to the worst-case bound** — which stays O(2ⁿ), since an input where nothing overshoots (all values small relative to the target) prunes nothing. That gap between typical and worst case is characteristic of backtracking: the bound is exponential, and pruning is what makes it usable anyway.

Sorting `xs` descending first strengthens the pruning further, because large values trigger the overshoot test earlier. Note the rule is **unsound if `xs` may contain negatives** — a later negative could bring an overshot total back to the target.

**4.** 1. **Mutable default argument.** `seen=[]` is created once at `def` time and shared by every call, so results accumulate across unrelated invocations. It is also never passed on to the recursive call, so it does not even do what it appears to.

2. **O(n²) slicing.** `xs[1:]` copies the remainder of the list at every level, so a linear search costs quadratic time and Θ(n²) total allocation. Pass an index instead: `find(xs, target, i + 1)` with `if i == len(xs)`.

3. **Recursion where iteration belongs.** This is a linear scan with no branching and no combining step — the natural expression is a `for` loop, which is clearer *and* immune to the 1000-frame limit that makes this version crash on any list of moderate size.

A fourth, subtler point: `if xs == []` compares against a freshly built list where `if not xs` would do, and it silently fails for any non-list sequence. The whole function should be:

```python
def find(xs, target):
    return target in xs
```

which is the real lesson of §6 — the best fix for a badly written recursion is often not a well-written recursion.



---

## Reading

- **Guttag, Ch. 4.3** — Recursion (finish)
- **Guttag, Ch. 3.3** — Bisection search (connects recursion to approximation)

---

*CS 101 · Week 4 · Lecture 15 (Fri) · © CSE Department*
