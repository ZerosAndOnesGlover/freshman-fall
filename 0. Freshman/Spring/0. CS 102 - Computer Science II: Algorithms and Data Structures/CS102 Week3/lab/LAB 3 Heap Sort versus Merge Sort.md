# CS 102 · Lab 3
## Heap Sort versus Merge Sort

**Date:** Tuesday 16 February 2027 · 15:00–16:50 · Lab section (Week 4) — covers Week 3 (L10–L12)
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab3.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 12 required labs (Labs 0–11) to pass the course.** See the syllabus.

---

## Purpose

Heap sort and merge sort are both $\Theta(n\log n)$ in the worst case. Lecture 11 claimed they are
otherwise almost entirely different, and that **one of the differences does not show up in the
comparison count at all**.

This lab makes you find that difference by measurement. Part D is the assessed thinking; Parts A–C
are the apparatus.

You may use `heapq` for cross-checking only. **Both sorts must be your own.**

---

## Part A — Instrument (10 pts)

**A1.** *(4)* `heapsort(a)` — build a max-heap in place, then repeatedly swap the root to the end and
sift down over the shrinking prefix. **Ascending output.** No auxiliary list.

**A2.** *(3)* `mergesort(a)` — standard top-down. Returning a new list is fine.

**A3.** *(3)* A comparison counter for each, counting **every comparison between two elements of the
input**. For `sift_down` that is two per level: one to choose the smaller child, one to test it
against the parent. Count both.

Verify both sorts against `sorted()` on at least 200 random arrays of random lengths in $[0, 100]$
**before you time anything**, and report the count. A sort that is wrong on the empty list will
otherwise waste an hour of your session.

---

## Part B — Comparisons (10 pts)

**B1.** *(6)* For $n \in \{1000, 10000, 100000\}$ tabulate comparisons for both sorts on

- random input (mean of 5 seeds),
- already-sorted input,
- reverse-sorted input.

**B2.** *(4)* Answer in `RESULTS.md`:

- On random input, what is the ratio heap sort : merge sort? Explain the ratio **from the code** —
  which line in which routine accounts for it?
- Divide each count by $n\log_2 n$. What do the two constants converge to?
- **Heap sort does more comparisons on sorted input than on random input.** Confirm this in your own
  numbers and say what it tells you about adaptivity.

---

## Part C — Time and Space (12 pts)

**C1.** *(5)* Time both sorts on random input for $n \in \{1000, 10000, 100000, 1000000\}$, best of 3.
Report milliseconds **and microseconds per element**.

> The $n = 10^6$ run takes about **7 seconds** for heap sort on the reference machine, and it is the
> row the rest of the lab depends on. Start this timing early and do Part B while it runs.

**C2.** *(4)* Take $n = 1000$ as a baseline. For each larger $n$, report how much the **per-element**
cost grew, alongside the growth $n\log n$ predicts, namely $\log_2 n / \log_2 1000$.

You should find one sort tracking the prediction and one exceeding it.

**C3.** *(3)* Measure peak memory for both at $n = 100{,}000$ with `tracemalloc`. Report both figures
and the ratio, and say what heap sort's non-zero figure consists of.

> `tracemalloc` has not been taught, and you need only these four lines of it:
>
> ```python
> import tracemalloc
> tracemalloc.start()
> heapsort(list(a))                      # the call you are measuring
> peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()   # peak bytes since start()
> ```
>
> `list(a)` hands the sort its own copy, and that copy is inside the measurement — say so.

---

## Part D — Explain the Gap (8 pts)

**D1.** *(3)* Your C2 table shows heap sort's per-element cost growing faster than $n\log n$ predicts,
while its comparison ratio against merge sort (Part B) stays flat.

**Both cannot be explained by the comparison count.** Give the explanation, and support it by
describing the sequence of array indices `sift_down` touches on one call starting at index 0.

**D2.** *(3)* Instrument `heapsort` to report the comparisons in the **build** phase and the
**extract** phase separately, at each $n$ from C1.

The build is the $\Theta(n)$ algorithm that Lecture 11 spent three sections proving linear. What
fraction of heap sort's total work is it? What does that imply about optimising it?

**D3.** *(2)* You need to sort 50 GB of records on a machine with 4 GB of RAM, and a hard real-time
deadline. Which of the two would you start from, and what is the single biggest problem you would
still have? Two or three sentences.

---

## Submission

- `lab3.py` — runnable end to end, producing every table.
- `RESULTS.md` — the tables from B, C, D and your answers. **Include your machine and Python
  version**, as in Lab 0.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 10 | Two correct sorts, verified before measurement |
| B | 10 | Comparison counts and what explains them |
| C | 12 | Timing, per-element normalisation, space |
| D | 8 | The locality argument |
| **Total** | **40** | |

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14, x86-64 Linux). **Comparison counts are
deterministic** given the input — yours should match on the sorted and reversed rows exactly.
**Timings will differ.**

Comparisons at $n = 100{,}000$:

| input | heap sort | merge sort | ratio |
| --- | --- | --- | --- |
| random (seed 0) | 3,019,138 | 1,536,386 | 1.97 |
| sorted | 3,112,517 | 815,024 | 3.82 |
| reversed | 2,926,640 | 853,904 | 3.43 |

Time, random input, best of 3:

| $n$ | heap sort | merge sort | heap µs/elem | merge µs/elem |
| --- | --- | --- | --- | --- |
| 1,000 | 2.1 ms | 2.0 ms | 2.111 | 1.979 |
| 10,000 | 30.0 ms | 25.0 ms | 3.004 | 2.495 |
| 100,000 | 444.8 ms | 318.4 ms | 4.448 | 3.184 |
| 1,000,000 | 6922.2 ms | 4287.1 ms | 6.922 | 4.287 |

Per-element growth against the $n\log n$ prediction (C2):

| $n$ | heap sort | merge sort | predicted |
| --- | --- | --- | --- |
| 10,000 | 1.42× | 1.26× | 1.33× |
| 100,000 | 2.11× | 1.61× | 1.67× |
| 1,000,000 | 3.28× | 2.17× | 2.00× |

Heap sort phase split (D2), random input:

| $n$ | build | extract | build share |
| --- | --- | --- | --- |
| 1,000 | 1,848 | 14,973 | 11.0% |
| 10,000 | 18,795 | 216,569 | 8.0% |
| 100,000 | 188,010 | 2,831,128 | 6.2% |

Peak memory at $n = 100{,}000$ (C3): heap sort **781 KiB**, merge sort **1,687 KiB**.

---

## A Note on What This Lab Is Really Testing

Lab 2 ended by saying that the headline result was not the interesting part. The same applies here,
more sharply.

That heap sort does about twice the comparisons of merge sort is arithmetic — you could have derived
it from the code without running anything. **Part C2 measures something the comparison count cannot
see**, and the only way to notice it is to normalise your timings and find that one column does not
fit.

That is the technique to take away. When a measurement disagrees with the model, **the disagreement
is the result.** Most of what you will learn about real performance arrives this way: not from
predicting a number and confirming it, but from predicting a number, missing, and asking why.

---

*CS 102 · Week 3 · Lab 3 · © CSE Department*
