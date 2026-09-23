# CS 102 · Lab 7
## Visualising DP Tables

**Date:** Tuesday 16 March 2027 · 15:00–16:50 · Lab section (Week 8) — covers Week 7 (L22–L24)
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab7.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 12 required labs (Labs 0–11) to pass the course.** See the syllabus.

---

## Purpose

A DP table is a picture, and most people never look at one. This lab makes you print them, watch them
fill, and read structure off them that the recurrence does not make obvious.

It ends by measuring something the lectures assert: **memoisation and tabulation do different amounts
of work**, and which is better is a property of the problem rather than a matter of taste.

---

## Part A — Print the Tables (10 pts)

**A1.** *(4)* `show_table(a, b, T, title)` printing a labelled table: column headers from $b$, row
labels from $a$, right-aligned cells.

**A2.** *(3)* Print the LCS table for $a = $ `AGGTAB`, $b = $ `GXTXAYB`. It should match the reference
below exactly.

**A3.** *(3)* Print the edit-distance table for `kitten` → `sitting`, including the initialised
borders.

State what the top row and left column mean, and what would go wrong if they were all zero.

---

## Part B — The Traceback (10 pts)

**B1.** *(5)* Modify `show_table` to mark the traceback path — an asterisk, or a second table of
arrows (`↖` for a match, `↑`, `←`).

Print the marked LCS table for the Part A strings.

**B2.** *(3)* Report the sequence of moves from the bottom-right, each labelled `match`, `up`, or
`left`, and the resulting subsequence.

**B3.** *(2)* Answer both in one sentence each:

- What does a **diagonal** step mean, and why is it the only step that increases the value?
- Your traceback breaks ties with `>=`. Change it to `>` and report whether the LCS you recover
  changes for these strings, and whether its **length** could ever change.

---

## Part C — Watch It Fill (10 pts)

**C1.** *(4)* Print the LCS table after each **row** is completed, so the fill is visible as a
sequence of snapshots. Use the Part A strings.

**C2.** *(3)* A cell $(i,j)$ depends on $(i-1,j-1)$, $(i-1,j)$ and $(i,j-1)$ — all with a smaller
$i+j$.

So all cells on an **anti-diagonal** $i+j = d$ can be computed at once, given diagonals $d-1$ and
$d-2$. Print the anti-diagonal sizes for the Part A table, and give the largest.

**C3.** *(3)* Answer both:

- Row-by-row filling needs 2 rows in memory. **How much does an anti-diagonal method need?** Compare
  for a square table of side $n$.
- Name one reason you might fill by anti-diagonal anyway, despite the answer above.

---

## Part D — Memoisation Against Tabulation (10 pts)

**D1.** *(4)* Implement 0/1 knapsack **both ways**, each instrumented to count the number of distinct
subproblems it actually computes — for top-down, the size of the memo; for bottom-up, the number of
table cells.

**D2.** *(3)* Report both counts for:

| $n$ | $W$ | weights |
| --- | --- | --- |
| 20 | 1,000 | random in $[1, 100]$ |
| 20 | 10,000 | random in $[1, 100]$ |
| 10 | 100,000 | random in $[1, 100]$ |
| 20 | 10,000 | random multiples of 1,000 |

Confirm the two methods return the same value in every case.

**D3.** *(3)* Do the same comparison for **LCS** on random 200-character strings, and report the
ratio.

Then answer: the two ratios differ by three orders of magnitude. **What property of the problem
decides which method does less work?**

---

## Submission

- `lab7.py` — runnable end to end, producing every table.
- `RESULTS.md` — the tables and answers. **Include your machine and Python version.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 10 | Readable tables, and what the borders mean |
| B | 10 | The traceback and what a diagonal step is |
| C | 10 | Fill order and the dependency structure |
| D | 10 | Memoisation vs tabulation, measured |
| **Total** | **40** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **All deterministic.**

**A2 — the LCS table**

```
       -  G  X  T  X  A  Y  B
    -  0  0  0  0  0  0  0  0
    A  0  0  0  0  0  1  1  1
    G  0  1  1  1  1  1  1  1
    G  0  1  1  1  1  1  1  1
    T  0  1  1  2  2  2  2  2
    A  0  1  1  2  2  3  3  3
    B  0  1  1  2  2  3  3  4
```

LCS length **4**; the recovered subsequence is `GTAB`.

**B2 — the traceback**, from the bottom-right:

| cell | move | character |
| --- | --- | --- |
| (6,7) | match | `B` |
| (5,6) | left | |
| (5,5) | match | `A` |
| (4,4) | left | |
| (4,3) | match | `T` |
| (3,2) | up | |
| (2,2) | left | |
| (2,1) | match | `G` |

**C2 — anti-diagonal sizes** for the $6 \times 7$ interior:

$$1,\ 2,\ 3,\ 4,\ 5,\ 6,\ 6,\ 5,\ 4,\ 3,\ 2,\ 1$$

Longest wavefront: **6** cells.

**D2 — knapsack, subproblems computed**

| $n$ | $W$ | weights | top-down | bottom-up | ratio |
| --- | --- | --- | --- | --- | --- |
| 20 | 1,000 | $[1,100]$ | 5,839 | 20,020 | 3.4× |
| 20 | 10,000 | $[1,100]$ | 5,839 | 200,020 | 34.3× |
| 10 | 100,000 | $[1,100]$ | **636** | 1,000,010 | **1,572×** |
| 20 | 10,000 | multiples of 1,000 | **161** | 200,020 | **1,242×** |

**D3 — LCS, subproblems computed**

| $\lvert a\rvert = \lvert b\rvert$ | top-down | bottom-up | ratio |
| --- | --- | --- | --- |
| 200 | 28,739 | 40,000 | **1.39×** |

---

## A Note on What This Lab Is Really Testing

Parts A to C are about making an abstraction visible. The recurrence for LCS is three lines and tells
you nothing about what the computation *looks* like; the table tells you immediately that values never
decrease, that they rise only on matches, and that the whole thing is a shortest-path problem on a
grid in disguise.

**Part D is the assessed idea.** Textbooks present memoisation and tabulation as two styles with the
same complexity, and students reasonably conclude the choice is aesthetic. Your D2 table has a ratio
of **1,242×** and your D3 table has **1.39×**, for the same pair of techniques.

The property that decides it is **what fraction of the state space is reachable**. Knapsack with
capacity 10,000 and weights that are multiples of 1,000 has only eleven reachable capacities per item
— tabulation fills 200,020 cells to use 161 of them. LCS reaches essentially every $(i,j)$, so there is
nothing to save and tabulation's cheaper cells win.

**Look at your subproblem graph before choosing.** That is the whole lesson, and it costs three orders
of magnitude when ignored.

---

*CS 102 · Week 7 · Lab 7 · © CSE Department*
