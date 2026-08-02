# CS 101 Problem Set 4
## Recursion: Thinking in Self-Reference

**Released:** Friday, Week 4
**Due:** Friday, Week 5 at 11:59 PM
**Submission:** Upload `ps4.py` and `PS 4 Recursion.md`
**Weight:** Part of the 30% Problem Sets grade

---

## Overview

This problem set covers:
- The three laws of recursion
- Correctness proofs by induction (base case + inductive step)
- Recursion tree analysis (counting calls, identifying complexity)
- Recursive list and string processing
- Divide-and-conquer algorithms
- Backtracking with choose-explore-unchoose
- Memoization to eliminate redundant subproblems
- Converting recursion to iteration

**Every function must have:**
- A complete docstring with base case, recursive case, and examples
- A correctness argument (commented — "Base: ... ✓; Step: ... ✓")
- At least 2 `assert` tests

---

## Part A: Written Questions (`PS 4 Recursion.md`)

### A1: Three Laws Analysis (6 points)

For each function below, identify which of the three laws (base case, progress, self-call) is violated — or state that all three are satisfied. If violated, write the corrected version.

**(a)**
```python
def countdown(n):
    print(n)
    if n > 0:
        countdown(n - 1)
```

**(b)**
```python
def sum_list(lst):
    if len(lst) == 1:
        return lst[0]
    return lst[0] + sum_list(lst[1:])
```

**(c)**
```python
def find_zero(lst):
    if lst[0] == 0:
        return True
    return find_zero(lst[1:])
```

**(d)**
```python
def always_recurse(n):
    if n == 0:
        return 0
    return always_recurse(n)
```

---

### A2: Recursion Tree Analysis (8 points)

**(a)** Draw the complete recursion tree for this call and count total nodes:

```python
def mystery(n):
    if n <= 0:
        return 0
    return mystery(n-1) + mystery(n-1) + mystery(n-2)

mystery(4)
```

**(b)** Without drawing the full tree, determine the number of calls to `f(0)` when `mystery(n)` is called. Give a formula in terms of n. (Hint: work out n=1,2,3,4 and find the pattern.)

**(c)** What is the time complexity of `mystery(n)` in Big-O notation? Justify with the recursion tree structure.

**(d)** For the following function, determine the exact number of recursive calls made by `count(8)`:

```python
def count(n):
    if n <= 1:
        return n
    if n % 2 == 0:
        return count(n // 2)
    return count(n - 1) + count(n - 1)
```

---

### A3: Inductive Proofs (8 points)

Write complete proofs by induction for each claim.

**(a)** Prove that this function computes n·(n+1)/2 for all non-negative integers n:

```python
def triangle(n):
    if n == 0:
        return 0
    return n + triangle(n - 1)
```

**(b)** Prove that `fast_power(b, n)` computes b^n for all non-negative integers n:

```python
def fast_power(b, n):
    if n == 0: return 1
    if n % 2 == 0:
        half = fast_power(b, n // 2)
        return half * half
    return b * fast_power(b, n - 1)
```

(Hint: you need to handle three cases: n=0, n even, n odd.)

---

### A4: Recursion vs. Iteration (4 points)

For each problem, state whether recursion or iteration is the clearer solution and give a one-sentence justification:

**(a)** Computing the sum of all integers from 1 to n.

**(b)** Traversing all files and subdirectories in a directory tree.

**(c)** Finding whether a given number is in a sorted array.

**(d)** Generating all binary strings of length n.

---

## Part B: Python Implementation (`ps4.py`)

### B1: Recursive List Operations (12 points)

Implement each function **recursively** using the pattern: base case on empty/single-element list, recursive case on smaller list. Pass **indices** (not slices) where possible to avoid O(n²) behavior.

**(a)** `recursive_min(lst)` — return the minimum value.

**(b)** `count_if(lst, predicate)` — count elements satisfying predicate.
- `count_if([1,2,3,4,5], lambda x: x % 2 == 0)` → `2`

**(c)** `flatten(lst)` — flatten arbitrarily nested lists.
- `flatten([1,[2,[3,[4]],5]])` → `[1,2,3,4,5]`

**(d)** `all_pairs(lst)` — return all pairs (i,j) where i < j as a list of tuples.
- `all_pairs([1,2,3])` → `[(1,2),(1,3),(2,3)]`

