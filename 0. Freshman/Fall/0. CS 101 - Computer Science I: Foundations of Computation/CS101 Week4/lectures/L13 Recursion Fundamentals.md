# CS 101 · Lecture 13 (Week 4, Lecture 1)
## Recursion: Thinking in Self-Reference

**Week 4 · Wednesday**
*"To understand recursion, you must first understand recursion." — anonymous*
*"Recursion is not a trick. It is a mathematical concept." — CS 101*

**Date:** Wednesday 16 September 2026 · 09:00–09:50 · Week 4

---

## 0. What Recursion Actually Is

Week 3 ended with a preview: a function that calls itself. This week we make that idea rigorous, powerful, and practical.

Recursion is not a programming trick. It is a **mathematical concept** — the idea of defining something in terms of a simpler version of itself. This concept predates computers entirely:

- The Fibonacci numbers: F(n) = F(n-1) + F(n-2)
- The factorial: n! = n × (n-1)!
- The natural numbers: 0 is a natural number; if n is a natural number, so is n+1

When you write a recursive function, you are implementing a mathematical inductive definition directly in code. The principle of **mathematical induction** — which you study in MATH 151 — is precisely the formal justification that recursive definitions are well-founded.

---

## 1. The Three Laws of Recursion

Every correct recursive function obeys three laws:

**Law 1: A recursive function must have a base case.**
The base case is an input small enough to solve directly, without recursion. It stops the chain of calls.

**Law 2: A recursive function must change its state toward the base case.**
Each recursive call must make the problem *strictly smaller* (or simpler) than the current call. If it doesn't, the recursion never terminates.

**Law 3: A recursive function must call itself.**
This sounds trivial, but it means: the recursive call must be to the *same function*, on a *simpler* version of the problem.

```python
def factorial(n):
    # Law 1: base case
    if n == 0:
        return 1
    # Law 2: n-1 is strictly smaller than n
    # Law 3: calls factorial (itself) on n-1
    return n * factorial(n - 1)
```

If any law is violated, the function is either incorrect or doesn't terminate.

---

## 2. Recursion and Mathematical Induction: The Connection

Mathematical induction proves a property P(n) holds for all non-negative integers:
1. **Base case:** prove P(0) is true
2. **Inductive step:** prove that if P(k) is true, then P(k+1) is true

Recursive function correctness follows the same structure:
1. **Base case:** the function returns the correct value for the smallest input
2. **Inductive step:** *assuming* the recursive call returns the correct value for n-1, show the function returns the correct value for n

```python
def factorial(n):
    """Compute n! for non-negative integer n."""
    # Proof of correctness by induction:
    #
    # Base case (n=0): returns 1. Correct: 0! = 1 by definition.
    #
    # Inductive step: assume factorial(n-1) = (n-1)! (inductive hypothesis).
    # Then: n * factorial(n-1) = n * (n-1)! = n!  ✓
    #
    # By induction, factorial(n) = n! for all n >= 0.

    if n == 0:
        return 1
    return n * factorial(n - 1)
```

This is not hand-waving — it is a complete proof that the function is correct. The inductive hypothesis is exactly the "trust the recursion" step.

---

## 3. Drawing Recursion Trees

A recursion tree shows every function call as a node, with edges to the calls it makes.

```
factorial(4)
│
└── 4 * factorial(3)
         │
         └── 3 * factorial(2)
                  │
                  └── 2 * factorial(1)
                           │
                           └── 1 * factorial(0)
                                    │
                                    └── returns 1   ← base case
                           returns 1*1 = 1
                  returns 2*1 = 2
         returns 3*2 = 6
returns 4*6 = 24
```

Key observations:
- The tree grows **downward** (each call on a smaller input)
- The **base case** is always a leaf (no children)
- Values are computed **bottom-up** (leaves return first, root returns last)
- The call stack at the deepest point has as many frames as the tree's depth

---

## 4. The Fibonacci Sequence: Naive Recursion

The Fibonacci sequence is defined recursively:
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) for n ≥ 2

