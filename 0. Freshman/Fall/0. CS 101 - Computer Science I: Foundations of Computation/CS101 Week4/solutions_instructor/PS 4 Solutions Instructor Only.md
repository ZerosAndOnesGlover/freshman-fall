# CS 101 · Problem Set 4 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps4.py` below was run; every assert passes.
> Call counts in A2 were measured with a counter.

### A1 (8, 2 each)

(a) All three hold — prints `n, n−1, …, 0`. (b) No base case for `[]`: `sum_list([])` raises
`IndexError`. Fix: `if lst == []: return 0`. (c) No base case for a list with no zero:
`find_zero([1, 2])` raises `IndexError`. Fix: `if lst == []: return False` first. (d) No progress:
`always_recurse(1)` calls itself with 1 forever → `RecursionError`. Fix: `always_recurse(n - 1)`.

### A2 (8)

(a) `T(n) = 1 + 2T(n−1) + T(n−2)`, `T(0) = T(−1) = 1`. `T(1) = 4`, `T(2) = 10`, `T(3) = 25`,
**`T(4) = 61`** (measured). *(8)*
### A3 (14, 7 each)

(a) *Base* `n = 0`: returns 0 = 0·1/2. *Step*: assume `triangle(k) = k(k+1)/2`. Then
`triangle(k+1) = (k+1) + k(k+1)/2 = (k+1)(k+2)/2`. ✓
(b) *Base* `n = 0`: returns 1 = b⁰. *Step* (strong): assume correct for all exponents `< n`, `n ≥ 1`.
If `n` is even, `n // 2 < n`, so `half = b^(n/2)` and `half * half = bⁿ`. If `n` is odd, `n − 1 < n`,
so the result is `b · bⁿ⁻¹ = bⁿ`. ✓ Ordinary (weak) induction is not enough for the even case, since
it needs `n/2`, not `n − 1`.

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

assert recursive_min([3, 1, 4, 1, 5]) == 1 and recursive_min([7]) == 7
assert count_if([1, 2, 3, 4, 5], lambda x: x % 2 == 0) == 2 and count_if([], lambda x: True) == 0
assert flatten([1, [2, [3, [4]], 5]]) == [1, 2, 3, 4, 5] and flatten([]) == [] and flatten([[[1]]]) == [1]

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

assert count_vowels("Recursion") == 4 and count_vowels("") == 0
assert is_balanced("(()())") and not is_balanced("(()") and is_balanced("") and not is_balanced(")(")

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

assert fast_power(2, 10) == 1024 and fast_power(3, 0) == 1 and fast_power(2, 100) == 2 ** 100
assert merge_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9] and merge_sort([]) == []

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

assert len(subsets([1, 2, 3])) == 8 and [] in subsets([1, 2, 3]) and [1, 2, 3] in subsets([1, 2, 3])

print(subsets([1, 2, 3]))
print("all asserts passed")
```

**Marking.** B1 6 each. B2 7 each — `is_balanced` must reject `")("`. B3: 8 / 14. B4: 16 —
order within `subsets` may differ; check with `len` and membership.
Missing base/recursive case in a docstring, or fewer than two asserts: −1 per function (max −5).
Using a loop where recursion is required in B1–B4: half marks for that function.

---

*CS 101 · Week 4 · Problem Set 4 · Due Friday 30 October 2026, 17:00 · © CSE Department*