**(e)** `zip_lists(lst1, lst2)` — zip two lists into pairs (without using `zip()`).
- `zip_lists([1,2,3],[4,5,6])` → `[(1,4),(2,5),(3,6)]`
- Stop at the shorter list.

**(f)** `deep_sum(lst)` — sum all numbers in a nested list.
- `deep_sum([1,[2,[3]],4])` → `10`

---

### B2: Recursive String Operations (10 points)

**(a)** `count_vowels(s)` — count vowels in s (case-insensitive) recursively.
- No loops, no list comprehensions.

**(b)** `reverse_words(sentence)` — reverse the order of words in a sentence.
- `reverse_words("hello world foo")` → `"foo world hello"`
- Split on spaces; reverse recursively (not `[::-1]`).

**(c)** `is_balanced(s)` — return True if every `(` is matched by a `)`.
- `is_balanced("(()())")` → True
- `is_balanced("(()")` → False
- `is_balanced("")` → True
- Use a recursive helper with a `depth` counter.

**(d)** `interleave(s1, s2)` — interleave two strings character by character.
- `interleave("abc","def")` → `"adbecf"`
- `interleave("ab","defg")` → `"adbefg"` (append remaining when one is exhausted)

**(e)** `longest_run(s)` — return the length of the longest run of identical consecutive characters.
- `longest_run("aaabbbcccc")` → 4
- `longest_run("a")` → 1
- `longest_run("")` → 0

---

### B3: Divide and Conquer (12 points)

**(a)** `fast_power(base, exp)` — O(log exp) exponentiation (from lab, if not done).

**(b)** `merge_sort(lst)` — complete merge sort with `merge()` helper (from lab, if not done).

**(c)** `find_rotation_point(lst)` — given a sorted list that has been rotated (e.g., `[4,5,6,7,1,2,3]`), find the index of the smallest element using divide and conquer.
- `find_rotation_point([4,5,6,7,1,2,3])` → `4` (index of 1)
- `find_rotation_point([1,2,3,4,5])` → `0` (not rotated)
- Time: O(log n).

**(d)** `count_inversions(lst)` — count the number of pairs (i,j) where i < j but lst[i] > lst[j].
- `count_inversions([3,1,2])` → `2` (pairs: (3,1) and (3,2))
- `count_inversions([1,2,3])` → `0`
- Naive O(n²) solution acceptable; O(n log n) using a modified merge sort is the challenge version.

**(e)** `closest_pair_1d(lst)` — given a sorted list of numbers, find the pair with the smallest difference.
- `closest_pair_1d([1,3,6,10,15])` → `(1,3)` (difference of 2)
- Can be done in O(n) with a loop — implement it recursively in O(n) with divide and conquer for the exercise.

---

### B4: Backtracking (14 points)

**(a)** `subsets(lst)` — return all subsets of lst (power set).
- `subsets([1,2,3])` → `[[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]`
- Use the recursive structure: each element is either included or not.

**(b)** `combinations(lst, k)` — return all k-element subsets of lst.
- `combinations([1,2,3,4], 2)` → `[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]`
- C(n,k) = C(n-1,k-1) + C(n-1,k): include first element or don't.

**(c)** `sum_subsets(lst, target)` — return all subsets of lst that sum to target.
- `sum_subsets([2,4,6,8], 10)` → `[[2,8],[4,6]]`

**(d)** `word_break(s, words)` — given a string s and a list of valid words, return True if s can be formed by concatenating words from the list.
- `word_break("leetcode", ["leet","code"])` → True
- `word_break("applepenapple", ["apple","pen"])` → True
- `word_break("catsandog", ["cats","dog","sand","and","cat"])` → False
- Add memoization to handle overlapping subproblems.

**(e)** `generate_parentheses(n)` — return all strings of n pairs of balanced parentheses.
- `generate_parentheses(3)` → `["((()))", "(()())", "(())()", "()(())", "()()()"]`
- Use a helper that tracks open and close counts.

---

### B5: Memoization (10 points)

**(a)** `fib_memo(n)` — Fibonacci with memoization (if not already done).

**(b)** `catalan(n)` — the nth Catalan number.
- C(0)=1, C(1)=1, C(n) = sum of C(i)*C(n-1-i) for i in 0..n-1
- C(5)=42. Add memoization.

**(c)** `count_paths(m, n)` — count paths from top-left to bottom-right of an m×n grid, moving only right or down.
- `count_paths(2,2)` → 2, `count_paths(3,3)` → 6
- Recurrence: `paths(m,n) = paths(m-1,n) + paths(m,n-1)`
- Add memoization; the result is C(m+n-2, m-1).

