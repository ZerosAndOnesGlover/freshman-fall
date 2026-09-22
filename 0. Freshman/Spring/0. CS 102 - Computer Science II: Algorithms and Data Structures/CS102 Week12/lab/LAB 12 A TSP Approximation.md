# CS 102 · Lab 12
## A TSP Approximation

**Date:** Tuesday 20 April 2027 · 15:00–16:50 · Lab section (finals week) — covers Week 12 (L37–L39)
> ⚠️ Under the "Lab *N* meets the Tuesday after Week *N*" rule this lab falls in finals week, the day
> before the CS 102 final. Moving it is an open decision recorded in the CS 102 course audit.
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab12.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **This is the last lab.** You must have satisfactorily completed **at least 10 of the 13** to pass
> the course. If you are at nine, this one is compulsory.
> **PROJECT 2 and PS 11 were due Friday 16 April. The FINAL EXAM is tomorrow, Wednesday 21 April, 09:00.**

---

## Purpose

TSP is NP-hard. This lab makes that concrete — you will watch the exact algorithm die at twenty cities
— and then builds two ways of living with it.

One has a **proof** and mediocre performance. The other has **no guarantee** and is nearly optimal.
Part D is about why you would ship the first one.

---

## Part A — Exact, and the Wall (10 pts)

**A1.** *(4)* `tsp_exact(n, D)` by Held–Karp bitmask DP (Week 8 Lecture 26).

Verify against brute-force permutation search on at least 100 instances with $n \le 8$.

**A2.** *(3)* Time it for $n \in \{8, 12, 16, 20\}$ on metric instances. Report the times alongside
$2^n n^2$.

**A3.** *(3)* From your $n = 20$ timing, **extrapolate** to $n = 25$, $n = 30$ and $n = 40$, assuming
the $2^n n^2$ growth.

Report the estimates in sensible units. Then answer: **a computer 1,000× faster — what $n$ does that
buy you?** Show the arithmetic.

---

## Part B — The MST 2-Approximation (12 pts)

**B1.** *(5)* `tsp_approx(n, D)`: build an MST (reuse Week 6's Prim), walk it in preorder, shortcut
past visited cities. Return the tour and its cost.

**B2.** *(4)* On at least 200 **metric** instances with $n \le 10$, report:

- the worst ratio approx/optimal you observe;
- the number of instances exceeding **2×** (should be zero);
- the worst ratio of **MST weight** to optimal tour (should be $\le 1$).

**B3.** *(3)* State the three steps of the proof, one line each, and say which step uses the triangle
inequality.

---

## Part C — Break the Guarantee (8 pts)

**C1.** *(4)* Generate **non-metric** instances — symmetric random edge weights, no geometry, so the
triangle inequality fails.

Run the same `tsp_approx` on at least 1,000 of them. Report the worst ratio and how many exceed 2×.

**C2.** *(4)* Answer both:

- **(a)** *(2)* Which step of your B3 proof fails, and why?
- **(b)** *(2)* For general (non-metric) TSP, no constant-factor approximation is possible unless
  P = NP. **What does that tell you that your measurement in C1 does not?**

---

## Part D — A Heuristic With No Guarantee (10 pts)

**D1.** *(4)* Implement **2-opt**: repeatedly pick two tour edges and reconnect the other way if that
shortens the tour, until no improvement exists.

Start it from your MST tour.

**D2.** *(3)* On at least 200 metric instances with $n \le 10$, report for both the MST tour and the
2-opt tour: the **mean** ratio to optimal, the **worst** ratio, and how many instances reached the
**exact** optimum.

**D3.** *(3)* You should find 2-opt is far better on every measurement.

- **(a)** *(2)* Does 2-opt have an approximation guarantee? What does your D2 table establish, and what
  does it not?
- **(b)** *(1)* You must ship one program. Which do you ship, and what do you report to the user?

---

## Submission

- `lab12.py` — runnable end to end, producing every table.
- `RESULTS.md` — all tables and answers. **Include your machine and Python version.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 10 | The exponential wall, measured and extrapolated |
| B | 12 | The 2-approximation and its proof |
| C | 8 | Removing the assumption and watching the bound fail |
| D | 10 | A heuristic that beats it, and why that is not enough |
| **Total** | **40** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Ratios are deterministic given the same instances; timings are not.**

**A2 / A3 — Held–Karp**

| $n$ | $2^n n^2$ | time |
| --- | --- | --- |
| 8 | 16,384 | 0.001 s |
| 12 | 589,824 | 0.022 s |
| 16 | 16,777,216 | 0.590 s |
| 20 | 419,430,400 | **14.8 s** |

Extrapolated: $n = 25$ ≈ **12 minutes**; $n = 30$ ≈ **9.5 hours**; $n = 40$ ≈ **2 years**.

*(These follow from the $n = 20$ timing and are machine-dependent; the orders of magnitude are not.)*

**B2 — 300 metric instances, $n = 4 \dots 10$**

| quantity | value |
| --- | --- |
| worst approx / optimal | **1.3509** |
| instances exceeding 2× | **0** |
| worst MST / optimal | **0.8286** |

**C1 — 2,000 non-metric instances**

| quantity | value |
| --- | --- |
| worst ratio | **4.000** |
| instances exceeding 2× | **42** |

**D2 — 200 metric instances, $n = 6 \dots 10$**

| method | mean ratio | worst ratio | reached the optimum |
| --- | --- | --- | --- |
| MST 2-approximation | 1.1145 | 1.3205 | — |
| **+ 2-opt** | **1.0051** | **1.1290** | **167 of 200** |

---

## A Note on What This Lab Is Really Testing

Part D produces an uncomfortable table. 2-opt averages **0.5%** above optimal and finds the exact
answer **84%** of the time. The algorithm with the theorem averages **11%** above and never provably
does better than 2×.

**On every measurement you can make, the heuristic wins.** And the answer to D3(b) is still: ship the
approximation, or ship both — because what you can tell a user about the heuristic is "it was good on
the 200 instances I tried", and what you can tell them about the 2-approximation is **"it will never be
more than twice optimal, on any input, ever"**.

Part C is the same lesson from the other side. The proof has three steps and one of them is the
triangle inequality. Remove it — change nothing else — and the worst ratio goes to 4.0 with 42
violations. **The guarantee was never a property of the code.** It was a property of the code *plus*
an assumption about the input, and the code cannot tell you when the assumption has gone.

That is where this course ends, and it is the same sentence it has been building since Week 2: **know
what your algorithm guarantees, and know what it assumed in order to guarantee it.**

---

*CS 102 · Week 12 · Lab 12 · © CSE Department*