The direct implementation:

```python
def fib(n):
    """Return the nth Fibonacci number."""
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)
```

This is mathematically beautiful — it mirrors the definition exactly. Let's draw the recursion tree for `fib(5)`:

```
                    fib(5)
                   /      \
              fib(4)        fib(3)
             /      \       /    \
         fib(3)  fib(2) fib(2) fib(1)
         /   \   /   \   /   \
      fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
      /   \
   fib(1) fib(0)
```

Count the nodes: for `fib(5)`, there are **15 function calls**. For `fib(n)`, the number of calls is approximately O(2^n) — **exponential**. `fib(50)` would require over a trillion calls.

**Why?** Because `fib(3)` is computed twice, `fib(2)` is computed three times, `fib(1)` is computed five times. The same subproblems are solved over and over. This is **overlapping subproblems** — the defining characteristic of problems that call for **dynamic programming** (Week 7 in CS 102).

The fix — **memoization** — stores results to avoid recomputation:

```python
def fib_memo(n, memo=None):
    """Return the nth Fibonacci number, with memoization."""
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

With memoization, each subproblem is solved exactly once: O(n) calls instead of O(2^n). We'll study this transformation formally in CS 102.

---

## 5. Recursive List Processing

Recursion is natural for list problems: a list is either empty, or it has a first element and a rest (which is itself a list).

```python
# Pattern:
def recursive_list_function(lst):
    if not lst:           # base case: empty list
        return base_value
    first = lst[0]
    rest  = lst[1:]
    # combine first with the result of recursing on rest
    return combine(first, recursive_list_function(rest))
```

### Examples:

```python
def recursive_sum(lst):
    """Sum all elements in a list."""
    if not lst:
        return 0
    return lst[0] + recursive_sum(lst[1:])

def recursive_max(lst):
    """Return the maximum element of a non-empty list."""
    assert lst, "Cannot take max of empty list"
    if len(lst) == 1:
        return lst[0]
    rest_max = recursive_max(lst[1:])
    return lst[0] if lst[0] > rest_max else rest_max

def recursive_reverse(lst):
    """Return a new list with elements in reverse order."""
    if not lst:
        return []
    return recursive_reverse(lst[1:]) + [lst[0]]

def recursive_contains(lst, target):
    """Return True if target is in lst."""
    if not lst:
        return False
    if lst[0] == target:
        return True
    return recursive_contains(lst[1:], target)

def flatten(lst):
    """Flatten a nested list structure."""
    if not lst:
        return []
    first = lst[0]
    rest_flat = flatten(lst[1:])
    if isinstance(first, list):
        return flatten(first) + rest_flat
    return [first] + rest_flat
```

**Correctness proofs** (abbreviated):
- `recursive_sum`: base case `sum([]) = 0`; inductive step `sum([h]+t) = h + sum(t)` ✓
- `recursive_max`: base case `max([x]) = x`; inductive step: max of list is max of head vs max of tail ✓

---

## 6. Recursive String Processing

```python
def is_palindrome(s):
    """Return True if s is a palindrome (ignoring case and spaces)."""
    # Clean first
    cleaned = "".join(c.lower() for c in s if c.isalpha())
    return _is_palindrome_helper(cleaned)

def _is_palindrome_helper(s):
    # Base cases: 0 or 1 characters are always palindromes
    if len(s) <= 1:
        return True
    # Recursive case: first and last must match; middle must be palindrome
    if s[0] != s[-1]:
        return False
    return _is_palindrome_helper(s[1:-1])

# Test:
assert _is_palindrome_helper("racecar") == True
assert _is_palindrome_helper("hello")   == False
assert _is_palindrome_helper("")        == True
assert _is_palindrome_helper("a")       == True
```

**Recursion tree for `_is_palindrome_helper("racecar")`:**
```
is_palindrome_helper("racecar")  → 'r'=='r': True → recurse on "aceca"
  is_palindrome_helper("aceca")  → 'a'=='a': True → recurse on "cec"
    is_palindrome_helper("cec")  → 'c'=='c': True → recurse on "e"
      is_palindrome_helper("e")  → len==1: return True
    returns True
  returns True
