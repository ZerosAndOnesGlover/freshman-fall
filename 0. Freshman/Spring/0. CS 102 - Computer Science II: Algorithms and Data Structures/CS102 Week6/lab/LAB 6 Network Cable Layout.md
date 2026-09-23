# CS 102 · Lab 6
## Network Cable Layout

**Date:** Tuesday 9 March 2027 · 15:00–16:50 · Lab section (Week 7) — covers Week 6 (L19–L21)
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab6.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 12 required labs (Labs 0–11) to pass the course.** See the syllabus.

---

## Purpose

You are laying fibre across a campus of 400 buildings. Every pair *could* be joined; you want every
building connected using as little cable as possible.

This is an MST, and Parts A and B are that. Part C then asks two questions the MST answers **without
being designed to**: what is the longest single cable run you must be able to make, and — more
surprisingly — how many natural groups of buildings are there.

Part D breaks the second one.

---

## Part A — Build the Campus and the MST (10 pts)

**A1.** *(4)* Implement `campus(n=400, k=5, seed=17, spread=3.0, span=100.0)`:

- Place $k$ cluster centres evenly on a circle of radius 35 about $(\texttt{span}/2, \texttt{span}/2)$,
  with centre $i$ at angle $2\pi i/k$ — centre $i$ is
  $(50 + 35\cos(2\pi i/k),\ 50 + 35\sin(2\pi i/k))$.
- Building $i$ belongs to centre $i \bmod k$ and sits at that centre plus **two independent**
  `random.gauss(0, spread)` offsets, $x$ drawn before $y$.
- `random.seed(seed)` once, before generating any building.

The graph is the **complete** Euclidean graph: every pair joined, weight the distance between them.

**A2.** *(3)* Report $n$, the number of edges, and the total cable length of the MST.

Compute it **twice** — once with Kruskal on the explicit edge list, once with $\Theta(V^2)$ Prim which
never materialises the edges — and confirm the totals agree.

**A3.** *(3)* Compare against two alternatives:

- the best **star** (one hub, its own cable to every other building — take the best hub);
- joining **every pair**.

Report both as multiples of the MST.

---

## Part B — Which Algorithm (8 pts)

**B1.** *(4)* Time all three of Kruskal, heap-Prim, and dense-Prim on this campus. Report each,
including for Kruskal and heap-Prim **the time spent building the edge list**.

**B2.** *(4)* The graph has $V = 400$ and $E = 79{,}800$ — as dense as a graph can be. State which
algorithm you would ship for this problem and why.

Your answer must mention what dense-Prim avoids doing at all.

---

## Part C — Two Questions the MST Also Answers (14 pts)

**C1.** *(4)* **The bottleneck.** Report the heaviest edge in the MST.

Then verify that it is the **minimum possible maximum edge** over all spanning trees: sort the edges,
add them in order until the graph is connected, and confirm the last edge added has that same weight.

Say in one sentence what this number means for the cable order.

**C2.** *(6)* **Clustering.** Delete the $k-1$ heaviest MST edges to leave $k$ components. For
$k = 2 \dots 6$ report the cluster sizes **and the weight of the smallest edge you deleted**.

**C3.** *(4)* You were not told how many groups of buildings there are.

- **(a)** *(2)* Read it off your C2 table. Which $k$, and what in the table tells you?
- **(b)** *(2)* Compare your $k$-clusters against the true grouping (building $i$ belongs to group
  $i \bmod 5$). Report the agreement as a percentage of vertex pairs classified consistently.

---

## Part D — Break It (8 pts)

**D1.** *(3)* Rebuild the campus with `spread=10.0`, everything else identical. The clusters now
overlap.

Rerun C2 and C3(b). Report the $k=5$ cluster sizes and the agreement.

**D2.** *(3)* You should find the sizes are badly wrong, with several one-building clusters. Name this
failure mode and explain **why single-linkage produces it** — the reason is the same property that
makes the method work in Part C.

