# CS 102 · Problem Set 4 — Solutions
## Graph Representations and Traversal

**INSTRUCTOR / TA COPY — not for distribution**

Every number here was produced by running code. **Deterministic** figures should match a correct
submission exactly; **machine-dependent** ones will not.

---

> **Revised 2026-09-22.** Removed: A2–A3 (memory measurement, already in Lecture 13 §4), B3 (it
> needed Floyd–Warshall, a Week 8 topic), D1–D2 (edge-classification counts, already in Lecture 15
> §4) and Part E (timing, already in Lecture 13 §7). Remaining items were renumbered and re-weighted
> to keep 100 points; scale any in-item breakdown that still quotes the old points.

## Part A — Representations (10)

### A1 (10)

Both classes must pass the same suite. 3 for `AdjList`, 3 for `AdjMatrix`.

**The error to look for** is an `AdjList.has_edge` that is $O(1)$ because the student silently used a
`set`. That is a legitimate design, but it changes the answer to A3 and makes Part D4(b) trivially
true. If they did it, accept it and require them to say so — and check that D4 is answered against the
`list` version.

## Part B — BFS (26)

### B1 (8), B2 (6)

Standard. B2's expected sentence: `parent` is $V$ integers and encodes **all** $V$ shortest paths;
storing the paths themselves is $\Theta(V^2)$ in the worst case (a path graph).

**Look for** `dist[v] == -1` used as the discovery test versus a separate `seen` array. Both are fine;
using `parent[v] is None` is **not**, because `parent[s]` is legitimately `None`.

### B3 (6)

Expected argument: the outer loop starts BFS only from **undiscovered** vertices, and each vertex is
discovered exactly once across the entire run. So each vertex is enqueued once in total and each
adjacency list is scanned once in total, giving $\Theta(V+E)$ over all invocations combined — not per
invocation.

*The word doing the work is "total". A student who says "each BFS is $\Theta(V+E)$ and there are at
most $V$ of them, so $\Theta(V(V+E))$, but really it's less" has not made the argument — 2 of 4.*

### B4 (6) — deterministic

Cycles of length 3, 5, 7 are **not** bipartite; 4, 6, 8 **are**.

Expected theorem: **a graph is bipartite iff it contains no odd cycle.**

*(Reference: verified against exhaustive $2^n$ brute force on 300 random graphs of up to 12 vertices —
0 mismatches.)*

---

## Part C — DFS and Timestamps (34)

### C1 (8)

A recursive DFS on a path of 5,000 fails with **`RecursionError`** (default limit 1,000).

Expected explanation of why raising the limit is unsatisfactory: the frames are real C-stack frames.
`sys.setrecursionlimit` raises only Python's *counter*, not the operating system's stack allocation,
so a large enough graph produces a **segmentation fault** instead of a catchable exception. Trading a
clean error for a crash is not a fix.

*3 for the iterative version, 2 for the explanation. Accept "you'd need to raise the thread stack size
too" as a full answer — it is correct and more sophisticated.*

### C2 (8) — deterministic: 0 failures

Reference: 300 random digraphs. All $2V$ timestamps were a permutation of $1 \dots 2V$ and
$d[u] < f[u]$ everywhere. **0 failures.**

*5 for correct timestamps including the outer forest loop, 2 for the verification. **The most common
error is omitting the outer loop**, which silently produces correct output on connected graphs and
zeros elsewhere — check their test includes a disconnected graph.*

### C3 (10)

**(a) (3)** For any $u, v$ exactly one of: the intervals are disjoint (neither is a descendant of the
other); $[d(v),f(v)] \subset [d(u),f(u)]$ ($v$ is a descendant of $u$); or the reverse. **Partial
overlap is impossible.**

**(b) (3)** Reference: **21,814 ordered pairs** across 200 random digraphs. Exactly one case held for
every pair, and containment matched the independently computed descendant relation in every case.
**0 failures.**

