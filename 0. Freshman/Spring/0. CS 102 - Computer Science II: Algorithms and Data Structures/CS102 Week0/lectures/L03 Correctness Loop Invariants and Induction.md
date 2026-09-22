# CS 102 · Computer Science II
## Lecture 03: Correctness — Loop Invariants and Induction

**Date:** Friday 22 January 2027 · 09:00–09:50 · Week 0

---

## 1. Testing Is Not Proof

You wrote tests in CS 101 and you should keep writing them. But consider what a passing test suite
establishes.

```python
def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:  return mid
        elif a[mid] < target: lo = mid + 1
        else:                 hi = mid - 1
    return -1
```

Suppose this passes a thousand random tests. What have you learned? That it is correct on those
thousand inputs. For a list of 64 distinct integers there are $64!$ orderings — more than $10^{89}$ —
and you have checked $10^3$ of them.

**Tests find bugs; they do not establish their absence.** For most working software that trade is
entirely reasonable. But this course asks a different question: *why does this algorithm work, for
every input, forever?* Answering it requires a proof, and it also happens to be the fastest way to
find the bug in an algorithm that does not work.

> Dijkstra's line is worth remembering: *"Program testing can be used to show the presence of bugs,
> but never to show their absence."*

---

## 2. Loop Invariants

A **loop invariant** is a statement that is true before the loop starts, stays true across each
iteration, and — combined with the exit condition — gives you what you wanted.

The proof has exactly three parts, deliberately mirroring induction:

| Part | What you show |
| --- | --- |
| **Initialisation** | The invariant holds before the first iteration. |
| **Maintenance** | If it holds at the start of an iteration, it holds at the start of the next. |
| **Termination** | The loop ends, and the invariant plus the exit condition give the result. |

**Termination is not optional and is the part students omit.** An invariant that is maintained
forever by a loop that never exits has proved nothing.

### 2.1 Worked: insertion sort

```python
def insertion_sort(a):
    for j in range(1, len(a)):
        key = a[j]
        i = j - 1
        while i >= 0 and a[i] > key:
            a[i + 1] = a[i]
            i -= 1
        a[i + 1] = key
    return a
```

> **Invariant.** At the start of each iteration of the `for` loop, the subarray `a[0..j-1]` consists
> of the elements originally in `a[0..j-1]`, in sorted order.

**Initialisation.** Before the first iteration $j = 1$, so `a[0..0]` is a single element: trivially
sorted, and trivially the original element. ✓

**Maintenance.** The inner `while` shifts every element greater than `key` one position right, then
places `key` in the gap. Elements $\le$ `key` are untouched and remain in order; shifted elements
keep their relative order; `key` lands after everything $\le$ it and before everything $>$ it. So
`a[0..j]` is sorted and contains exactly the original elements of `a[0..j]`. ✓

**Termination.** The `for` loop ends when $j = n$. The invariant then says `a[0..n-1]` — the whole
array — holds the original elements in sorted order. **That is the definition of a correct sort.** ∎

Notice what the invariant did: it converted a question about a loop running an unknown number of
times into three finite checks.

### 2.2 The invariant for binary search

> **Invariant.** At the start of each iteration, if `target` is present in the original array, its
> index lies in `[lo, hi]`.

**Initialisation.** `lo, hi = 0, n-1` — the whole array. ✓

**Maintenance.** The array is sorted. If `a[mid] < target`, then every index $\le$ `mid` holds a
value $\le$ `a[mid]` $<$ `target`, so `target` cannot be there; restricting to `[mid+1, hi]` is safe.
Symmetrically for the other branch. ✓

**Termination.** Each iteration strictly shrinks `hi - lo`, so the loop ends. It exits either by
returning `mid` on a hit, or with `lo > hi` — an empty range, which by the invariant means `target`
was never present, so `-1` is correct. ∎

**The sortedness assumption is where the proof would fail** on unsorted input, and that is exactly
where the algorithm fails. A good proof localises the assumption that matters.

---

## 3. Induction for Recursive Algorithms

Recursive algorithms are proved by induction on the input size — the same three parts wearing
different names.

### Worked: merge sort