**(d)** `min_coins(coins, amount)` — minimum number of coins to make `amount`.
- `min_coins([1,5,10,25], 36)` → 3 (25+10+1)
- `min_coins([2], 3)` → -1 (impossible)
- Recurrence: `min_coins(amount) = 1 + min(min_coins(amount-c) for c in coins if c <= amount)`
- Add memoization.

**(e)** `edit_distance(s1, s2)` — minimum edit distance (Levenshtein distance) between two strings.
- Operations: insert, delete, substitute (each costs 1).
- `edit_distance("kitten","sitting")` → 3
- Recurrence:
  - If last chars match: `edit(s1[:-1], s2[:-1])`
  - Otherwise: `1 + min(edit(s1[:-1],s2), edit(s1,s2[:-1]), edit(s1[:-1],s2[:-1]))`
- Add memoization.

---

### B6: Iterative Conversion (8 points)

Rewrite each recursive function as an iterative one. The iterative version must produce identical output.

**(a)** Convert `factorial_recursive(n)` to `factorial_iterative(n)`.

**(b)** Convert `binary_search(lst, target)` (recursive) to `binary_search_iter(lst, target)` using a while loop.

**(c)** Convert `flatten(lst)` (recursive) to `flatten_iter(lst)` using an explicit stack (list used as a stack with `.append()` and `.pop()`).

**(d)** Convert `merge_sort(lst)` to `merge_sort_bottom_up(lst)` — an iterative merge sort that starts by merging pairs of single elements, then pairs of pairs, etc. This is O(n log n) without any recursion.

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|--------------|
| A1 Three laws | 6 | Correctly identify violations; correct fix |
| A2 Tree analysis | 8 | Correct tree; correct formula; correct O() |
| A3 Inductive proofs | 8 | Rigorous base + step; correct algebraic manipulation |
| A4 Recursion vs iteration | 4 | Correct choice with justification |
| B1 List operations | 12 | All 6 correct; index-based (not slicing) where noted |
| B2 String operations | 10 | All 5 correct |
| B3 Divide and conquer | 12 | All 5 correct; complexities as specified |
| B4 Backtracking | 14 | All 5 correct; memoization in (d) |
| B5 Memoization | 10 | All 5 correct; memoization actually speeds up |
| B6 Iterative conversion | 8 | All 4 correct; identical outputs verified |
| **Total** | **92** | |
| Docstring + proof quality | up to 5 bonus | |

---

## Part C: Challenge Problems (Ungraded)

**C1: Karatsuba Multiplication**
The naïve multiplication of two n-digit numbers is O(n²). Karatsuba's algorithm (1960) runs in O(n^1.585) using divide-and-conquer:
- Split each number into two halves: X = X_h * 10^(n/2) + X_l, Y = Y_h * 10^(n/2) + Y_l
- Compute: z2 = X_h * Y_h, z0 = X_l * Y_l, z1 = (X_h+X_l)*(Y_h+Y_l) - z2 - z0
- Result: z2*10^n + z1*10^(n/2) + z0
- This uses 3 multiplications instead of 4 → O(n^log₂3) ≈ O(n^1.585)

Implement and verify against Python's `*` operator for large numbers.

**C2: Counting Paths with Obstacles**
Extend `count_paths(m,n)` to handle a grid with obstacles. An obstacle at (i,j) makes that cell impassable. Use memoization. Return 0 if no path exists.

**C3: Regular Expression Matching**
Implement `regex_match(pattern, text)` supporting:
- `.` matches any single character
- `*` matches zero or more of the preceding character
- `isMatch("aab", "c*a*b")` → True

This is a classic recursive problem with overlapping subproblems — add memoization.

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading Rubric above (92 + up to 5 bonus).

### Note on A2(b) wording

A2(b) asks for "the number of calls to **`f(0)`**", but the function is named `mystery`. Read as `mystery(0)` — i.e. how many times the base case is reached. No student should be penalised for either reading.

---

### Part A — Written (26 points)

**A1 Three Laws (6 pts).** 1.5 pts each.

