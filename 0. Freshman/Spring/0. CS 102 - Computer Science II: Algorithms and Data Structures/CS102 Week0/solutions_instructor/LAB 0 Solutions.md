# CS 102 · Lab 0 Solutions
## INSTRUCTOR ONLY

**Total: 40 points.** All code below was executed; all timings are measured, not estimated.

> **Reference machine for the timings in this document:** CPython 3, Linux x86-64, single run per
> cell, `random.seed(102)`. **Student numbers will differ and must not be marked against these.**
> Mark the *shape* and the *reasoning*.

---

## Part A — Implementations (12 pts)

```python
def insertion_sort(a):
    a = a[:]                       # copy: contract says leave input unmodified
    for j in range(1, len(a)):
        key = a[j]
        i = j - 1
        while i >= 0 and a[i] > key:
            a[i + 1] = a[i]
            i -= 1
        a[i + 1] = key
    return a


def selection_sort(a):
    a = a[:]
    for i in range(len(a)):
        m = i
        for j in range(i + 1, len(a)):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a


def merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:            # <= keeps the sort stable
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


def merge_sort(a):
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    return merge(merge_sort(a[:mid]), merge_sort(a[mid:]))
```

**Marking A (4 each):** 3 for a correct algorithm, 1 for honouring the contract (`a[:]` copy, returns
a new list). **Deduct 1** for `merge_sort` returning `a` rather than `a[:]` in the base case — it
leaks a reference to the caller's list, which is exactly the bug Part A warns about.

*Common wrong answer:* `while i >= 0 and a[i] >= key` in insertion sort — still sorts, but **destroys
stability**. Not penalised here (stability was not required) but worth a comment; it becomes a real
issue in Week 10.

---

## Part B — Verification (6 pts)

```python
import random

def check(f, trials=500):
    random.seed(0)
    for _ in range(trials):
        n = random.randint(0, 40)
        a = [random.randint(-20, 20) for _ in range(n)]   # duplicates + negatives
        expected = sorted(a)
        original = a[:]
        got = f(a)
        assert got == expected, f"{f.__name__} failed on {original}: got {got}"
        assert a == original,   f"{f.__name__} mutated its input"
    return True
```

**Verified:** all three pass 500 trials each, including $n=0$ and $n=1$.

**Marking B:** B1 3 pts — 2 for the oracle comparison, **1 for also asserting the input was not
mutated** (few students do this unprompted; award generously and point it out to those who missed
it). B2 3 pts for evidence in `RESULTS.md`.

---

## Part C — Benchmarks (14 pts)

### C1 — measured, random input (ms)

| $n$ | insertion | selection | merge |
|---|---|---|---|
| 100 | 0.17 | 0.18 | 0.17 |
| 200 | 0.72 | 0.68 | 0.34 |
| 400 | 2.98 | 3.10 | 0.79 |
| 800 | 13.59 | 12.57 | 1.36 |
| 1600 | 46.54 | 46.27 | 3.22 |
| 3200 | 190.28 | 183.00 | 6.05 |

### C2 — doubling ratios

| step | insertion | selection | merge |
|---|---|---|---|
| 100→200 | 4.15 | 3.73 | 1.99 |
| 200→400 | 4.11 | 4.54 | 2.29 |
| 400→800 | 4.57 | 4.05 | 1.73 |
| 800→1600 | 3.42 | 3.68 | 2.36 |
| 1600→3200 | 4.09 | 3.96 | 1.88 |

**The quadratic sorts cluster around 4; merge sort around 2.** Both match theory. Note the scatter —
individual ratios range 3.42–4.57 and 1.73–2.36 — which is normal single-run timing noise and is
itself worth discussing.

### C3 — input-order sensitivity at $n = 2000$ (ms)

| input | insertion | selection |
|---|---|---|
| already sorted | **0.19** | 67.43 |
| reverse sorted | **137.51** | 73.72 |
| random | 71.36 | 67.61 |

**Insertion sort spans a factor of ~700 between best and worst. Selection sort varies by under 10%.**

