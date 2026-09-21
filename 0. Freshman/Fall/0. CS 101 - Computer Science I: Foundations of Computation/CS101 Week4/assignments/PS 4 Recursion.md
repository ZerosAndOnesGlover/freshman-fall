# CS 101 · Problem Set 4
## Recursion: Thinking in Self-Reference

**Released:** Friday 23 October 2026, 10:00 (after L15) · Week 4
**Due:** Friday 30 October 2026, 17:00 · Week 5 — late penalty from 17:01
**Submission:** `ps4.py` (Part B) and your answer sheet (Part A) in `"$CS101/week4"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 4–5 hours

---

## What this problem set uses

Weeks 0–4: the three laws of recursion and the induction connection (L13 §1–2), recursion trees
(L13 §3, L14 §1), recursion on lists and strings (L13 §5–6), recursive binary search (L13 §8), merge
sort (L14 §2), converting recursion to iteration (L14 §5), and the power-set pattern (L15 §5).
Induction is also MATH 151 Week 3.

**Not needed and not expected:** memoization with a dictionary (dictionaries are Week 8), Big-O
notation (Week 6 — count calls instead), backtracking beyond subsets and combinations.

Every Part B function needs a docstring that names its base case and recursive case, and at least
two `assert` tests.

---

## Part A: Written (36 points)

### A1: The Three Laws (8 points)

For each function, say which law (base case, progress toward it, self-call) is broken — or that all
three hold. If one is broken, give an input that fails and write the fix.

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

### A2: Recursion Trees (10 points)

```python
def mystery(n):
    if n <= 0:
        return 0
    return mystery(n - 1) + mystery(n - 1) + mystery(n - 2)