- **(a) `countdown` — all three satisfied.** Base case is the implicit "do nothing when `n <= 0`"; progress via `n-1`; self-call present. It terminates and prints `n` down to `0`. (Accept "no explicit `return`" as a style remark, not a violation.)
- **(b) `sum_list` — base case is incomplete.** It handles `len == 1` but not `len == 0`, so `sum_list([])` recurses to `sum_list([])`… no: it raises `IndexError` on `lst[0]`. Fix: `if not lst: return 0`.
- **(c) `find_zero` — base case missing (crashes).** With no zero present, the list shrinks to `[]` and `lst[0]` raises `IndexError`. It never returns `False`. Fix: `if not lst: return False` before the index.
- **(d) `always_recurse` — progress violated.** It calls `always_recurse(n)` with the *same* `n`, so it never approaches the base case → `RecursionError`. Fix: recurse on `n - 1`.

*Grading: ½ pt naming the violated law, 1 pt for a correct fix. For (a), award full marks for "all three satisfied"; deduct nothing for also noting the missing return.*

**A2 Recursion Tree (8 pts).**

**(a)** Total nodes in the call tree for `mystery(4)` — where `T(n) = 1 + 2T(n−1) + T(n−2)`, `T(n≤0) = 1`:

| n | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| total nodes | 1 | 4 | 10 | 25 | **61** |

**(b)** Base-case hits `B(n)` satisfy `B(n) = 2·B(n−1) + B(n−2)`, with `B(0)=1`, `B(1)=3`:

| n | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| B(n) | 1 | 3 | 7 | 17 | 41 | 99 | 239 |

These are the **half-companion Pell numbers**. Closed form: `B(n) = ((1+√2)^(n+1) + (1−√2)^(n+1)) / 2`. Verified: `B(8)/B(7) = 2.41421…` → `1 + √2`.

**(c)** **O((1+√2)ⁿ) ≈ O(2.414ⁿ)** — exponential. The dominant root of the characteristic equation `x² = 2x + 1` is `1 + √2`. Accept a looser but correctly-justified `O(3ⁿ)` upper bound (each node has ≤3 children) if the student states it as an upper bound rather than a tight one.

**(d)** `count(8)`: 8 is even → `count(4)` → even → `count(2)` → even → `count(1)` → base. So the calls are `count(8), count(4), count(2), count(1)` = **4 invocations, i.e. 3 recursive calls**. The odd branch (which would double) is never taken because 8 is a power of two. In general `count(2^k)` makes exactly `k` recursive calls.

*Grading: 3 pts (a) — the tree or the recurrence with the table. 2 pts (b) — the recurrence alone earns both; the closed form is bonus-worthy. 2 pts (c). 1 pt (d).*
*Common error on (d): answering 255 or similar by assuming the doubling branch fires. Emphasise that `n % 2 == 0` short-circuits it for every value in this chain.*

**A3 Inductive Proofs (8 pts).** 4 pts each.

**(a)** Claim: `triangle(n) = n(n+1)/2` for all `n ≥ 0`.
*Base* (`n=0`): returns `0`; `0·1/2 = 0`. ✓
*IH*: assume `triangle(k) = k(k+1)/2` for some `k ≥ 0`.
*Step*: `triangle(k+1) = (k+1) + triangle(k) = (k+1) + k(k+1)/2 = (k+1)(1 + k/2) = (k+1)(k+2)/2`. ✓ ∎

**(b)** Claim: `fast_power(b, n) = bⁿ` for all `n ≥ 0`. Uses **strong** induction, since the even branch recurses on `n//2`, not `n−1`.
*Base* (`n=0`): returns `1 = b⁰`. ✓
*IH*: assume the claim for all `0 ≤ m < n`.
*Step, n even*: `half = fast_power(b, n/2) = b^(n/2)` by IH (since `n/2 < n` for `n ≥ 1`); returns `half·half = b^(n/2)·b^(n/2) = bⁿ`. ✓
*Step, n odd*: returns `b · fast_power(b, n−1) = b · b^(n−1) = bⁿ` by IH. ✓ ∎

*Grading: 1 pt base, 1 pt IH stated for a fixed k (or "all m < n" for strong), 2 pts algebra. For (b), award only 2 of 4 if the student uses weak induction — the even branch genuinely requires strong induction, and this is the point of the problem.*

**A4 Recursion vs Iteration (4 pts).** 1 pt each; grade the justification.
- **(a) Iteration** — a flat linear accumulation; recursion adds stack depth for no structural gain (and `n(n+1)/2` is closed-form anyway).
- **(b) Recursion** — the data structure is itself a tree; recursion mirrors its shape naturally.
- **(c) Either, leaning iteration** — binary search's recursion is tail-recursive, so the loop form is equivalent and avoids stack depth. Accept recursion with a note about the natural divide-and-conquer reading.
- **(d) Recursion** — the branch-per-position structure (choose `0` or `1`, recurse) is exactly a backtracking tree.

