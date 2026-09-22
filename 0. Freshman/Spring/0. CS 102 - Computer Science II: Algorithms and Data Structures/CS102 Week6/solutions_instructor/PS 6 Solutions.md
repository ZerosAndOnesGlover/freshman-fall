# CS 102 · Problem Set 6 — Solutions
## Minimum Spanning Trees and Union-Find

**INSTRUCTOR / TA COPY — not for distribution**

Every number was produced by running code. **Deterministic** figures should match a correct
submission; **machine-dependent** ones will not.

---

> **Revised 2026-09-22.** Removed: Part D (timing Kruskal and Prim — Lab 6 Part B does it) and E3
> (MST clustering — Lab 6 Part C does it). E1 now names its reference (threshold + BFS) instead of an
> untaught "modified Dijkstra". Old Part E is Part D; items re-weighted to keep 100 points.

## Part A — The Two Properties (22)

### A1 (6)

Brute force over $\binom{|E|}{V-1}$ subsets, keeping those that are spanning trees. Fine to $V \le 7$.

*The error to look for: testing "is a tree" by counting edges only. A subset of $V-1$ edges can
contain a cycle and leave the graph disconnected. Require an acyclicity check (union-find is easiest).*

### A2 (8) — deterministic: 0 violations

Reference: **3,191 (graph, cut) pairs** across 200 random graphs, every non-trivial cut checked
against every MST found by enumeration. **0 violations.**

**The construction.** The cleanest example is the triangle with all three weights equal to 1:

```
0-1 (1),  1-2 (1),  0-2 (1)
```

There are **3** MSTs, each of weight 2, and each edge appears in exactly **2 of the 3**. Take the cut
$S = \{0\}$: both crossing edges $(0,1)$ and $(0,2)$ are minimum. $(0,1)$ is in some MST but not in
the one consisting of $\{(1,2), (0,2)\}$.

*4 for the verification with counts, 3 for a correct construction showing **both** trees. Accept any
graph with a tie among minimum crossing edges. A student who claims no such graph exists has
misread "some" as "every" — which is the misconception the question exists to catch.*

### A3 (8) — deterministic: 0 violations

Reference: **758 (cycle, strictly-heaviest-edge) cases** across 150 random graphs. **0 violations.**

**Why "strictly" is needed.** The triangle $0{-}1\ (1)$, $1{-}2\ (2)$, $0{-}2\ (2)$: the cycle's
heaviest weight is 2 and it is **tied**. There are two MSTs — $\{(0,1),(1,2)\}$ and
$\{(0,1),(0,2)\}$ — and each contains one of the tied heaviest edges.

So without "strictly" the property is false.

---

## Part B — Prim and Kruskal (22)

### B1 (6), B2 (6), B3 (5) — deterministic: 0 mismatches

Reference: all three algorithms against brute force on **295 graphs** with $V \le 7$ — **0
mismatches** — and against each other on **500 graphs** with $V \le 40$ — **0 mismatches**.

*Mark against the total weight, not the edge set. With tied weights different algorithms legitimately
return different MSTs, and a student comparing edge sets will report spurious failures. If a submission
reports mismatches, check what they compared before assuming a bug.*

### B4 (5) — the assessed question

The difference is the **priority pushed**:

```python
# Dijkstra: distance from the SOURCE
if d + w < dist[v]: heapq.heappush(pq, (dist[v], v))

# Prim:     weight of THIS EDGE
heapq.heappush(pq, (ww, v, u))
```

Expected explanation: Dijkstra accumulates — the key is the whole path cost from $s$ — so it grows a
tree of shortest *routes*. Prim does not accumulate; the key is only the cost of attaching this vertex
to the tree, so it grows the *cheapest connection*. The problems differ in exactly that: shortest paths
care how far you have come, an MST does not.

*Full marks need both the identified line and the accumulate/don't-accumulate contrast. "One uses
distances and one uses weights" is 2 of 4.*

---

## Part C — Union-Find (30)

### C1 (9), C2 (7) — deterministic

| $n$ | neither | rank | compression | both |
| --- | --- | --- | --- | --- |
| 1,000 | 81,403 | 3,479 | 4,240 | 2,450 |
| 5,000 | 1,978,844 | 18,040 | 22,987 | 12,243 |
| 20,000 | 30,823,531 | 72,486 | 99,855 | 49,232 |
| 100,000 | 779,553,223 | 379,496 | 542,521 | 246,855 |

Expected: the naive column grows **quadratically** — 100× the input gives roughly $10^4$× the work
(81,403 → 779,553,223 is 9,576× for a 100× size increase). Speedup of *both* over *neither* at
$n = 10^5$: **3,158×**.

*Exact counts depend on the RNG stream. Mark the **ratios and growth rates**, not the digits. Any
submission whose naive column is not roughly quadratic has an accidental optimisation — usually a
`find` that assigns `p[x] = root` somewhere.*

### C3 (8) — deterministic and exact