*The independent computation must walk the `parent` array. A student who defines "descendant" using
$d$ and $f$ and then verifies it against $d$ and $f$ has proved nothing — this is the trap in (b) and
it is worth checking carefully. Award 0 of 3 for a circular verification, regardless of the reported
count.*

**(c) (2)**

```python
def is_descendant(v, u):
    return d[u] < d[v] and f[v] < f[u]
```

Useful because ancestry — normally a tree walk — becomes two integer comparisons after $\Theta(V+E)$
preprocessing.

### C4 (8) — deterministic

Reference over 300 random digraphs: tree 2,279, back 1,516, forward 749, cross 1,541 — all four occur.

Cycle theorem: compared against an independently written three-colour detector on **1,000 random
digraphs — 0 mismatches**, of which 185 were cyclic in the smaller sample.

*3 for correct classification, 3 for the verification. The classification error to look for is testing
`d[u] < d[v]` to separate forward from cross **before** checking the colour — the colour test must
come first.*

---

## Part D — Undirected Cycle Detection (30)

### D1 (10)

Smallest tree on which the parent-free version reports a cycle: **two vertices, one edge.** DFS goes
$0 \to 1$, then from 1 examines 0, finds it seen, and reports a cycle. (A 3-vertex path also works;
accept either, but 2 vertices is the true minimum.)

### D2 (20) — the assessed question

**(a) (3)** **The claim is false.** Exhaustive search over every multigraph on $V \le 4$ with up to 3
edges — self-loops and parallel edges included — against a union-find ground truth gives **0
disagreements**.

The reason: if $u$ and $p$ are joined by two edges, `g[p]` contains `u` **twice**. DFS descends
through the first copy; on returning it examines the second, finds $u$ seen and $u \ne$ *its own*
parent, and reports the cycle correctly. Self-loops are caught the same way.

**(b) (3)** Building adjacency from `set` instead of `list` gives **56 disagreements** in the same
search. Smallest failing case: $V = 2$ with edges $\{(0,1), (0,1)\}$ — a genuine 2-cycle that
deduplication erases.

**The fault is in the data structure, not the algorithm.** The `set` cannot represent a multigraph, so
the traversal is correct about a graph that is not the one supplied.

*3 + 3, and both halves require the student's own exhaustive search with a reported count. A student
who argues the point correctly but reports no numbers scores 4 of 6 — the question said "test this
claim". A student who reports the claim is **true** has almost certainly built adjacency from sets;
send them back to (b) before marking.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 10 |
| B | 26 |
| C | 34 |
| D | 30 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. C3(b)'s circular-verification trap is the one to watch.** It is easy to "verify" the parenthesis
theorem using the same two arrays that define the thing being verified. The independent computation
must walk `parent`. Expect a meaningful fraction of the cohort to get this wrong while reporting a
confident zero, and check the code rather than the number.

**2. D2 will produce confident wrong answers from good students**, because the false claim is
well-attested online. That is the point of the question. Where a student has clearly *searched* and
reported what they found, give full credit even if their explanation of the mechanism is shaky.

**3. MIDTERM 1 is Monday 1 March 2027 (Week 6)**, three days after this set is due. Everything on the
set is examinable, so marked scripts should go back before the paper if at all possible.

**4. Carried forward.** Week 3's Lab 3 D1 asked students to distinguish a constant factor from a
trend. Lecture 13 §7 makes the same point for BFS, and Quiz 5 Q6 asks it; students who missed it in
Lab 3 should be pointed at their own Lab 3 answer.

**5. Forward.** C4's back-edge machinery becomes topological sort and strongly connected components in
**Week 5**. B4's bipartiteness returns in **Week 12** as 2-colouring, the one graph-colouring problem
that is *not* NP-complete — worth mentioning to strong students now.

---

*CS 102 · Week 4 · PS 4 Solutions · © CSE Department*