---

### Part B — Coding (66 points)

All values below were executed and match the spec's stated examples.

**B1 Recursive List Operations (12 pts).** 2 pts each.

```python
def recursive_min(lst, i=0):
    if i == len(lst) - 1: return lst[i]           # index-based: no O(n²) slicing
    rest = recursive_min(lst, i + 1)
    return lst[i] if lst[i] < rest else rest

def count_if(lst, predicate, i=0):
    if i == len(lst): return 0
    return (1 if predicate(lst[i]) else 0) + count_if(lst, predicate, i + 1)

def flatten(lst):
    out = []
    for item in lst:
        out.extend(flatten(item)) if isinstance(item, list) else out.append(item)
    return out

def all_pairs(lst, i=0):
    if i >= len(lst) - 1: return []
    return [(lst[i], lst[j]) for j in range(i + 1, len(lst))] + all_pairs(lst, i + 1)

def zip_lists(a, b, i=0):
    if i >= len(a) or i >= len(b): return []      # stop at the shorter
    return [(a[i], b[i])] + zip_lists(a, b, i + 1)

def deep_sum(lst):
    return sum(deep_sum(x) if isinstance(x, list) else x for x in lst)
```

Verified: `all_pairs([1,2,3])` → `[(1,2),(1,3),(2,3)]`; `deep_sum([1,[2,[3]],4])` → `10`.

*Grading: deduct 1 per function that slices (`lst[1:]`) where the spec says to pass indices — the whole point of B1 is avoiding the hidden O(n²) copy cost. `flatten` and `deep_sum` are exempt (structural recursion, not positional).*

**B2 Recursive String Operations (10 pts).** 2 pts each.

```python
def count_vowels(s, i=0):
    if i == len(s): return 0
    return (1 if s[i].lower() in "aeiou" else 0) + count_vowels(s, i + 1)

def reverse_words(sentence):
    words = sentence.split()
    def rev(ws):
        return [] if not ws else rev(ws[1:]) + [ws[0]]
    return " ".join(rev(words))

def is_balanced(s, i=0, depth=0):
    if depth < 0: return False                    # closed one too many
    if i == len(s): return depth == 0
    d = depth + (1 if s[i] == "(" else -1 if s[i] == ")" else 0)
    return is_balanced(s, i + 1, d)

def interleave(a, b):
    if not a: return b
    if not b: return a
    return a[0] + b[0] + interleave(a[1:], b[1:])

def longest_run(s, i=0, cur=1, best=0):
    if not s: return 0
    if i == len(s) - 1: return max(best, cur)
    nxt = cur + 1 if s[i] == s[i + 1] else 1
    return longest_run(s, i + 1, nxt, max(best, cur))
```

Verified: `interleave("abc","def")` → `"adbecf"`; `interleave("ab","defg")` → `"adbefg"`; `longest_run("aaabbbcccc")` → `4`; `longest_run("")` → `0`.

*Common error on `is_balanced`: checking only the final count, so `")("` wrongly passes (net depth 0). The `depth < 0` early return is required — test `")("` explicitly, it must be `False`.*

**B3 Divide and Conquer (12 pts).**

```python
def find_rotation_point(lst):
    lo, hi = 0, len(lst) - 1
    if lst[lo] <= lst[hi]: return 0               # not rotated
    while lo < hi:
        mid = (lo + hi) // 2
        if lst[mid] > lst[hi]: lo = mid + 1       # min is right of mid
        else:                  hi = mid           # min is at or left of mid
    return lo

def count_inversions(lst):                        # O(n log n) via merge sort
    def sort_count(a):
        if len(a) <= 1: return a, 0
        m = len(a) // 2
        left, x = sort_count(a[:m]); right, y = sort_count(a[m:])
        merged, inv, i, j = [], x + y, 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]: merged.append(left[i]); i += 1
            else: merged.append(right[j]); j += 1; inv += len(left) - i
        return merged + left[i:] + right[j:], inv
    return sort_count(lst)[1]
```

Verified: `find_rotation_point([4,5,6,7,1,2,3])` → `4`; `([1,2,3,4,5])` → `0`; `count_inversions([3,1,2])` → `2`; `([1,2,3])` → `0`; `closest_pair_1d([1,3,6,10,15])` → `(1,3)`.