returns True
```

---

## 7. The Tower of Hanoi

The Tower of Hanoi is the classic recursive problem. Three pegs: A (source), B (auxiliary), C (destination). N disks of decreasing size, all on A. Rules:
- Move one disk at a time
- Never place a larger disk on a smaller one
- Goal: move all disks from A to C

**The recursive insight:**
To move N disks from A to C using B:
1. Move N-1 disks from A to B (using C as auxiliary)
2. Move the largest disk from A to C
3. Move N-1 disks from B to C (using A as auxiliary)

```python
def hanoi(n, source, destination, auxiliary):
    """
    Print moves to transfer n disks from source to destination via auxiliary.

    Args:
        n:           number of disks
        source:      name of the source peg (e.g. 'A')
        destination: name of the destination peg
        auxiliary:   name of the auxiliary peg
    """
    if n == 1:    # base case: move one disk directly
        print(f"Move disk 1 from {source} to {destination}")
        return

    # Step 1: move n-1 disks from source to auxiliary
    hanoi(n - 1, source, auxiliary, destination)

    # Step 2: move the largest disk from source to destination
    print(f"Move disk {n} from {source} to {destination}")

    # Step 3: move n-1 disks from auxiliary to destination
    hanoi(n - 1, auxiliary, destination, source)


# Test with n=3:
hanoi(3, 'A', 'C', 'B')
```

Output for n=3 (7 moves):
```
Move disk 1 from A to C
Move disk 2 from A to B
Move disk 1 from C to B
Move disk 3 from A to C
Move disk 1 from B to A
Move disk 2 from B to C
Move disk 1 from A to C
```

**How many moves does this take?** Let T(n) be the number of moves.
- T(1) = 1
- T(n) = 2·T(n-1) + 1

Solving: T(n) = 2^n - 1. For 64 disks: 2^64 - 1 ≈ 1.8 × 10^19 moves. At one move per second: ~585 billion years. This is a provably optimal solution — you cannot do better.

---

## 8. Binary Search — Recursion on a Search Space

Binary search is one of the most important algorithms in CS. Given a **sorted** list and a target, find the target's index (or report it's absent) in O(log n) time.

**The recursive idea:** Look at the middle element.
- If it equals the target: done.
- If it's less than the target: the target must be in the right half.
- If it's greater than the target: the target must be in the left half.

```python
def binary_search(lst, target, lo=0, hi=None):
    """
    Search for target in sorted lst[lo:hi+1].
    Returns the index if found, -1 otherwise.

    Invariant: if target is in lst, it is in lst[lo:hi+1].
    """
    if hi is None:
        hi = len(lst) - 1

    # Base case: search space is empty
    if lo > hi:
        return -1

    mid = (lo + hi) // 2

    if lst[mid] == target:
        return mid
    elif lst[mid] < target:
        # Target is in the right half
        return binary_search(lst, target, mid + 1, hi)
    else:
        # Target is in the left half
        return binary_search(lst, target, lo, mid - 1)


# Tests:
lst = [1, 3, 5, 7, 9, 11, 13]
assert binary_search(lst, 7)  == 3
assert binary_search(lst, 1)  == 0
assert binary_search(lst, 13) == 6
assert binary_search(lst, 4)  == -1
assert binary_search(lst, 14) == -1
assert binary_search([], 5)   == -1
```

**Correctness by induction:**
- Base case: `lo > hi` → search space empty → target not there → return -1 ✓
- Inductive step: if `binary_search` correctly searches any list of size k, then for size k+1:
  - If `lst[mid] == target`: found, return mid ✓
  - If `lst[mid] < target`: target is in `lst[mid+1:hi+1]` (size ≤ k by induction) ✓
  - If `lst[mid] > target`: target is in `lst[lo:mid]` (size ≤ k by induction) ✓

**Why O(log n)?** Each call halves the search space. Starting from n, after k halvings: n/2^k = 1, so k = log₂n calls. For n = 1,000,000: at most 20 calls.

---

## 9. Tail Recursion: And Why Python Doesn't Optimize It

A **tail-recursive** function makes its recursive call as its **last action** — there is no work to do after the call returns.

```python
# NOT tail recursive — must multiply after recursive call returns:
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)   # must wait for result to multiply

