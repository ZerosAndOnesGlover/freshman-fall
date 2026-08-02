# CS 102 · Lab 4 — Solutions and Checkoff Notes
## BFS and DFS on a Social Network

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Run the reference generator on the lab machines first.** The whole lab depends on students
reproducing one specific graph, and if their generator differs by so much as the order they append
neighbours, every number after Part A disagrees and they will spend the session debugging arithmetic
instead of thinking.

**Put the A2 reference table on the board at the start.** Tell them to check against it before moving
to Part B. This is the single highest-value intervention in this lab.

Timing on the reference machine: graph construction is instant, B3's 5,000 BFS runs take about
**8 seconds**, and everything else is sub-second. **There is no slow part** — this lab is short on
compute and long on interpretation, which is the opposite of Lab 3. Budget the time accordingly and
expect Part C to absorb it.

---

## Part A — Build the Network (8)

### A1 (5)

The specification is precise about the sampling: choose from a list in which each vertex appears once
per incident edge. The two errors that change the graph:

- **Sampling with replacement into `chosen`** without the `while len(chosen) < m` loop, giving a new
  vertex fewer than $m$ distinct neighbours.
- **Forgetting to append the new vertex $m$ times** to `rep`, which stops new vertices from ever being
  chosen and collapses the degree distribution.

Either produces a plausible-looking graph with the wrong numbers. **Diagnose from $E$**: it must be
exactly 14,994.

### A2 (3) — deterministic

| quantity | value |
| --- | --- |
| $V$ | 5,000 |
| $E$ | **14,994** |
| mean degree | 6.00 |
| components | 1 |
| max degree | 192 |
| min degree | 3 |
| median degree | 4 |
| ten largest | 192, 164, 142, 128, 118, 117, 114, 110, 109, 104 |
| degree-3 vertices | 2,024 |

$E = 3 + 3 \times 4997 = 14{,}994$: three edges among the initial triangle, then $m = 3$ per added
vertex. A student whose $E$ is 14,997 or 15,000 has an off-by-one in the seeding; it is worth
diagnosing rather than waving through, because it shifts everything downstream.

**Connectivity is not an accident** — every new vertex attaches to existing ones, so the graph is
connected by construction. Ask a student who reports more than one component to explain how that could
happen; they will find their bug.

---

## Part B — Degrees of Separation (12)

### B1 (4) — deterministic

| level | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| vertices | 1 | 142 | 1,543 | 3,001 | 313 |

Eccentricity **4**, mean distance from vertex 0 **2.697**.

### B2 (4)

Expected: the levels grow because each frontier vertex has several unvisited neighbours, so the
frontier multiplies — and it multiplies *fast* here because preferential attachment means the early
frontier contains hubs.

They collapse because the graph is finite: levels 0–3 account for $1+142+1543+3001 = 4{,}687$ of the
5,000 vertices, so level 4 can only contain the 313 that remain. **The peak is where "most neighbours are new" stops being
true.**

*Full marks need both halves. The collapse is the half students omit — many write only the branching
argument, which alone would predict unbounded growth. 2 of 4 for one half.*

### B3 (4) — deterministic

| quantity | value |
| --- | --- |
| **diameter** | **7** |
| radius | 4 |
| mean distance, all ordered pairs | 4.0511 |
| eccentricities | 4: 10 · 5: 1,671 · 6: 3,291 · **7: 28** |

---

## Part C — The Double-Sweep Heuristic (10)

### C1 (3) — deterministic

From vertex 0: $a = 757$ (eccentricity 6), $b = 2385$, estimate **6**.

### C2 (3)

**They do not agree.** The heuristic reports 6; the true diameter is 7.

*Some students will report agreement. That means they started the sweep somewhere other than vertex 0,
which the handout specified — the heuristic does sometimes succeed from other starts. Accept a correct
disagreement from a different start; do not accept a reported agreement without checking which start
they used.*

### C3 (4) — the assessed question

Three things wanted:

1. **28 of 5,000 vertices** (0.56%) have eccentricity 7.
2. The double sweep examines the eccentricity of exactly **two** vertices, neither chosen to be
   extremal in the right way, so it is unlikely to land on one of the 28. Vertex 0 is a founding hub
   with eccentricity 4 — one of the **10 most central vertices in the graph** — which makes it about
   the worst possible starting point.
3. **It is a lower bound, always.** $\mathrm{dist}(a,b)$ is the distance between two actual vertices,
   and the diameter is the maximum over all pairs, so the estimate can never exceed it. It can — and
   here does — fall short.

*The bound direction is the mark that separates answers. A student who says "it's approximate" or
"usually close" has not answered; the question asked upper, lower, or neither, and demanded
justification. 2 of 4 for the statistics without the bound; 0 of 4 for guessing the direction with no
argument, even if the guess is right.*

> **Worth saying aloud at checkoff:** the double sweep is a genuinely good heuristic and is exact on
> trees. Students should not leave thinking it is bad — they should leave able to say *which way* it
> is wrong, which is what makes it usable.

---

## Part D — BFS Against DFS (10)

### D1 (4) — deterministic

| quantity | value |
| --- | --- |
| BFS eccentricity from vertex 0 | 4 |
| **iterative DFS tree depth from vertex 0** | **3,226** |
| ratio | 806× |

The DFS depth is deterministic given the generator and the adjacency order. A student whose value
differs but whose A2 numbers match has a different push order in their stack — accept anything in the
low thousands, but have them explain the source of the difference.

### D2 (3)

Expected: DFS commits to one neighbour and follows it as far as it can, so its tree is a long snake
through a graph in which everything is within 4 steps of the source. **BFS's tree is a shortest-path
tree** — every root-to-node path in it is a shortest path. **DFS's tree is not optimal in any sense**;
it records the order the search happened to take. Its usefulness is structural, not metric.

### D3 (3)

Recursive DFS on the network raises **`RecursionError`**.

The expected answer to the "why" question: **the recursion depth is bounded by the length of the DFS
tree path, not by the graph's diameter.** The diameter says every vertex is within 7 steps *by the
shortest route*; DFS does not take shortest routes, and its path here is 3,226 long. A small-diameter
graph can still contain very long simple paths — the DFS here walks one of 3,226 vertices, about 65%
of the graph, in a network where no two vertices are more than 7 apart.

*This is the graded idea of Part D. A student who says "because the graph is big" has missed it — a
graph can be big and shallow. The distinction is diameter versus longest simple path. 1 of 3 for a
vague answer, 3 for one that names the right quantity.*

---

## Checkoff Checklist

1. $E = 14{,}994$ and components $= 1$. **Check this first; nothing downstream is meaningful without
   it.**
2. B1 level sizes match 1, 142, 1543, 3001, 313.
3. B3 diameter is 7, not 6. (A student reporting 6 has probably used their C1 code for B3.)
4. C3 names the bound direction *and* justifies it.
5. D3 distinguishes diameter from longest simple path.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 8 |
| B | 12 |
| C | 10 |
| D | 10 |
| **Total** | **40** |

Labs are pass/fail for progression: **10 of 13 required.** A student who completes A, B and D and
answers C3 poorly still passes.

---

## Note for the Week 5 Lecture

Part C3 is a rehearsal for the whole of the back half of this course. **Knowing the direction of your
error is what makes an inexact method usable**, and that idea carries:

- **Week 9**, greedy algorithms: an exchange argument proves a greedy choice is *no worse*, which is a
  bound in a direction.
- **Week 12**, approximation: a 2-approximation for TSP is only useful because the 2 is an upper
  bound.

If Part C3 went badly across the cohort, spend five minutes on it before starting Dijkstra — the
correctness argument for Dijkstra is also a statement about a quantity that can only move one way, and
students who did not see it here will not see it there either.

---

*CS 102 · Week 4 · Lab 4 Solutions · © CSE Department*