```python
def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left  = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return merge(left, right)
```

**Claim.** `merge_sort(a)` returns a sorted permutation of `a`, for every list `a`.

**Base case.** $n \le 1$: a list of zero or one element is sorted and is a permutation of itself. ✓

**Inductive step.** Assume the claim for all lists of length $< n$ (**strong** induction — note that
we need it for *both* halves, and neither has length $n-1$). For $|a| = n \ge 2$ we have
$1 \le \texttt{mid} < n$, so both slices are strictly shorter and the hypothesis applies: `left` and
`right` are sorted permutations of their halves. Given `merge` correctly merges two sorted lists into
one sorted list containing exactly their combined elements, the result is a sorted permutation of
`a`. ∎

**Two things to notice.**

First, **the proof is only as good as its assumption about `merge`** — which needs its own proof, by
loop invariant. Decomposing correctness the way you decompose code is the normal practice.

Second, **strong induction is required**, not ordinary induction. This is the kind of thing MATH 151
covered and this course now silently relies on.

### Why `mid = len(a) // 2` matters

If `mid` could be $0$, then `a[:0]` is empty and `a[0:]` is all of `a` — the recursion would never
shrink and would not terminate. For $n \ge 2$, `n // 2` $\ge 1$ and `n // 2` $< n$, so both halves
are non-empty and strictly shorter.

**Termination arguments in recursion are about a strictly decreasing measure bounded below.** Here
that measure is the list length.

---

## 4. Common Failures in Correctness Arguments

| Failure | What it looks like | Why it is not a proof |
| --- | --- | --- |
| Restating the code | "The loop adds each element to the sum, so the sum is correct." | Says *what* happens, not *why* it gives the answer. |
| Omitting termination | Initialisation and maintenance, then stop. | An invariant maintained by an infinite loop proves nothing. |
| Assuming the conclusion | "Since the array is sorted after the loop…" | That is what you are trying to establish. |
| Ordinary induction where strong is needed | Assuming only $n-1$ for a divide-and-conquer algorithm. | The halves are not of size $n-1$. |
| Proving on an example | Tracing $n = 5$ and declaring it general. | Establishes one input. |

---

## 5. What This Buys You

Three concrete things this term.

**It localises assumptions.** Binary search's proof used sortedness exactly once, at maintenance —
telling you precisely what you may not violate. In Week 5 the same discipline shows why Dijkstra
needs non-negative weights: the proof breaks at exactly one step, and that step tells you what
Bellman-Ford must do differently.

**It finds bugs faster than debugging.** When an algorithm is wrong, attempting the maintenance step
usually fails at the specific line containing the error.

**It is how you will know your own new algorithm is right.** From Week 7 you will design algorithms
nobody has handed you. There is no reference implementation to compare against. **The proof is the
only thing standing between you and a plausible algorithm that is wrong.**

---

## 6. Exercises

*Work these before Week 1. They are not collected, and Quiz 1 draws on them.*

**1.** State and prove a loop invariant for:
```python
def maximum(a):
    m = a[0]
    for i in range(1, len(a)):
        if a[i] > m:
            m = a[i]
    return m
```

**2.** State a loop invariant for selection sort. What is the exit condition, and how does the
invariant plus the exit condition give sortedness?

**3.** The binary search above computes `mid = (lo + hi) // 2`. In a language with fixed-width
integers this can overflow when `lo + hi` exceeds the maximum. Give an expression computing the same
midpoint without that risk, and argue it is equal for all `0 <= lo <= hi`.

**4.** Prove by induction that this returns $a^n$ for $n \ge 0$, and give a recurrence for its
running time:
```python
def power(a, n):
    if n == 0:            return 1
    half = power(a, n // 2)
    if n % 2 == 0:        return half * half
    else:                 return half * half * a
```

**5.** Below is a *wrong* binary search. Attempt the maintenance step of the invariant proof, and
report the precise point at which it fails.
```python
def broken_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] == target:  return mid
        elif a[mid] < target: lo = mid
        else:                 hi = mid
    return -1
```

---

*CS 102 · Week 0 · Lecture 03 · © CSE Department*