**D3.** *(2)* Given only the MST edge weights from D1 — not the answer — could you have told that the
clustering was untrustworthy? Say what you would look for.

---

## Submission

- `lab6.py` — runnable end to end, producing every table.
- `RESULTS.md` — all tables and answers. **Include your machine and Python version.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 10 | A correct, reproducible campus and MST |
| B | 8 | Choosing an algorithm for a dense implicit graph |
| C | 14 | Bottleneck and clustering, including choosing $k$ unaided |
| D | 8 | The failure mode, and detecting it from the data |
| **Total** | **40** | |

---

## Reference Numbers

`n=400, k=5, seed=17, spread=3.0, span=100.0`, Python 3.14 on x86-64 Linux. **Deterministic.**

**A2 / A3**

| quantity | value |
| --- | --- |
| buildings | 400 |
| edges in the complete graph | **79,800** |
| **MST total cable** | **485.061** |
| MST edges | 399 |
| best single hub (star) | 16,041.893 — **33.07×** the MST |
| every pair joined | 3,549,494.3 — **7,318×** the MST |

Kruskal and dense-Prim agree exactly.

**B1** — timings, best of 5 (**machine-dependent**; the ordering is not)

| step | time |
| --- | --- |
| building the 79,800-edge list | 37.3 ms |
| Kruskal, given the edges | 84.8 ms |
| Prim (heap), given the adjacency | 218.6 ms |
| **Prim (dense), no edge list at all** | **42.0 ms** |

End to end: Kruskal 122.1 ms, heap-Prim 255.9 ms, **dense-Prim 42.0 ms** — 2.91× faster than Kruskal.
All three totals identical.

**C1**

| quantity | value |
| --- | --- |
| heaviest MST edge (bottleneck) | **27.476** |
| minimum possible maximum edge over all spanning trees | 27.476 — equal |

**C2** — cluster sizes and the smallest deleted edge

| $k$ | sizes | smallest deleted edge |
| --- | --- | --- |
| 2 | 320, 80 | 27.476 |
| 3 | 240, 80, 80 | 26.522 |
| 4 | 160, 80, 80, 80 | 25.311 |
| **5** | **80, 80, 80, 80, 80** | **23.725** |
| 6 | 80, 80, 80, 80, 79, 1 | **5.227** |

The five largest MST edges are **5.227, 23.725, 25.311, 26.522, 27.476**.

**C3** — agreement with the true grouping at $k=5$: **100.0%**.

**D1** — the same campus with `spread=10.0`

| quantity | value |
| --- | --- |
| MST total | 1,195.781 |
| bottleneck | 9.256 |
| $k=5$ cluster sizes | **237, 159, 2, 1, 1** |
| agreement | **67.1%** |

---

## A Note on What This Lab Is Really Testing

Part C2's last column is the point of the lab.

At $k = 5$ the smallest edge you delete weighs **23.725**. At $k = 6$ it weighs **5.227** — a drop of
4.5× in a single step. The four heaviest MST edges are the four links between genuinely separate
groups of buildings, and everything below them is ordinary within-group wiring. **The MST's edge
weights tell you there are five groups**, and you were never told.

That is a data structure answering a question it was not built for, and it is worth noticing how
little work it took: the clustering is three lines on top of a tree you had already computed.

**Part D is the balance.** With overlapping clusters the same method returns 237, 159, 2, 1, 1 — it
peels off individual outliers instead of finding groups. This is *chaining*, and it happens because
single-linkage judges two groups by the single shortest link between them, so one building sitting
between two clusters welds them together.

**The property that makes the method optimal is the property that makes it fragile.** Sensitivity to
the shortest link is exactly what maximises the minimum inter-cluster separation, and exactly what
lets one bridging point destroy the answer. You cannot fix one without losing the other; you can only
know which you are relying on — which is what D3 asks.

---

*CS 102 · Week 6 · Lab 6 · © CSE Department*
