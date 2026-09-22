# CS 102 · Lab 5
## Route Planning on a Road Network

**Date:** Tuesday 2 March 2027 · 15:00–16:50 · Lab section (Week 6) — covers Week 5 (L16–L18)
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab5.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 13 labs to pass the course.** See the syllabus.

---

## Purpose

Dijkstra's algorithm explores outwards in every direction until it stumbles on the destination. A
route planner that did that for a journey across a continent would examine most of the continent.

This lab builds a road network, measures how much of it Dijkstra examines, and then adds a heuristic
that cuts the work by a factor of seven **without changing a single answer**.

Then it changes the cost model from *distance* to *travel time*, and the heuristic starts returning
wrong routes. **Part D is finding out why and fixing it.**

---

## Part A — Build the Network (8 pts)

**A1.** *(5)* Implement `road_network(k=60, seed=7, jitter=0.30, n_long=144)`:

- $V = k^2$ junctions on a $k \times k$ grid. Junction $(i,j)$ is vertex $ik+j$, at coordinates
  $(j + \varepsilon,\ i + \varepsilon)$ where each $\varepsilon$ is drawn from
  `random.uniform(-jitter, jitter)`. **Generate the coordinates row by row, $i$ outer and $j$ inner**,
  drawing $x$ before $y$ for each junction.
- Connect each junction to its right and lower neighbours. **Every edge's weight is the Euclidean
  distance between its endpoints.** The graph is undirected.
- Add `n_long` "long roads": repeatedly pick two random vertices, and if they are more than $k/4$
  apart, join them with an edge of weight equal to their Euclidean distance.

Call `random.seed(seed)` once at the start, before generating any coordinates.

**A2.** *(3)* Report $V$, $E$, mean/min/max degree, whether the graph is connected, and the maximum
distance from vertex 0.

**Check against the reference table before continuing.** Everything downstream depends on this graph.

---

## Part B — Dijkstra (10 pts)

**B1.** *(4)* `dijkstra(adj, s, t=None)` returning distances and the number of vertices **expanded**
(popped and finalised). With `t` supplied, stop as soon as `t` is popped.

**B2.** *(3)* Justify the early exit in one sentence: why is `dist[t]` final at the moment `t` is
popped?

**B3.** *(3)* Using `random.seed(99)` and then ten `(random.randrange(V), random.randrange(V))` pairs,
report for each: the shortest distance, and the vertices expanded.

Roughly what fraction of the network does Dijkstra examine on a typical query?

---

## Part C — A\* (14 pts)

A\* is Dijkstra with the priority changed from $g(u)$ to $g(u) + h(u)$, where $h(u)$ estimates the
remaining distance from $u$ to the target. Use the **straight-line distance** from $u$'s coordinates
to $t$'s.

**C1.** *(4)* Implement it. Setting $h \equiv 0$ must reproduce Dijkstra exactly — check this.

**C2.** *(4)* Rerun the ten pairs from B3. Report the expansions for both algorithms and the ratio,
and confirm **the distances are identical**.

**C3.** *(3)* A heuristic is **admissible** if it never overestimates the true remaining distance.

Test yours: for several targets $t$, compute true distances to $t$ with one Dijkstra run and compare
against $h$ for many $u$. Report pairs checked and violations.

Then explain in one sentence **why** admissibility holds here — the reason is a property of how you
assigned the edge weights.

**C4.** *(3)* Run at least 200 random queries and confirm A\* returns the same distance as Dijkstra
every time. Report the number of suboptimal answers.

---

## Part D — Change the Cost Model (8 pts)

Real route planners minimise **time**, not distance. Motorways cover more distance per minute.

**D1.** *(2)* Build a second weighting of the *same* network in which every long road takes
$1/2.5$ of the time per unit length — i.e. divide those edge weights by $\texttt{SPEED} = 2.5$.
Grid roads are unchanged. Report the new maximum travel time from vertex 0.

**D2.** *(3)* Rerun C3 and C4 on the travel-time network with the **unchanged** straight-line
heuristic. Report:

- how many (u, t) pairs now violate admissibility;
- how many of 200 queries return a suboptimal route, and the worst relative error.

**D3.** *(3)* Fix it. Find a heuristic that is admissible for the travel-time network, is still
useful, and requires no extra data beyond what you already have.

Report the admissibility violations and suboptimal answers with your fix, and the expansions against
Dijkstra. **State the general rule** your fix is an instance of.

---

## Submission

- `lab5.py` — runnable end to end, producing every table.
- `RESULTS.md` — the tables and answers. **Include your machine and Python version.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 8 | A correct, reproducible network |
| B | 10 | Dijkstra with early exit, and why it is valid |
| C | 14 | A\*, admissibility, and verified optimality |
| D | 8 | The cost-model change, the failure, and the principled fix |
| **Total** | **40** | |

---

## Reference Numbers

`k=60, seed=7, jitter=0.30, n_long=144`, Python 3.14 on x86-64 Linux. **Deterministic** — if your
generator follows the specification these should match exactly.

**A2 — the network**

| quantity | value |
| --- | --- |
| $V$ | 3,600 |
| $E$ | **7,224** |
| mean degree | 4.013 |
| min / max degree | 2 / 6 |
| connected | yes |
| max distance from vertex 0 | 88.48 |

**B3 / C2 — ten pairs, `random.seed(99)`**

| $s$ | $t$ | distance | Dijkstra expanded | A\* expanded | ratio |
| --- | --- | --- | --- | --- | --- |
| 1654 | 1559 | 26.398 | 1,628 | 82 | 19.85 |
| 819 | 2455 | 37.747 | 2,226 | 398 | 5.59 |
| 732 | 943 | 32.359 | 1,488 | 130 | 11.45 |
| 1017 | 545 | 56.530 | 2,990 | 550 | 5.44 |
| 3112 | 354 | 47.928 | 2,256 | 199 | 11.34 |
| 1028 | 2986 | 56.525 | 3,191 | 448 | 7.12 |
| 1569 | 2174 | 13.676 | 407 | 59 | 6.90 |
| 2802 | 2869 | 7.704 | 132 | 14 | 9.43 |
| 2206 | 367 | 56.052 | 3,471 | 549 | 6.32 |
| 2555 | 2004 | 18.114 | 761 | 101 | 7.53 |
| **totals** | | | **18,550** | **2,530** | **7.33** |

**C3 / C4** — admissibility violations: **0 of 5,760** pairs checked. Suboptimal answers: **0 of 200**.

**D1 — travel-time network**

Max travel time from vertex 0: **50.36** (against a max *distance* of 88.48).

**D2 — travel-time network, unscaled heuristic**

| quantity | value |
| --- | --- |
| admissibility violations | **3,545 of 5,760** |
| suboptimal answers | **101 of 200** |
| worst relative error | **74.92%** |

**D3 — with a correct fix**

| quantity | value |
| --- | --- |
| admissibility violations | **0 of 5,760** |
| suboptimal answers | **0 of 200** |
| expansions, Dijkstra vs A\* (200 queries) | 354,095 vs 100,900 — ratio **3.51** |

---

## A Note on What This Lab Is Really Testing

Part C is satisfying: a 7.3× speedup for a dozen lines, with provably identical answers.

**Part D is the lesson.** Nothing about the graph changed — same junctions, same roads, same
coordinates. Only the *meaning* of the edge weights changed, from distance to time. The heuristic that
was a valid lower bound on distance is not a valid lower bound on time, and A\* silently began
returning routes up to 75% worse than optimal.

There is no error message. The code runs, returns a plausible route, and is wrong on half the queries.

**A heuristic is a claim about the cost function, not about the graph.** When the cost function
changes, every such claim must be rechecked — and the fix in D3 is not a trick, it is the general
statement of what admissibility requires. Notice also that the fix costs you something: the speedup
falls from 7.3× to 3.5×. **A weaker heuristic is still admissible and still useful; it is just less
informative.** That trade — how much you can assume against how much you gain — has been this course's
subject since Week 2.

---

*CS 102 · Week 5 · Lab 5 · © CSE Department*
