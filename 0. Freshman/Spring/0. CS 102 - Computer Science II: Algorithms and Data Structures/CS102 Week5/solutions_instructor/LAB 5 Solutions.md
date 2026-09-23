# CS 102 · Lab 5 — Solutions and Checkoff Notes
## Route Planning on a Road Network

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Put the A2 reference table on the board.** As in Lab 4, everything depends on students reproducing
one specific graph, and the generator has more places to diverge than Lab 4's did — coordinate
generation order, whether $x$ or $y$ is drawn first, and the long-road acceptance test.

The specification pins all three deliberately. **If a student's $E \ne 7{,}224$, stop them and fix the
generator before they go further.**

Compute cost is small: the whole lab runs in a few seconds. Part C3's admissibility check is the only
part that does repeated full Dijkstra runs, and eight of them take about a second.

**Budget the time for Part D.** Parts A–C are mechanical for a student who has done PS 5; Part D is
where the thinking is and it should get at least 40 minutes.

---

## Part A — Build the Network (8)

### A1 (5), A2 (3) — deterministic

| quantity | value |
| --- | --- |
| $V$ | 3,600 |
| $E$ | **7,224** |
| mean degree | 4.013 |
| min / max degree | 2 / 6 |
| connected | yes |
| max distance from vertex 0 | **88.48** |

$E = 2 \cdot 60 \cdot 59 + 144 = 7080 + 144 = 7224$: the grid contributes $k(k-1)$ horizontal and
$k(k-1)$ vertical edges.

The corner junctions have degree 2, which is why `min degree = 2`. A student reporting min degree 3 or
4 has probably wrapped the grid into a torus.

---

## Part B — Dijkstra (10)

### B1 (4), B2 (3)

Expected justification: **when $t$ is popped it is finalised**, and by the correctness theorem
(Lecture 17 §2) its distance is already the true shortest distance, so no later relaxation can improve
it.

*The subtle error: breaking when $t$ is first **pushed** rather than popped. That is wrong — a pushed
distance is an upper bound, not final. It usually gives the right answer, which makes it worse. Check
the code, not the output.*

### B3 (3) — deterministic

Ten pairs from `random.seed(99)`:

| $s$ | $t$ | distance | expanded |
| --- | --- | --- | --- |
| 1654 | 1559 | 26.398 | 1,628 |
| 819 | 2455 | 37.747 | 2,226 |
| 732 | 943 | 32.359 | 1,488 |
| 1017 | 545 | 56.530 | 2,990 |
| 3112 | 354 | 47.928 | 2,256 |
| 1028 | 2986 | 56.525 | 3,191 |
| 1569 | 2174 | 13.676 | 407 |
| 2802 | 2869 | 7.704 | 132 |
| 2206 | 367 | 56.052 | 3,471 |
| 2555 | 2004 | 18.114 | 761 |
| **total** | | | **18,550** |

Expected observation: a typical query expands **1,500–3,500 of 3,600 vertices**, i.e. **40–95% of the
network**. Dijkstra explores a disc around the source and only stops when the disc reaches the target.

---

## Part C — A\* (14)

### C1 (4)

The $h \equiv 0$ check must reproduce Dijkstra's expansion counts **exactly**, not approximately. If
it does not, the student has changed something else — usually the tie-breaking or the stopping test —
and their C2 comparison is not measuring the heuristic.

### C2 (4) — deterministic

| $s$ | $t$ | Dijkstra | A\* | ratio |
| --- | --- | --- | --- | --- |
| 1654 | 1559 | 1,628 | 82 | 19.85 |
| 819 | 2455 | 2,226 | 398 | 5.59 |
| 732 | 943 | 1,488 | 130 | 11.45 |
| 1017 | 545 | 2,990 | 550 | 5.44 |
| 3112 | 354 | 2,256 | 199 | 11.34 |
| 1028 | 2986 | 3,191 | 448 | 7.12 |
| 1569 | 2174 | 407 | 59 | 6.90 |
| 2802 | 2869 | 132 | 14 | 9.43 |
| 2206 | 367 | 3,471 | 549 | 6.32 |
| 2555 | 2004 | 761 | 101 | 7.53 |
| **totals** | | **18,550** | **2,530** | **7.33** |

