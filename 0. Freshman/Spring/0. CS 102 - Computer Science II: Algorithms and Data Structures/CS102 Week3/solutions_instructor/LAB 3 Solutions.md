# CS 102 · Lab 3 — Solutions and Checkoff Notes
## Heap Sort versus Merge Sort

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Run the reference script yourself on the lab machines.** Part C1's $n = 10^6$ row takes about
**7 seconds** for heap sort and **4.3 seconds** for merge sort on the reference machine; on a slower
lab machine, budget 20 seconds per timed repetition and therefore about two minutes for C1 as
specified (best of 3, two sorts, four sizes). **That is the single biggest schedule risk in this
lab** — tell students at the start to launch C1 and do Part B while it runs, as the handout says.

If the lab machines cannot manage $n = 10^6$ inside the session, **drop to $n = 400{,}000$ rather
than dropping the row.** The row is what makes Part D visible; without it C2's effect is only
2.11× against 1.67× and students reasonably call it noise.

---

## Part A — Instrument (10)

### A1 (4)

```python
CMP = 0

def sift_down_max(a, i, n):
    global CMP
    while True:
        l, r, m = 2*i + 1, 2*i + 2, i
        if l < n:
            CMP += 1
            if a[l] > a[m]: m = l
        if r < n:
            CMP += 1
            if a[r] > a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]
        i = m

def heapsort(a):
    n = len(a)
    for i in range(n//2 - 1, -1, -1):
        sift_down_max(a, i, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down_max(a, 0, end)
    return a
```

**The `n` parameter to `sift_down_max` is the whole trick of the extract loop** — the heap shrinks
while the array does not. A student who calls `sift_down_max(a, 0, len(a))` in the second loop will
sort nothing and be baffled; it is the most common A1 failure.

*3 for a correct in-place heap sort, 1 for ascending output from a max-heap. A student who builds a
min-heap and reverses at the end has not done A1 — send them back, it is 30 seconds of work and the
point of the exercise.*

### A2 (3), A3 (3)

For A3, comparisons must count **both** the child-selection comparison and the parent test. A student
counting one per level will report roughly half the expected figure and their B2 ratio will come out
near 1.0 instead of 1.97. **If a submission's heap-sort count is close to merge sort's, check the
counter before believing the analysis.**

Expected A3 report: 200+ trials, 0 failures, **including the empty list and single-element list**.

---

## Part B — Comparisons (10)

### B1 (6) — deterministic on the sorted/reversed rows

$n = 100{,}000$:

| input | heap sort | merge sort | ratio |
| --- | --- | --- | --- |
| random (seed 0) | 3,019,138 | 1,536,386 | 1.97 |
| sorted | 3,112,517 | 815,024 | **3.82** |
| reversed | 2,926,640 | 853,904 | **3.43** |

Smaller sizes, random, mean of 5 seeds:

| $n$ | heap sort | merge sort | heap$/n\log_2 n$ | merge$/n\log_2 n$ |
| --- | --- | --- | --- | --- |
| 1,000 | 16,833 | 8,705 | 1.69 | 0.87 |
| 10,000 | 235,359 | 120,417 | 1.77 | 0.91 |
| 100,000 | 3,019,554 | 1,536,292 | 1.82 | 0.92 |

**Mark the sorted and reversed rows exactly.** They do not depend on a seed.

### B2 (4)

Expected answers:

- **Ratio $\approx 1.97$**, accounted for by the two comparisons per level inside `sift_down` — the
  child selection and the parent test — against merge sort's single comparison per output element.
  *A student who says "heap sort is just worse" without locating the line scores 0 of this mark.*
- **Constants:** heap sort $\to$ about $1.8$–$2.0$, merge sort $\to$ about $0.92$. Heap sort tends to
  $2n\log_2 n$; merge sort's exact worst case is
  $n\lceil\log_2 n\rceil - 2^{\lceil\log_2 n\rceil} + 1$, a little below $n\log_2 n$.
  *(Verified exhaustively: the maximum over all $n!$ permutations equals this formula for every
  $n \le 9$ — 0, 1, 3, 5, 8, 11, 14, 17, 21.)*
- **Adaptivity:** heap sort does **more** work on sorted input (3,112,517) than on random
  (3,019,138). It is not adaptive — pre-existing order is not merely unhelpful, it is very slightly
  harmful, because an ascending array is close to a *min*-heap and therefore a badly arranged max-heap.
  Merge sort halves its count on sorted input because the merge exhausts one run before the other.

*Full marks require noticing that heap sort's sorted-input count is larger, not just "about the
same." It is a 3.1% increase and students who round it away should be corrected — this is the
observation that motivates Timsort in Week 10's reading.*

---

## Part C — Time and Space (12)

### C1 (5) — machine-dependent

| $n$ | heap sort | merge sort | heap µs/elem | merge µs/elem |
| --- | --- | --- | --- | --- |
| 1,000 | 2.1 ms | 2.0 ms | 2.111 | 1.979 |
| 10,000 | 30.0 ms | 25.0 ms | 3.004 | 2.495 |
| 100,000 | 444.8 ms | 318.4 ms | 4.448 | 3.184 |
| 1,000,000 | 6922.2 ms | 4287.1 ms | 6.922 | 4.287 |

Mark the **shape**, not the values: heap sort slower at every size, the gap widening from about 1.07
to about 1.6.

### C2 (4) — the assessed table