# Tail recursive — the recursive call IS the return value:
def factorial_tail(n, accumulator=1):
    if n == 0:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)  # nothing to do after
```

In functional languages (Scheme, Haskell, Erlang), tail calls are optimized to reuse the current stack frame — constant stack space regardless of depth.

**Python does NOT optimize tail calls.** The CPython interpreter keeps every frame, so `factorial_tail(10000)` still overflows the stack. This is a deliberate design choice by Guido van Rossum — Python prioritizes readable tracebacks over tail call optimization.

For deep recursion in Python: convert to an iterative solution or use the `sys.setrecursionlimit()` (risky). We'll see the iterative conversion technique in lecture 14.

---

## 10. Python's Recursion Limit

```python
import sys
print(sys.getrecursionlimit())   # 1000 (default)

# What happens when you exceed it:
def infinite(n):
    return infinite(n + 1)

infinite(0)   # RecursionError: maximum recursion depth exceeded
```

For well-designed recursive functions on reasonable inputs, 1000 frames is rarely a problem. The recursion limit exists to catch infinite recursion early (preventing memory exhaustion) and to maintain traceback quality.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Three laws | Base case; change toward base case; call itself |
| Induction connection | Base case = P(0); inductive step = P(k) → P(k+1) |
| Recursion tree | Visualizes all calls; leaves are base cases; values flow bottom-up |
| Fibonacci naive | O(2^n) — exponential due to overlapping subproblems |
| Memoization | Cache results; O(n) instead of O(2^n) |
| List recursion | Empty list = base case; head + tail = recursive structure |
| Tower of Hanoi | T(n) = 2^n - 1 moves; provably optimal |
| Binary search | O(log n); halves search space each call |
| Tail recursion | Last action is the recursive call; Python doesn't optimize |
| Recursion limit | 1000 frames by default; `RecursionError` if exceeded |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Instrument the naive Fibonacci from §4 with a call counter and report the number of calls for `n = 5, 10, 20`. Then find the closed form relating calls to `fib(n)` itself.

**2. (Explain.)** §2 claims recursion and mathematical induction are the same idea. Make the correspondence exact: for the function below, state the induction hypothesis, the base case, and the inductive step, and identify which part of the *code* plays each role.

```python
def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)
```

**3. (Build.)** Write the Tower of Hanoi solver that *records* its moves. Run it for n = 3, report the move list, and confirm the move count against the closed form. Then explain why the recurrence T(n) = 2T(n−1) + 1 has solution 2ⁿ − 1.

**4. (Stretch.)** Python's default recursion limit is 1000 and there is no tail-call optimisation. Explain why CPython refuses to add TCO, and rewrite this tail-recursive function as a loop.

```python
def total(xs, acc=0):
    if not xs:
        return acc
    return total(xs[1:], acc + xs[0])
