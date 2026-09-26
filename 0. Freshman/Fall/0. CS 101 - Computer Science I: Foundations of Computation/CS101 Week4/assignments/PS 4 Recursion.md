# CS 101 · Problem Set 4
## Recursion: Thinking in Self-Reference

**Released:** Friday 23 October 2026, 10:00 (after L15) · Week 4
**Due:** Friday 30 October 2026, 17:00 · Week 5 — late penalty from 17:01
**Submission:** `ps4.py` (Part B) and your answer sheet (Part A) in `"$CS101/week4"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 3 hours

*(Revised 2026-09-26: cut from four to five hours to about three. A2(b), A4, `deep_sum`, `interleave`,
the recursive binary search (L13 §8 writes it out), `combinations` and B5 were removed, and the answer
key moved out of this handout.)*

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

## Part A: Written (30 points)

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

### A2: Recursion Trees (8 points)

```python
def mystery(n):
    if n <= 0:
        return 0
    return mystery(n - 1) + mystery(n - 1) + mystery(n - 2)
```

Let `T(n)` be the number of calls made by `mystery(n)`, counting the first. Write the recurrence
for `T(n)`, give `T(0)`, `T(-1)`, and compute `T(1)` … `T(4)`. Check `T(2)` by drawing its tree.

### A3: Proofs by Induction (14 points)

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

## Part B: Python (`ps4.py`) (70 points)

### B1: Recursive List Operations (18 points)

**(a)** `recursive_min(lst)` — the smallest element of a non-empty list.
**(b)** `count_if(lst, predicate)` — `count_if([1, 2, 3, 4, 5], lambda x: x % 2 == 0)` → `2`.
**(c)** `flatten(lst)` — `flatten([1, [2, [3, [4]], 5]])` → `[1, 2, 3, 4, 5]` (L13 §5 builds this).

### B2: Recursive String Operations (14 points)

No loops.

**(a)** `count_vowels(s)` — any case. `count_vowels("Recursion")` → `4`.
**(b)** `is_balanced(s, depth=0)` — every `(` closed by a later `)`. `depth` counts the currently open
brackets; it must never go negative. `"(()())"` → `True`, `"(()"` → `False`, `")("` → `False`, `""` → `True`.

### B3: Divide and Conquer (22 points)

**(a)** `fast_power(base, exp)` — the function from A3(b).
**(b)** `merge(left, right)` and `merge_sort(lst)` as in L14 §2. `merge_sort([5, 2, 9, 1, 5, 6])` → `[1, 2, 5, 5, 6, 9]`.

### B4: Subsets (16 points)

`subsets(lst)` — all subsets (L15 §5): the subsets of the rest, plus each of those with the first
element added. `subsets([1, 2, 3])` has 8 elements.

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Three laws | 8 |
| A2 Recursion trees | 8 |
| A3 Induction | 14 |
| B1 Lists | 18 |
| B2 Strings | 14 |
| B3 Divide and conquer | 22 |
| B4 Subsets | 16 |
| **Total** | **100** |

---

*CS 101 · Week 4 · Problem Set 4 · Due Friday 30 October 2026, 17:00 · © CSE Department*
