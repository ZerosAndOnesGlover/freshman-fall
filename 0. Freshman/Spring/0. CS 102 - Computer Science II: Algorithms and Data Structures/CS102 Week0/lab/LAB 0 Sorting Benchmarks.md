# CS 102 · Lab 0
## Implement and Benchmark Three Sorting Algorithms

**Week 0 · 2-hour lab session · 40 points**
**Deliverable:** `lab0.py` and a short `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102. They are still required: **you must satisfactorily
> complete at least 10 of the 13 labs to pass the course.** See the syllabus.

---

## Purpose

Two things, one practical and one conceptual.

**Practical:** reconnect your hands to CS 101 material before Week 1 raises the pace.

**Conceptual:** make the gap between $\Theta(n^2)$ and $\Theta(n\log n)$ something you have
**measured** rather than been told. Lecture 02 gave you a table of numbers. This lab makes you
produce your own, and — more importantly — makes you check whether they match the theory.

---

## Part A — Implement (12 pts)

Implement three sorts from CS 101, **from scratch**. `list.sort()` and `sorted()` are forbidden in
this part; you will use them only as a correctness oracle in Part B.

**A1.** *(4)* `insertion_sort(a)` — returns a new sorted list, leaves `a` unmodified.

**A2.** *(4)* `selection_sort(a)` — same contract.

**A3.** *(4)* `merge_sort(a)` — same contract. Write `merge(left, right)` as a separate function; you
will reason about it in Part D.

**All three must return a new list.** A function that sorts in place and also returns the list will
silently corrupt your benchmark, because the second algorithm you time will receive already-sorted
input. **This is the most common way to get nonsense results in this lab**, and finding it is part of
the exercise.

---

## Part B — Verify Before You Measure (6 pts)

**B1.** *(3)* Write `check(f)` that runs `f` against `sorted()` on at least 500 random lists, with
lengths from 0 to 40 and values that **include duplicates and negatives**. It should raise or report
on the first mismatch.

**B2.** *(3)* Confirm all three pass. Include the output in `RESULTS.md`.

> **Do this before timing anything.** Benchmarking an incorrect algorithm is a way to spend an hour
> producing meaningless numbers. Empty lists, single-element lists, all-equal lists, and
> already-sorted lists are where these three break.

---

## Part C — Benchmark (14 pts)

**C1.** *(6)* Time all three on **random** input for $n \in \{100, 200, 400, 800, 1600, 3200\}$. Use
`time.perf_counter()`. Give every algorithm **the same input list** at each $n$.

Produce a table of milliseconds.

**C2.** *(4)* For each algorithm and each consecutive pair of sizes, compute the **doubling ratio** —
time at $2n$ divided by time at $n$. Tabulate it.

Theory predicts:

| Complexity | Predicted doubling ratio | Why |
| --- | --- | --- |
| $\Theta(n^2)$ | $\approx 4$ | $(2n)^2 / n^2 = 4$ |
| $\Theta(n\log n)$ | $\approx 2.2$–$2.3$ | $\frac{2n\log 2n}{n\log n} = 2\left(1 + \frac{1}{\log_2 n}\right)$ |

Evaluate that formula yourself at each $n$ before comparing — it is **not** a constant $2$, and it
drifts downward as $n$ grows (2.30 at $n=100$, 2.19 at $n=1600$). Comparing your measurements against
a flat $2$ will make correct data look wrong.

**C3.** *(4)* Now vary the *input order* rather than the size. Fix $n = 2000$ and time
`insertion_sort` and `selection_sort` on three inputs: **already sorted**, **reverse sorted**, and
**random**.

You should find a large asymmetry between the two algorithms. **Explain it from the code**, not from
memory.

---

## Part D — Interpret (8 pts)

Answer in `RESULTS.md`. One short paragraph each; the marks are for the reasoning.

**D1.** *(2)* Do your doubling ratios match the predictions? Where they do not, give a reason. At
small $n$ they usually do not — say why measurement is unreliable there.

**D2.** *(2)* At which $n$ does merge sort first beat both quadratic sorts in your data? Is that
crossover a property of the algorithms or of your machine? Justify.

**D3.** *(2)* From C3: why is insertion sort dramatically faster on sorted input while selection sort
is essentially unaffected? Answer by reference to the loop structure of each. **What is insertion
sort's best-case complexity, and why does selection sort have no comparable best case?**

**D4.** *(2)* Lecture 02 claimed constants can dominate at small $n$, and that real library sorts
switch to insertion sort below a threshold of roughly 10–30 elements. **Does your data support
that?** If your smallest $n$ is too large to tell, say what measurement you would add.

---

## Submission

- `lab0.py` — the three sorts, `check`, and your benchmarking code, runnable end to end.
- `RESULTS.md` — your tables from C1–C3 and your answers to D1–D4.

**Include your machine and Python version in `RESULTS.md`.** Timings are meaningless without them,
and the habit of reporting the conditions of a measurement is one this course will keep asking for.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 12 | Three correct implementations, correct contract |
| B | 6 | Verification before measurement |
| C | 14 | Benchmarks, doubling ratios, input-order study |
| D | 8 | Interpretation |
| **Total** | **40** | |

---

## A Note on Getting Anomalous Results

**Your numbers will not match anyone else's, and they do not need to.** Different machines, different
Python versions, background load, and CPU frequency scaling all move absolute timings.

What should be robust is the **shape**: quadratic sorts roughly quadrupling per doubling, merge sort
roughly doubling. If your shape is wrong, that is a finding worth reporting, and the two usual causes
are (a) an in-place sort mutating the shared input, per the warning in Part A, and (b) timing a
single run rather than taking a best-of-several.

**Reporting an anomaly you investigated honestly earns full marks in D1.** Reporting clean numbers
you did not check earns fewer.

---

*CS 102 · Week 0 · Lab 0 · © CSE Department*