| $n$ | heap sort | merge sort | $\log_2 n / \log_2 1000$ |
| --- | --- | --- | --- |
| 10,000 | 1.42× | 1.26× | 1.33× |
| 100,000 | 2.11× | 1.61× | 1.67× |
| 1,000,000 | **3.28×** | 2.17× | **2.00×** |

**Merge sort tracks the prediction (within 9% at $10^6$); heap sort exceeds it by 64%.**

*A student whose heap-sort column tracks the prediction has almost certainly timed a run that fits in
cache, or reused one array across repetitions so that later runs sort an already-sorted array. Check
that they re-copy the input before each timed repetition — this is the most common silent error in the
lab, and it makes Part D unanswerable.*

### C3 (3)

Peak `tracemalloc` at $n = 100{,}000$: heap sort **781 KiB**, merge sort **1,687 KiB**, ratio **2.2×**.

Heap sort's figure is entirely the defensive `list(xs)` copy. A student who sorts the caller's list in
place will report ~0 KiB and should be given full marks with a note — that is the correct answer for
a true in-place sort, and it is worth saying so at checkoff.

---

## Part D — Explain the Gap (8)

### D1 (3) — the assessed question

Expected: **memory locality / cache behaviour.**

`sift_down` starting at index 0 touches indices $0 \to 1 \to 3 \to 7 \to 15 \to 31 \to \dots$, i.e.
roughly $2^k$. **The stride doubles at every step**, so consecutive accesses move exponentially
further apart. Once the heap exceeds the cache, the deep levels of every sift are effectively random
access, and a heap of $10^6$ floats is far past that on any current machine. Merge sort's inner loop
reads two sequential runs and writes one, which is the access pattern hardware prefetchers exist for.

*2 for identifying locality, 1 for a concrete index sequence. Accept "cache misses" for the 2 marks
only with some mechanism attached; the bare phrase is worth 1.*

Two wrong answers to watch for, both plausible:

- **"Python's memory management / garbage collection."** Merge sort allocates far more than heap sort
  and is faster, so allocation cost cannot be the explanation. Ask the student to reconcile their
  answer with their own C3 table.
- **"Heap sort does more comparisons."** True but already accounted for — the comparison ratio is
  flat at 1.97 across all sizes while the time ratio grows from 1.07 to 1.61. A constant cannot
  explain a trend. **This is the answer to look for and reject**, because it sounds right.

### D2 (3)

| $n$ | build | extract | build share |
| --- | --- | --- | --- |
| 1,000 | 1,848 | 14,973 | 11.0% |
| 10,000 | 18,795 | 216,569 | 8.0% |
| 100,000 | 188,010 | 2,831,128 | **6.2%** |

Expected implication: **the $\Theta(n)$ build is a shrinking minority of heap sort's work, so
optimising it further cannot help much** — even eliminating it entirely would save 6% at $n = 10^5$,
and less at larger $n$. Amdahl's law, arrived at empirically.

The linear build earns its three lectures because it is used **on its own** — `heapify`, top-$k$,
Dijkstra's initialisation — not because of what it does for heap sort.

*3 for the table plus the implication. 1 for the table alone. A student who concludes "so the linear
build doesn't matter" has missed the second half and should get 2.*

### D3 (2)

Expected: **start from merge sort.** External sorting is merge sort — sort runs that fit in memory,
write them out, then $k$-way merge them, which is exactly `heapq.merge` from Lecture 12 §7 and
exactly the structure of Part A2. Heap sort's $O(1)$ space is worthless here because the array does
not fit in memory in the first place, and its access pattern is catastrophic on disk for the same
reason it is bad in cache — Week 2's B-tree lecture made this point about the same hardware.

The remaining problem: **I/O, not comparisons.** 50 GB through 4 GB of RAM means at least two full
passes over the data, and the run count and buffer sizes must be tuned to the device rather than to
the comparison count.

*Full marks for merge sort plus an I/O-shaped concern. 1 for merge sort with a weak justification.
A student choosing heap sort for its space bound has misread the problem — the space bound is on
**auxiliary** space, and the data itself is what does not fit.*

---

## Checkoff Checklist

At the bench, verify in this order:

1. Both sorts handle `[]` and `[1]`. *(30 seconds, catches a third of the failures.)*
2. Input is re-copied before every timed repetition. *(Otherwise C2 is meaningless.)*
3. Heap sort's comparison counter counts two per level. *(Otherwise B2's ratio is wrong.)*
4. The extract loop passes the shrinking `end`, not `len(a)`.
5. C1 includes the $n = 10^6$ row, or a documented substitute.
6. D1 says "locality," not "more comparisons."

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 10 |
| B | 10 |
| C | 12 |
| D | 8 |
| **Total** | **40** |

Labs are pass/fail for progression: **10 of the 12 required labs (0–11).** Record the score for feedback, but a
student who completes A–C and answers D1 wrongly still passes the lab.

---

## Note for the Week 4 Lecture

If a substantial fraction of the cohort answered D1 with "more comparisons," **spend five minutes on
it at the start of Week 4.** The transferable skill is recognising that *a constant factor cannot
explain a trend* — and Week 4 opens with graph representations, where the adjacency-matrix versus
adjacency-list comparison has exactly the same structure: two options whose ranking depends on a
property the asymptotic notation does not mention.

---

*CS 102 · Week 3 · Lab 3 Solutions · © CSE Department*