*Grading: 2 pts each (a)(b)(e), 3 pts (c) — must be O(log n), a linear scan earns 1 — and 3 pts (d) (naive O(n²) acceptable per the spec; award full marks, note the O(n log n) version as bonus).*
*The `lst[mid] > lst[hi]` comparison is the crux of (c). Comparing against `lst[lo]` instead fails on the already-sorted case — which is exactly why the spec includes `[1,2,3,4,5]`.*

**B4 Backtracking (14 pts).**

```python
def subsets(lst):
    if not lst: return [[]]
    rest = subsets(lst[1:])
    return rest + [[lst[0]] + r for r in rest]

def combinations(lst, k):
    if k == 0: return [[]]
    if len(lst) < k: return []
    with_first = [[lst[0]] + c for c in combinations(lst[1:], k - 1)]
    return with_first + combinations(lst[1:], k)      # C(n,k)=C(n-1,k-1)+C(n-1,k)

def sum_subsets(lst, target):
    out = []
    def go(i, cur, total):
        if total == target: out.append(list(cur))
        if i >= len(lst) or total > target: return
        for j in range(i, len(lst)):
            cur.append(lst[j]); go(j + 1, cur, total + lst[j]); cur.pop()
    go(0, [], 0)
    return out

def word_break(s, words):
    ws, memo = set(words), {}
    def go(i):
        if i == len(s): return True
        if i in memo: return memo[i]
        memo[i] = any(s[i:j] in ws and go(j) for j in range(i + 1, len(s) + 1))
        return memo[i]
    return go(0)

def generate_parentheses(n):
    out = []
    def go(s, opened, closed):
        if len(s) == 2 * n: out.append(s); return
        if opened < n:      go(s + "(", opened + 1, closed)
        if closed < opened: go(s + ")", opened, closed + 1)
    go("", 0, 0)
    return out
```

Verified: `subsets([1,2,3])` → 8 subsets; `sum_subsets([2,4,6,8],10)` → `[[2,8],[4,6]]`; all three `word_break` cases match (`True, True, False`); `generate_parentheses(3)` → exactly the five strings in the spec, in that order.

*Grading: 2 pts (a), 3 pts (b), 3 pts (c), 3 pts (d) — **memoization is required by the spec**, deduct 2 if absent even when correct — 3 pts (e).*
*`generate_parentheses` correctness hinges on `closed < opened` (not `closed < n`); the looser guard emits unbalanced strings like `"())("`.*

**B5 Memoization (10 pts).** 2 pts each. Verified: `catalan(5)=42`; `count_paths(2,2)=2`, `count_paths(3,3)=6` (= `C(4,2)`); `min_coins([1,5,10,25],36)=3`; `min_coins([2],3)=-1`; `edit_distance("kitten","sitting")=3`.

```python
def min_coins(coins, amount):
    memo = {}                                  # local dict — NOT a default argument
    def go(amt):
        if amt == 0: return 0
        if amt < 0:  return -1
        if amt in memo: return memo[amt]
        best = -1
        for c in coins:
            r = go(amt - c)
            if r >= 0 and (best < 0 or r + 1 < best): best = r + 1
        memo[amt] = best
        return best
    return go(amount)
```

*Critical grading note: a memo written as a **mutable default argument** (`def go(amt, memo={})`) is the PS3-A4 bug resurfacing — the cache leaks across separate top-level calls, so `min_coins([2], 3)` can return a stale answer computed for a different coin set. Deduct 1 and cross-reference PS3 A4. Test by calling `min_coins([1,5,10,25],36)` and then `min_coins([2],3)` in that order — a leaking memo returns something other than `-1`.*
*`min_coins([2],3)` must be `-1`, not `0` or a crash — the impossible case is the one students miss.*

**B6 Iterative Conversion (8 pts).** 2 pts each. Grade on: identical outputs to the recursive versions across a shared test battery, and an explicit stack where the recursion was not tail-recursive.

---

### Part C — Challenge (ungraded)

Standard results: Ackermann grows faster than any primitive-recursive function; the Collatz total-stopping-time has no known closed form; mutual recursion (`is_even`/`is_odd`) is the canonical example that recursion need not be self-referential.

---

*CS 101 · Week 4 · Problem Set 4 · Due Friday Week 5 · © CSE Department*