```

**(a)** Let `T(n)` be the number of calls made by `mystery(n)`, counting the first. Write the recurrence
for `T(n)`, give `T(0)`, `T(-1)`, and compute `T(1)` … `T(4)`. Check `T(2)` by drawing its tree.

**(b)** For the function below, how many calls (counting the first) does `count(8)` make? And `count(7)`?
Why is there such a difference?

```python
def count(n):
    if n <= 1:
        return n
    if n % 2 == 0:
        return count(n // 2)
    return count(n - 1) + count(n - 1)
```

### A3: Proofs by Induction (12 points)

**(a)** Prove that `triangle(n)` returns `n(n + 1)/2` for every integer `n ≥ 0`.

```python
def triangle(n):
    if n == 0:
        return 0
    return n + triangle(n - 1)
```

**(b)** Prove that `fast_power(b, n)` returns `bⁿ` for every integer `n ≥ 0`. Use strong induction
(MATH 151 L11): assume it is correct for every smaller exponent, and handle `n = 0`, `n` even, `n` odd.

```python
def fast_power(b, n):
    if n == 0:
        return 1
    if n % 2 == 0:
        half = fast_power(b, n // 2)
        return half * half
    return b * fast_power(b, n - 1)
```

### A4: Recursion or Iteration? (6 points)

Which is clearer, and why (one sentence each)?

**(a)** The sum of 1..n. **(b)** Visiting every file in a folder and all its sub-folders.
**(c)** All binary strings of length n.

---

## Part B: Python (`ps4.py`) (64 points)

### B1: Recursive List Operations (16 points)

**(a)** `recursive_min(lst)` — the smallest element of a non-empty list.
**(b)** `count_if(lst, predicate)` — `count_if([1, 2, 3, 4, 5], lambda x: x % 2 == 0)` → `2`.
**(c)** `flatten(lst)` — `flatten([1, [2, [3, [4]], 5]])` → `[1, 2, 3, 4, 5]` (L13 §5 builds this).
**(d)** `deep_sum(lst)` — `deep_sum([1, [2, [3]], 4])` → `10`.

### B2: Recursive String Operations (12 points)

No loops.

**(a)** `count_vowels(s)` — any case. `count_vowels("Recursion")` → `4`.
**(b)** `is_balanced(s, depth=0)` — every `(` closed by a later `)`. `depth` counts the currently open
brackets; it must never go negative. `"(()())"` → `True`, `"(()"` → `False`, `")("` → `False`, `""` → `True`.
**(c)** `interleave(s1, s2)` — `("abc", "def")` → `"adbecf"`; `("ab", "defg")` → `"adbefg"`.

### B3: Divide and Conquer (16 points)

**(a)** `fast_power(base, exp)` — the function from A3(b).
**(b)** `merge(left, right)` and `merge_sort(lst)` as in L14 §2. `merge_sort([5, 2, 9, 1, 5, 6])` → `[1, 2, 5, 5, 6, 9]`.
**(c)** `binary_search(lst, target, lo=0, hi=None)` — recursive, as in L13 §8; return the index or `-1`.

### B4: Subsets and Combinations (12 points)

**(a)** `subsets(lst)` — all subsets (L15 §5): the subsets of the rest, plus each of those with the
first element added. `subsets([1, 2, 3])` has 8 elements.
**(b)** `combinations(lst, k)` — all `k`-element subsets, using `C(n, k) = C(n−1, k−1) + C(n−1, k)`:
`combinations([1, 2, 3, 4], 2)` → `[[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]`.

### B5: Recursion to Iteration (8 points)

**(a)** `factorial_iterative(n)` with a `for` loop.
**(b)** `binary_search_iter(lst, target)` with a `while` loop. Test that it agrees with your recursive
version for every target from 0 to 12 in `[1, 3, 5, 7, 9, 11]`.

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Three laws | 8 |
| A2 Recursion trees | 10 |
| A3 Induction | 12 |
| A4 Recursion or iteration | 6 |
| B1 Lists | 16 |
| B2 Strings | 12 |
| B3 Divide and conquer | 16 |
| B4 Subsets and combinations | 12 |
| B5 Recursion to iteration | 8 |
| **Total** | **100** |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps4.py` below was run; every assert passes.
> Call counts in A2 were measured with a counter.

### A1 (8, 2 each)

(a) All three hold — prints `n, n−1, …, 0`. (b) No base case for `[]`: `sum_list([])` raises
`IndexError`. Fix: `if lst == []: return 0`. (c) No base case for a list with no zero:
`find_zero([1, 2])` raises `IndexError`. Fix: `if lst == []: return False` first. (d) No progress:
`always_recurse(1)` calls itself with 1 forever → `RecursionError`. Fix: `always_recurse(n - 1)`.

### A2 (10)

(a) `T(n) = 1 + 2T(n−1) + T(n−2)`, `T(0) = T(−1) = 1`. `T(1) = 4`, `T(2) = 10`, `T(3) = 25`,
**`T(4) = 61`** (measured). *(6)*
(b) `count(8)`: **4** calls (8 → 4 → 2 → 1). `count(7)`: **13** calls. Even `n` halves with one
call; odd `n` makes **two** calls on `n − 1`, doubling the tree. *(4)*

### A3 (12, 6 each)

(a) *Base* `n = 0`: returns 0 = 0·1/2. *Step*: assume `triangle(k) = k(k+1)/2`. Then
`triangle(k+1) = (k+1) + k(k+1)/2 = (k+1)(k+2)/2`. ✓
(b) *Base* `n = 0`: returns 1 = b⁰. *Step* (strong): assume correct for all exponents `< n`, `n ≥ 1`.
If `n` is even, `n // 2 < n`, so `half = b^(n/2)` and `half * half = bⁿ`. If `n` is odd, `n − 1 < n`,
so the result is `b · bⁿ⁻¹ = bⁿ`. ✓ Ordinary (weak) induction is not enough for the even case, since
it needs `n/2`, not `n − 1`.

### A4 (6, 2 each)

(a) Iteration — a simple count. (b) Recursion — the folder structure is itself recursive (a folder
holds folders). (c) Recursion — each string is a choice of `0` or `1` followed by a shorter string.

### Part B — reference `ps4.py`

```python
# --- B1: Recursive list operations ---
def recursive_min(lst):
    """Smallest element of a non-empty list. Base: one element. Step: min of first and min of rest."""
    assert len(lst) > 0
    if len(lst) == 1:
        return lst[0]
    rest = recursive_min(lst[1:])
    return lst[0] if lst[0] < rest else rest

def count_if(lst, predicate):
    """Number of elements x with predicate(x) true."""
    if lst == []:
        return 0
    return (1 if predicate(lst[0]) else 0) + count_if(lst[1:], predicate)

def flatten(lst):
    """All non-list items of an arbitrarily nested list, in order."""
    if lst == []:
        return []
    first = lst[0]
    if isinstance(first, list):
        return flatten(first) + flatten(lst[1:])
    return [first] + flatten(lst[1:])

def deep_sum(lst):
    """Sum of every number in an arbitrarily nested list."""
    if lst == []:
        return 0
    first = lst[0]
    if isinstance(first, list):
        return deep_sum(first) + deep_sum(lst[1:])
    return first + deep_sum(lst[1:])

assert recursive_min([3, 1, 4, 1, 5]) == 1 and recursive_min([7]) == 7
assert count_if([1, 2, 3, 4, 5], lambda x: x % 2 == 0) == 2 and count_if([], lambda x: True) == 0
assert flatten([1, [2, [3, [4]], 5]]) == [1, 2, 3, 4, 5] and flatten([]) == [] and flatten([[[1]]]) == [1]
assert deep_sum([1, [2, [3]], 4]) == 10 and deep_sum([]) == 0

# --- B2: Recursive string operations ---
def count_vowels(s):
    """Number of vowels in s, any case."""
    if s == "":
        return 0
    return (1 if s[0].lower() in "aeiou" else 0) + count_vowels(s[1:])

def is_balanced(s, depth=0):
    """True if every '(' in s is closed by a later ')'. depth = currently open brackets."""
    if depth < 0:
        return False
    if s == "":
        return depth == 0
    if s[0] == "(":
        return is_balanced(s[1:], depth + 1)
    if s[0] == ")":
        return is_balanced(s[1:], depth - 1)
    return is_balanced(s[1:], depth)

def interleave(s1, s2):
    """Alternate characters of s1 and s2; append the rest of the longer one."""
    if s1 == "":
        return s2
    if s2 == "":
        return s1
    return s1[0] + s2[0] + interleave(s1[1:], s2[1:])

assert count_vowels("Recursion") == 4 and count_vowels("") == 0
assert is_balanced("(()())") and not is_balanced("(()") and is_balanced("") and not is_balanced(")(")
assert interleave("abc", "def") == "adbecf" and interleave("ab", "defg") == "adbefg"

# --- B3: Divide and conquer ---
def fast_power(base, exp):
    """base ** exp using halving: O(log exp) multiplications."""
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = fast_power(base, exp // 2)
        return half * half
    return base * fast_power(base, exp - 1)

def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]

def merge_sort(lst):
    """A new sorted list with the elements of lst (L14 §2)."""
    if len(lst) <= 1:
        return lst[:]
    mid = len(lst) // 2
    return merge(merge_sort(lst[:mid]), merge_sort(lst[mid:]))

def binary_search(lst, target, lo=0, hi=None):
    """Index of target in sorted lst, or -1 (L13 §8)."""
    if hi is None:
        hi = len(lst) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if lst[mid] == target:
        return mid
    if lst[mid] < target:
        return binary_search(lst, target, mid + 1, hi)
    return binary_search(lst, target, lo, mid - 1)

assert fast_power(2, 10) == 1024 and fast_power(3, 0) == 1 and fast_power(2, 100) == 2 ** 100
assert merge_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9] and merge_sort([]) == []
assert binary_search([1, 3, 5, 7, 9, 11], 7) == 3 and binary_search([1, 3, 5, 7, 9, 11], 4) == -1 and binary_search([], 1) == -1

# --- B4: Choose-explore-unchoose ---
def subsets(lst):
    """All subsets of lst: those without the first element, then those with it."""
    if lst == []:
        return [[]]
    rest = subsets(lst[1:])
    with_first = []
    for s in rest:
        with_first.append([lst[0]] + s)
    return rest + with_first

def combinations(lst, k):
    """All k-element subsets of lst, keeping lst's order: C(n,k) = C(n-1,k-1) + C(n-1,k)."""
    if k == 0:
        return [[]]
    if len(lst) < k:
        return []
    with_first = []
    for c in combinations(lst[1:], k - 1):
        with_first.append([lst[0]] + c)
    return with_first + combinations(lst[1:], k)

assert len(subsets([1, 2, 3])) == 8 and [] in subsets([1, 2, 3]) and [1, 2, 3] in subsets([1, 2, 3])
assert combinations([1, 2, 3, 4], 2) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
assert len(combinations([1, 2, 3, 4, 5], 3)) == 10 and combinations([1, 2], 3) == []

# --- B5: Recursion to iteration ---
def factorial_iterative(n):
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result

def binary_search_iter(lst, target):
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            return mid
        if lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

assert factorial_iterative(0) == 1 and factorial_iterative(10) == 3628800
for t in range(0, 13):
    assert binary_search_iter([1, 3, 5, 7, 9, 11], t) == binary_search([1, 3, 5, 7, 9, 11], t)
print(subsets([1, 2, 3]))
print("all asserts passed")
```

**Marking.** B1 4 each. B2 4 each — `is_balanced` must reject `")("`. B3: 4 / 8 / 4. B4: 6 each —
order within `subsets` may differ; check with `len` and membership. B5: 4 each.
Missing base/recursive case in a docstring, or fewer than two asserts: −1 per function (max −5).
Using a loop where recursion is required in B1–B4: half marks for that function.

---

*CS 101 · Week 4 · Problem Set 4 · Due Friday 30 October 2026, 17:00 · © CSE Department*