| $n$ | naive | both |
| --- | --- | --- |
| 1,000 | 499,500 | 999 |
| 5,000 | 12,497,500 | 4,999 |
| 20,000 | 199,990,000 | 19,999 |

**Closed forms**: naive is $\binom{n}{2} = n(n-1)/2$ — the sum of path lengths $0 + 1 + \dots + (n-1)$
in a chain. Optimised is exactly $n - 1$: the first `find` walks the chain and flattens it, so every
later `find` costs one step.

*These are exact and a correct submission matches them precisely. 3 for the measurements, 3 for both
closed forms with justification. A student who reports the naive column but not the formula has done
the easy half.*

### C4 (6)

| $n$ | steps/op | $\log_2 n$ |
| --- | --- | --- |
| $10^3$ | 1.225 | 10.0 |
| $10^4$ | 1.222 | 13.3 |
| $10^5$ | 1.234 | 16.6 |
| $10^6$ | 1.235 | 19.9 |

Expected answer on $\alpha$: **it is not a constant.** It grows without bound, just extraordinarily
slowly — $\alpha(n) \le 4$ for every $n$ up to $A_4(1) = 2^{2^{2^{16}}} - 3$, which exceeds the number
of atoms in the observable universe, so it is a constant for every input that can exist. And the bound
$O(m\,\alpha(n))$ is **tight**, not merely the best known.

*2 for the table, 2 for a precise answer. "Yes, it's basically constant" scores 1; "no, it grows"
without the practical qualification scores 1. Both halves are needed.*

---

## Part D — Applications (26)

### D1 (9) — deterministic: 0 mismatches

Reference: **15,988 (source, target) pairs** across 300 random graphs. **0 mismatches.**

The handout's reference is the threshold test: sort the distinct weights, and for each pair take the
smallest $w$ at which a BFS over edges of weight $\le w$ connects $u$ and $v$. It computes the same
value as Dijkstra with `max(d[u], w)` in place of `d[u] + w` (which the original key used). Both are
exact, so any mismatch is the student's MST path code.

### D2 (8)

Smallest example: the triangle $0{-}1\ (2)$, $1{-}2\ (2)$, $0{-}2\ (3)$.

- Shortest $0 \to 2$: the direct edge, **3**.
- MST: $\{(0,1), (1,2)\}$, total 4; the MST path $0 \to 1 \to 2$ costs **4**.

Expected cycle-property explanation: $(0,2)$ with weight 3 is the **strictly heaviest** edge on the
triangle, so it is in no MST — even though it is the shortest route between its endpoints. **The MST
is forced to exclude exactly the edge that a shortest-path tree would want.**

*3 for the example, 2 for the cycle-property argument. Any triangle $a, a, b$ with $a < b < 2a$ works.*

### D3 (9) — deterministic: 0 mismatches

Reference: adding 100 to every edge left the MST edge set unchanged in **300 of 300** graphs.

Expected explanation: **every spanning tree has exactly $V-1$ edges**, so adding $c$ to every weight
adds exactly $(V-1)c$ to every spanning tree's total and cannot reorder them. Paths do **not** have a
fixed length, so a shift favours paths with fewer edges and can change which path is shortest.

*2 for the verification, 2 for the counting argument. The phrase "every spanning tree has $V-1$ edges"
is the whole answer and must appear.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 22 |
| B | 22 |
| C | 30 |
| D | 26 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. Mark B3 against total weights, not edge sets.** With tied weights the algorithms legitimately
disagree on *which* MST they return. Expect several students to report false mismatches; this is a
teaching moment about A2 rather than a deduction.

**2. The timing comparison has moved to Lab 6 Part B**, where it is the fifth appearance of the same
idea — a complexity comparison that does not predict the measurement. The previous four were `SortedList` (Week 2), heap sort and `heapq.merge` (Week 3), and
BFS locality (Week 4). By now a student should be reaching for "operation count versus operation cost"
without prompting. If the cohort still is not, it is worth ten minutes rather than another deduction,
because **Week 7 has no such moment** and the habit will go unrehearsed for a fortnight.

**3. C3's closed forms are exact**, which makes this an unusually clean question to mark. A student
whose numbers do not match $n(n-1)/2$ and $n-1$ exactly has a bug, and it is worth finding for them —
it is almost always a `find` that partially compresses.

**4. Carried forward.** PS 5's Part C asked students to break their own Dijkstra. **A2 and A3 here are
the same skill applied to a theorem**: take a correct statement, find where its qualifiers ("some",
"strictly") are load-bearing, and construct the graph that shows it. Students who did well on PS 5 C
should do well here; if a student did badly on both, the issue is not graphs.

**5. Forward.** The exchange argument in Theorem 21.1 is the template for **Week 9**'s greedy
correctness proofs — flag this explicitly in feedback. **Week 12** uses the MST for a
2-approximation to TSP.

---

*CS 102 · Week 6 · PS 6 Solutions · © CSE Department*
