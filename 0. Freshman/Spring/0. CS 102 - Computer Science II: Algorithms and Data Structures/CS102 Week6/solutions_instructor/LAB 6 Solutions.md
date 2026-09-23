# CS 102 · Lab 6 — Solutions and Checkoff Notes
## Network Cable Layout

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Put the A2 reference figures on the board**: 400 buildings, 79,800 edges, MST total **485.061**. As
in Labs 4 and 5, everything after Part A depends on reproducing one specific point set.

The generator has three places to diverge and the handout pins all three: the centres are on a
radius-35 circle at angles $2\pi i/k$; building $i$ belongs to centre $i \bmod k$; and $x$ is drawn
before $y$ for each building. **If a student's MST total is not 485.061, fix the generator first.**

Compute cost is small — the whole lab is a few seconds. **Part C3 and Part D are where the thinking
is**; budget at least 45 minutes for them and do not let students spend the session tuning timings.

---

## Part A — Build the Campus and the MST (10)

### A1 (4), A2 (3) — deterministic

| quantity | value |
| --- | --- |
| buildings | 400 |
| edges in the complete graph | **79,800** = $\binom{400}{2}$ |
| **MST total cable** | **485.061** |
| MST edges | 399 |

Kruskal and dense-Prim agree exactly. A student whose two methods disagree has usually written
dense-Prim with `best[]` initialised to the distance from vertex 0 rather than to infinity.

### A3 (3) — deterministic

| alternative | total | multiple of MST |
| --- | --- | --- |
| best single hub (star) | 16,041.893 | **33.07×** |
| every pair joined | 3,549,494.3 | **7,318×** |

Worth saying aloud: the star is the layout a naive designer proposes, and it costs **33 times** as much
cable. This is the cheapest possible motivation for the whole week.

---

## Part B — Which Algorithm (8)

### B1 (4) — machine-dependent, ordering is not

| step | time |
| --- | --- |
| building the 79,800-edge list | 37.3 ms |
| Kruskal, given the edges | 84.8 ms |
| Prim (heap), given the adjacency | 218.6 ms |
| **Prim (dense)** | **42.0 ms** |

End to end: Kruskal **122.1 ms**, heap-Prim **255.9 ms**, dense-Prim **42.0 ms**.

### B2 (4)

Expected: **ship dense-Prim.** The graph is complete, so $E = \Theta(V^2)$ and a heap buys nothing —
$O(E\log V)$ is worse than $\Theta(V^2)$ here. More importantly, **dense-Prim never materialises the
edge list at all**: it computes each distance on demand inside the scan. Building the 79,800-edge list
costs 37.3 ms before either other algorithm starts, and at $V = 4{,}000$ that list would have eight
million entries.

*2 for choosing dense-Prim, 2 for identifying that it avoids constructing the edges. A student who
says "Prim is better for dense graphs" without the implicit-graph point scores 2 of 4 — that is the
textbook answer, and the reason it is right **here** is the memory, not the $\log V$.*

> **Contrast with Lecture 20 §4 deliberately.** There, on explicit sparse edge lists, Kruskal beat Prim
> at every size including dense ones. Here Prim wins by 2.9×. **The difference is whether the edge
> list has to exist**, and a student who noticed the apparent contradiction and resolved it deserves
> credit in the feedback.

---

## Part C — Two Questions the MST Also Answers (14)

### C1 (4) — deterministic

Heaviest MST edge: **27.476**. Adding edges in weight order until connected produces the same value.

Expected sentence: it is the **shortest cable reel that could possibly suffice** — no spanning layout
exists whose longest single run is shorter. Anything less and some pair of buildings cannot be joined.

### C2 (6) — deterministic

| $k$ | sizes | smallest deleted edge |
| --- | --- | --- |
| 2 | 320, 80 | 27.476 |
| 3 | 240, 80, 80 | 26.522 |
| 4 | 160, 80, 80, 80 | 25.311 |
| **5** | **80, 80, 80, 80, 80** | **23.725** |
| 6 | 80, 80, 80, 80, 79, 1 | **5.227** |