Distances identical in all ten.

### C3 (3) — deterministic: 0 violations of 5,760

Expected explanation: **every edge weight is exactly the Euclidean length of that edge**, so any path
is a polyline whose total length is at least the straight-line distance between its endpoints. The
heuristic is therefore a lower bound — by the triangle inequality, not by luck.

*This is the sentence that matters for Part D. A student who says "because straight lines are short"
has not identified the dependence on the weighting, and will not be able to answer D3. 1 of 3.*

### C4 (3) — deterministic: 0 suboptimal of 200

---

## Part D — Change the Cost Model (8)

### D1 (2) — deterministic

Max travel time from vertex 0: **50.36** (against a max distance of 88.48).

### D2 (3) — deterministic

| quantity | value |
| --- | --- |
| admissibility violations | **3,545 of 5,760** (62%) |
| suboptimal answers | **101 of 200** (51%) |
| worst relative error | **74.92%** |

Expected explanation: the heuristic returns a straight-line **distance**, but the quantity being
minimised is now **time**. A motorway covers that straight-line distance in $1/2.5$ of the time, so
the "estimate" now exceeds the true remaining cost and the heuristic overestimates. A\* with an
inadmissible heuristic finalises vertices too early and returns suboptimal routes.

### D3 (3) — the assessed question

The fix: **divide the heuristic by the maximum speed**, i.e.
$h(u) = \mathrm{dist}(u,t) / \texttt{SPEED}$.

| quantity | with the fix |
| --- | --- |
| admissibility violations | **0 of 5,760** |
| suboptimal answers | **0 of 200** |
| expansions over 200 queries, Dijkstra vs A\* | 354,095 vs 100,900 |
| ratio | **3.51** |

**The general rule**: an admissible heuristic must be a lower bound on the **true remaining cost in
the units being minimised**. When minimising time, divide the remaining distance by the greatest speed
achievable anywhere in the network — no route can beat that, so the estimate can never overshoot.

Expected observation about the cost: the speedup falls from **7.33× to 3.51×**. Dividing by 2.5
weakens the heuristic everywhere, including on the vast majority of edges where no motorway is
available. **Admissibility is bought with informativeness.**

*3 for the fix with verified numbers **and** the general rule. 2 for a working fix with no rule. Accept
any correct admissible heuristic — e.g. computing the true max speed from the edge data rather than
hard-coding 2.5, which is a better answer and should be praised. Award 0 for "use Dijkstra instead":
that is correct but abandons the question.*

---

## Checkoff Checklist

1. $E = 7{,}224$, min degree 2, max distance from 0 is 88.48. **Check first.**
2. A\* with $h \equiv 0$ reproduces Dijkstra's counts exactly.
3. The early exit triggers on **pop**, not on push.
4. C3's explanation names the edge weighting, not just "straight lines are shortest".
5. D3 states the general rule, not only the specific division.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 8 |
| B | 10 |
| C | 14 |
| D | 8 |
| **Total** | **40** |

Labs are pass/fail for progression: **10 of the 12 required labs (0–11).** A student who completes A–C and attempts D
passes.

---

## Note for the Week 6 Lecture

Part D is the third time this term a student has been shown a method that is correct under an
assumption, given a case where the assumption silently stops holding, and asked to notice. The
sequence is:

- **Week 3**, heap sort: an $O(1)$-space guarantee whose cost model changes once the heap leaves cache.
- **Week 5, PS 5 C**: Dijkstra correct only for non-negative weights, failing 2.3% of the time.
- **Week 5, this lab**: A\* correct only for admissible heuristics, failing 51% of the time after a
  change to the *weights* rather than the code.

**Week 6's cut property is the same shape** — Prim's and Kruskal's algorithms are correct because of a
theorem about which edges are safe, and a student who cannot say what makes a greedy choice safe will
not be able to say why either algorithm works. If Part D went badly, open Week 6 by asking what
Dijkstra and A\* each *assumed*, before introducing any new algorithm.

---

*CS 102 · Week 5 · Lab 5 Solutions · © CSE Department*
