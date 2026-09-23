# CS 102 · Lab 11
## A 2-D Nearest-Neighbour Searcher

**Date:** Tuesday 13 April 2027 · 15:00–16:50 · Lab section (Week 12) — covers Week 11 (L34–L36)
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab11.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 12 required labs (Labs 0–11) to pass the course.** See the syllabus.
> **PROJECT 2 is due Friday of Week 12.** This is Lab 11 of the 12 required.

---

## Purpose

Build a k-d tree, verify it, and measure what it buys — a factor of several hundred in two dimensions.

Then keep the code identical and raise the dimension until the speedup becomes a **slowdown**. Part C
is finding that point, and it is the lab.

---

## Part A — Build and Verify (14 pts)

**A1.** *(6)* `build(points, depth=0, k=2)` constructing a k-d tree by cycling through the axes and
splitting at the median.

**A2.** *(5)* `nearest(node, q)` returning the nearest point and its squared distance, with the
pruning test.

Instrument it to count **nodes visited**.

> Work in **squared** distances throughout. No square roots are needed anywhere in this lab, and
> avoiding them keeps integer inputs exact.

**A3.** *(3)* Verify against brute force on at least 300 random 2-D queries with integer coordinates.
Report mismatches.

**Do this before timing anything.** A pruning test with the wrong inequality is fast and wrong.

---

## Part B — What It Buys in 2-D (12 pts)

**B1.** *(5)* For $n \in \{1000, 8000, 64000\}$ random 2-D points, report the mean nodes visited over
200 queries and the mean query time, against brute force.

**B2.** *(4)* Plot or tabulate mean nodes visited against $n$. State the growth you observe and the
complexity it suggests.

**B3.** *(3)* Report the **build** time alongside the query time.

At how many queries does building the tree pay for itself? Show the arithmetic.

---

## Part C — The Curse of Dimensionality (14 pts)

**C1.** *(6)* Generalise your tree to $d$ dimensions — it should already work if `build` takes `k`.

For $n = 8192$ and $d \in \{2, 4, 8, 16, 32\}$, report the mean nodes visited over 200 queries, that
as a **percentage of $n$**, and the mean query time for both the tree and brute force.

**Spot-check correctness at every dimension** — the tree stays correct throughout, and saying so is
part of the result.

**C2.** *(5)* Identify the dimension at which the k-d tree stops being faster than a linear scan.

Then explain **why the pruning test stops firing**. Your answer must refer to what the test compares.

**C3.** *(3)* At $d = 32$ your tree visits every node and is slower than brute force.

- **(a)** *(2)* Is the tree **incorrect** at $d = 32$? Answer precisely, and say what that implies
  about testing.
- **(b)** *(1)* Name one technique used in practice for high-dimensional nearest-neighbour search.

---

## Submission

- `lab11.py` — runnable end to end, producing every table.
- `RESULTS.md` — the tables and answers. **Include your machine and Python version.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 14 | A correct tree, verified before measurement |
| B | 12 | What it buys in 2-D |
| C | 14 | Where it stops buying anything |
| **Total** | **40** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Node counts are deterministic given the same points; timings are not.**

**C1 — $n = 8192$, 200 queries per dimension**

| $d$ | nodes visited | % of $n$ | brute force | k-d tree | verdict |
| --- | --- | --- | --- | --- | --- |
| 2 | **20** | **0.2%** | 6.75 ms | **0.02 ms** | 337× faster |
| 4 | 62 | 0.8% | 8.73 ms | 0.09 ms | 97× faster |
| 8 | 787 | 9.6% | 13.61 ms | 1.78 ms | 7.6× faster |
| **16** | **8,071** | **98.5%** | 22.49 ms | **25.06 ms** | **slower** |
| 32 | 8,192 | **100.0%** | 37.72 ms | 42.94 ms | slower |

**The tree returns the correct nearest neighbour at every dimension.** Only its usefulness changes.

---

## A Note on What This Lab Is Really Testing

Part B is the advertisement: 20 nodes visited out of 8,192, and a query 337× faster than a scan. That
is what a spatial index is for, and it is a genuinely large win.

**Part C is the calibration, and C3(a) is the graded question.**

At $d = 32$ the k-d tree visits all 8,192 points and takes longer than a brute-force scan. It is
**still correct** — it returns the true nearest neighbour, in every dimension, on every query. Nothing
you could write as a test would fail.

**What fails is not the algorithm but the reason for choosing it.** The tree exists to prune, and its
pruning test compares one coordinate's contribution against the total distance. In high dimensions the
total is spread over many coordinates, so one coordinate is a small fraction of it, and a small
fraction almost never exceeds the whole.

There is a deeper problem underneath, which is worth knowing even though the lab does not measure it:
in high dimensions, the nearest and farthest points from a query become nearly equidistant. **When
everything is about the same distance away, "nearest neighbour" stops being a useful question at all**,
and no data structure can fix a question that has stopped meaning anything.

That is the last measurement in this course, and it is the right note to end the practical work on. You
have spent twelve weeks learning to choose structures by their guarantees. **This one keeps every
guarantee it ever made and stops being worth using**, and the only way to find that out was to measure
it.

---

*CS 102 · Week 11 · Lab 11 · © CSE Department*