### C3 (4) — the assessed question

**(a) (2)** $k = 5$. The evidence is the last column: the four deleted edges are 23.7 to 27.5 — all
comparable — and the fifth is **5.227**, a drop of **4.5×**. Above the gap you are cutting genuine
links between separated groups; below it you are cutting ordinary within-group wiring. The number of
edges above the gap is the number of clusters minus one.

Corroborating evidence in the sizes column: $k=5$ gives five equal groups, and $k=6$ immediately peels
off a **single building** — the signature of having gone one step too far.

**(b) (2)** Agreement with the true grouping at $k=5$: **100.0%**.

*2 for naming $k=5$ **with the gap as the reason**. A student who says "because the sizes are equal at
k=5" has used a fact they would not have in a real dataset — give 1, and point out that the last column
is the one that generalises.*

---

## Part D — Break It (8)

### D1 (3) — deterministic

`spread=10.0`:

| quantity | value |
| --- | --- |
| MST total | 1,195.781 |
| bottleneck | 9.256 |
| $k=5$ cluster sizes | **237, 159, 2, 1, 1** |
| agreement | **67.1%** |

### D2 (3)

The failure mode is **chaining**.

Expected explanation: single-linkage measures the distance between two groups by the **single shortest
link** between them. When clusters overlap, a few buildings sit in the gap and form a chain of short
hops from one group to the next, so the MST never contains a long edge separating them. The heaviest
MST edges are then not inter-cluster links at all but the connections to isolated outliers — so
deleting them peels off single points instead of splitting groups.

**And it is the same property that made Part C work.** Judging by the shortest link is exactly what
maximises the minimum separation between clusters, and exactly what lets one bridging building weld two
clusters together. You cannot have one without the other.

*3 requires naming chaining **and** connecting it to Part C's optimality. 1 for "the clusters overlap
so it fails".*

### D3 (2)

Expected: **look at the largest MST edge weights for a gap.** In Part C they were 27.5, 26.5, 25.3,
23.7, then 5.2 — an obvious break. In Part D the top weights are all small and closely spaced (the
bottleneck is only 9.256 against a within-cluster scale that has also grown), so there is **no gap to
find**, and that absence is the warning.

The general statement: *if the MST edge weights show no clear separation, the data has no clear
cluster structure at this scale, and any $k$ you choose is arbitrary.*

*2 for "look for a gap in the sorted MST edge weights, and note there isn't one". 1 for a vague answer
about the clusters overlapping — the question asked what you would look at, given only the weights.*

---

## Checkoff Checklist

1. MST total is **485.061** and edges number **79,800**. **Check first.**
2. Kruskal and dense-Prim agree exactly.
3. C1's bottleneck is verified by the sorted-edge method, not just read off the MST.
4. C3(a) cites the **gap**, not the equal cluster sizes.
5. D2 names chaining and links it back to why Part C worked.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 10 |
| B | 8 |
| C | 14 |
| D | 8 |
| **Total** | **40** |

Labs are pass/fail for progression: **10 of the 12 required labs (0–11).** A student completing A–C passes.

---

## Note for the Week 7 Lecture

This is the last graph lab; Week 7 changes subject to dynamic programming. Two things are worth
carrying over explicitly in Monday's lecture:

**The MST answered a question it was not designed for.** Nobody built minimum spanning trees to do
clustering, and the clustering is three lines on top of a tree you already had. Week 7's DP tables have
the same character — the table you fill to get one answer usually contains several others, and asking
what else is in it is a productive habit.

**Part D is the fourth "correct under an assumption" case this term** — after heap sort's cost model,
Dijkstra's non-negativity, and A\*'s admissibility. Single-linkage is optimal for a stated objective and
useless when the data does not have separated clusters. **Week 9's greedy algorithms are the same
story with the assumption made explicit in a proof**, which is where the term has been heading since
Week 2.

---

*CS 102 · Week 6 · Lab 6 Solutions · © CSE Department*