```


### Answers

**1.** `fib(5)` → **15** calls, `fib(10)` → **177**, `fib(20)` → **21,891**.

The closed form is **calls(n) = 2·fib(n+1) − 1**. Check it: `fib(6) = 8`, and `2·8 − 1 = 15` ✓; `fib(11) = 89`, and `2·89 − 1 = 177` ✓; `fib(21) = 10946`, and `2·10946 − 1 = 21891` ✓.

The reason is structural. The recursion tree is a binary tree in which every **leaf** returns a base case contributing 1 to the answer, so there are exactly `fib(n)` leaves. A binary tree in which every internal node has exactly two children has one fewer internal node than leaves, giving `fib(n) − 1` internal nodes and `2·fib(n) − 1` total. The off-by-one against the stated formula comes from the `n < 2` base convention — count for yourself which nodes are leaves under it.

Since `fib(n)` grows like φⁿ/√5 with φ ≈ 1.618, the call count is **Θ(φⁿ)** — exponential. This is the concrete cost of recomputing overlapping subproblems, and memoisation collapses it to Θ(n).

**2.** **Claim:** for all integers n ≥ 0, `fact(n)` returns n!.

- **Base case.** `fact(0)` returns `1`, and 0! = 1 by definition. ✓ *In the code:* the `if n == 0` branch.
- **Induction hypothesis.** Assume `fact(k)` returns k! for some k ≥ 0. *In the code:* the assumption you are permitted to make about the recursive call `fact(n - 1)` — that it already works. This is the leap of faith that makes recursion writable.
- **Inductive step.** `fact(k+1)` returns `(k+1) * fact(k)`, which by hypothesis is `(k+1) · k!` = `(k+1)!`. ✓ *In the code:* the `return n * fact(n - 1)` line.

The correspondence is exact, and it is not a metaphor: **a recursive function is a proof by induction, and the proof's structure is the code's structure.** This is why the three laws of recursion in §1 are the three parts of an induction, and why a recursive function with no base case is the same error as an induction with no base case — an argument that assumes what it should establish.

It also tells you where to look when a recursive function is wrong. If the base case is wrong, small inputs fail. If the step is wrong, small inputs pass and larger ones fail. MATH 151 formalises this.

**3.**

```python
def hanoi(n, src, dst, spare, moves):
    if n == 0:
        return
    hanoi(n - 1, src, spare, dst, moves)
    moves.append((src, dst))
    hanoi(n - 1, spare, dst, src, moves)

moves = []
hanoi(3, 'A', 'C', 'B', moves)
```

For n = 3 this gives **7 moves**: A→C, A→B, C→B, A→C, B→A, B→C, A→C. And 2³ − 1 = 7 ✓.

To solve T(n) = 2T(n−1) + 1 with T(0) = 0, unroll it:

T(n) = 2T(n−1) + 1 = 2[2T(n−2) + 1] + 1 = 4T(n−2) + 2 + 1 = 8T(n−3) + 4 + 2 + 1 = …

After k steps, T(n) = 2ᵏT(n−k) + (2ᵏ⁻¹ + … + 2 + 1) = 2ᵏT(n−k) + 2ᵏ − 1. Setting k = n gives T(n) = 2ⁿ·T(0) + 2ⁿ − 1 = **2ⁿ − 1**.

The `+1` per level contributes a geometric series, and in a geometric series the **last term dominates** — which is why the answer is 2ⁿ up to a constant. You will do this systematically with the Master Theorem in L20. Note also that 2ⁿ − 1 moves is provably optimal: every disk above the largest must move off before it can move, and back on after.

**4.**

```python
def total(xs):
    acc = 0
    for x in xs:
        acc += x
    return acc
```

The transformation is mechanical for any tail call: the accumulator becomes a local, the recursive call becomes the next loop iteration, and the base case becomes the loop exit.

Guido van Rossum's stated reasons for rejecting TCO are about **debuggability**, not difficulty. Eliminating frames destroys the stack trace: a crash a million iterations deep would report a single frame, and you would lose the call history that makes Python tracebacks useful. He also argued that TCO invites writing loops as recursion, which is not the idiom Python wants to encourage, and that the optimisation would be silent — code would work or blow the stack depending on whether the compiler recognised a call as tail-position, a fragile property to depend on.

Note the version above is also **O(n²)** in Python regardless of TCO, because `xs[1:]` copies the remaining list on every call. Passing an index instead would fix that — a reminder that the recursion is not always the expensive part.



---

## Reading

- **Guttag, Ch. 4.3** — Recursion (primary — read carefully)
- **Guttag, Ch. 3.4** — Binary Search (connects recursion to search)

---

*CS 101 · Week 4 · Lecture 13 (Wed) · © CSE Department*