**Marking C:** C1 6 — full marks for a complete table with same-input-per-algorithm. C2 4 — ratios
computed and tabulated. C3 4 — three input orders, both algorithms.

> **Do not require the numbers to resemble these.** Require: quadratic ratios near 4, merge near 2,
> and a large insertion/selection asymmetry in C3.

---

## Part D — Interpretation (8 pts)

### D1 *(2)* Do the ratios match?

**Expected answer.** Broadly yes. Quadratic sorts average close to 4 and merge sort close to 2.2.
Individual steps deviate (e.g. insertion 800→1600 measured 3.42) because a single timed run is
sensitive to CPU frequency scaling, garbage collection, and background load. At small $n$ the total
time is a fraction of a millisecond, so timer resolution and interpreter warm-up are a large share of
the measurement.

**Full marks require naming at least one concrete source of noise** and the remedy (best-of-$k$ runs,
or larger $n$).

### D2 *(2)* Crossover

In the reference data merge sort is already even with the others at $n=100$ (0.17 ms across the
board) and clearly ahead by $n=200$.

**The crossover is a property of the machine and implementation, not of the algorithms.** The
asymptotic classes guarantee merge sort *eventually* wins; they say nothing about where. Constant
factors — Python function-call overhead, list slicing and allocation in `merge_sort` versus tight
in-place index arithmetic in the quadratic sorts — set the crossover point, and they change with
language, machine, and coding style.

**Award full marks only if the student says the crossover is not intrinsic.** A student answering
just "at $n=200$" gets 1.

### D3 *(2)* Why the asymmetry

**Insertion sort's inner loop is `while i >= 0 and a[i] > key`.** On already-sorted input the
condition `a[i] > key` is false immediately, so the inner loop performs **one comparison and zero
shifts** per outer iteration. Total work is $\Theta(n)$ — **insertion sort's best case is
$\Theta(n)$**, and it is *adaptive*: it exploits existing order. On reverse-sorted input every
element must travel the full distance, giving the worst case $\Theta(n^2)$.

**Selection sort's inner loop is `for j in range(i+1, len(a))`** — an unconditional scan of the entire
remaining suffix. It performs exactly $\sum_{i=0}^{n-1}(n-1-i) = \frac{n(n-1)}{2}$ comparisons **on
every input**, so best, average and worst cases are all $\Theta(n^2)$. It has no best case because
nothing in its control flow can be skipped: it must inspect every remaining element to be sure it has
found the minimum.

*(At $n=2000$: $\frac{2000 \times 1999}{2} = 1{,}999{,}000$ comparisons, regardless of input.)*

**Marking:** 1 pt for identifying the early-exit condition, 1 pt for "selection sort's inner loop is
unconditional / it has no best case". A student who answers from memory ("insertion sort is adaptive")
**without reference to the loop condition gets 1** — the question explicitly asks for the code.

### D4 *(2)* Small-$n$ constants

The reference data's smallest size, $n=100$, is already at or past the crossover, so **it does not
resolve the 10–30 element claim** — all three are 0.17–0.18 ms, within noise of each other.

A student should say the data is insufficient and propose the missing measurement: **time all three
at $n \in \{5, 10, 20, 30, 50\}$, with many repetitions per size** (each run is microseconds, so a
single run is pure noise), and look for insertion sort winning below the threshold.

**Full marks for recognising the data does not support the claim and proposing a specific fix.**
A student who asserts the data confirms it should lose 1 — **it does not**, and noticing that is the
point of the question.

---

## Marking Summary

| Part | Points |
|---|---|
| A — three implementations | 12 |
| B — verification | 6 |
| C — benchmarks | 14 |
| D — interpretation | 8 |
| **Total** | **40** |

**Checkoff standard:** a student who implemented all three correctly, verified them, and produced a
table with roughly the right shape has passed the lab, even if Part D is thin. Part D is where the
teaching happens — **give written feedback on D3 and D4 to everyone**, since those two ideas
(adaptivity, and data not supporting a claim) recur all term.

---

*CS 102 · Week 0 · Lab 0 Solutions · © CSE Department*
