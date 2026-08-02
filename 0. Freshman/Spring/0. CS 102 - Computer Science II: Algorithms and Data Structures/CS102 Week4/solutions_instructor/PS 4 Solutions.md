# CS 102 · Problem Set 4 — Solutions
## Graph Representations and Traversal

**INSTRUCTOR / TA COPY — not for distribution**

Every number here was produced by running code. **Deterministic** figures should match a correct
submission exactly; **machine-dependent** ones will not.

---

## Part A — Representations (16)

### A1 (6)

Both classes must pass the same suite. 3 for `AdjList`, 3 for `AdjMatrix`.

**The error to look for** is an `AdjList.has_edge` that is $O(1)$ because the student silently used a
`set`. That is a legitimate design, but it changes the answer to A3 and makes Part D4(b) trivially
true. If they did it, accept it and require them to say so — and check that D4 is answered against the
`list` version.

### A2 (4) — deterministic

| $V$ | matrix | list | ratio |
| --- | --- | --- | --- |
| 100 | 86,576 B | 13,772 B | 6.3 |
| 500 | 2,032,272 B | 88,220 B | 23.0 |
| 1,000 | 8,064,912 B | 199,164 B | 40.5 |
| 2,000 | 32,128,240 B | 420,080 B | 76.5 |

Expected observation: **the ratio doubles when $V$ doubles.** The matrix is $\Theta(V^2)$ and the list
is $\Theta(V+E) = \Theta(V)$ here since $E = 2V$, so the ratio is $\Theta(V)$.

*Exact byte counts depend on the traversal used for `getsizeof`; accept anything within ~10% with the
right ratios. Mark the ratio column, not the bytes.*

### A3 (6) — deterministic

| $E$ | density | matrix | list |
| --- | --- | --- | --- |
| 400 | 0.005 | 1,305,712 B | 52,040 B |
| 2,000 | 0.025 | 1,305,712 B | 116,348 B |
| 10,000 | 0.125 | 1,305,712 B | 411,328 B |
| 40,000 | 0.501 | 1,305,712 B | 1,520,720 B |
| 79,800 | 1.000 | 1,305,712 B | 2,910,448 B |

**Crossover between density 0.125 and 0.501.** At the complete graph the list uses 2.2× the matrix.

Expected explanation: a Python `list` of small integers stores **8-byte pointers to `int` objects**,
not the integers themselves, plus per-list object overhead for each of the $V$ rows. So a list entry
costs far more than the one byte a matrix cell costs. The matrix is *also* a list of lists and pays
the same per-entry cost, but its entry count is fixed at $V^2$ regardless of $E$.

In C with a bit-packed matrix — one **bit** per pair — the matrix would use $V^2/8$ bytes and the
crossover would move **much earlier**, to roughly $E \approx V^2/128$ against an 8-byte-per-entry
list. At $V=400$ that is around $E \approx 1{,}250$, i.e. density ~1.5% rather than 50%.

*4 for the tables and a correctly located crossover; 2 for an explanation that mentions pointer
indirection. "Python is slow" scores 0 of those 2. Accept any sensible order-of-magnitude answer for
the C question — the direction is what matters.*

---

## Part B — BFS (24)

### B1 (6), B2 (4)

Standard. B2's expected sentence: `parent` is $V$ integers and encodes **all** $V$ shortest paths;
storing the paths themselves is $\Theta(V^2)$ in the worst case (a path graph).

**Look for** `dist[v] == -1` used as the discovery test versus a separate `seen` array. Both are fine;
using `parent[v] is None` is **not**, because `parent[s]` is legitimately `None`.

### B3 (6) — deterministic: 0 mismatches

Reference: 200 random graphs of up to 18 vertices, BFS from **every** source compared against
Floyd–Warshall on **every** pair. **0 mismatches.**

*3 for a correct independent reference, 3 for the comparison being over all sources and all pairs. A
student who checks only from vertex 0 has done a third of the work — cap at 4.*

### B4 (4)

Expected argument: the outer loop starts BFS only from **undiscovered** vertices, and each vertex is
discovered exactly once across the entire run. So each vertex is enqueued once in total and each
adjacency list is scanned once in total, giving $\Theta(V+E)$ over all invocations combined — not per
invocation.

*The word doing the work is "total". A student who says "each BFS is $\Theta(V+E)$ and there are at
most $V$ of them, so $\Theta(V(V+E))$, but really it's less" has not made the argument — 2 of 4.*

### B5 (4) — deterministic

Cycles of length 3, 5, 7 are **not** bipartite; 4, 6, 8 **are**.

Expected theorem: **a graph is bipartite iff it contains no odd cycle.**

*(Reference: verified against exhaustive $2^n$ brute force on 300 random graphs of up to 12 vertices —
0 mismatches.)*

---

## Part C — DFS and Timestamps (26)

### C1 (5)

A recursive DFS on a path of 5,000 fails with **`RecursionError`** (default limit 1,000).

Expected explanation of why raising the limit is unsatisfactory: the frames are real C-stack frames.
`sys.setrecursionlimit` raises only Python's *counter*, not the operating system's stack allocation,
so a large enough graph produces a **segmentation fault** instead of a catchable exception. Trading a
clean error for a crash is not a fix.

*3 for the iterative version, 2 for the explanation. Accept "you'd need to raise the thread stack size
too" as a full answer — it is correct and more sophisticated.*

### C2 (7) — deterministic: 0 failures

Reference: 300 random digraphs. All $2V$ timestamps were a permutation of $1 \dots 2V$ and
$d[u] < f[u]$ everywhere. **0 failures.**

*5 for correct timestamps including the outer forest loop, 2 for the verification. **The most common
error is omitting the outer loop**, which silently produces correct output on connected graphs and
zeros elsewhere — check their test includes a disconnected graph.*

### C3 (8)

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

### C4 (6) — deterministic

Reference over 300 random digraphs: tree 2,279, back 1,516, forward 749, cross 1,541 — all four occur.

Cycle theorem: compared against an independently written three-colour detector on **1,000 random
digraphs — 0 mismatches**, of which 185 were cyclic in the smaller sample.

*3 for correct classification, 3 for the verification. The classification error to look for is testing
`d[u] < d[v]` to separate forward from cross **before** checking the colour — the colour test must
come first.*

---

## Part D — Undirected Cycle Detection (18)

### D1 (4) — deterministic

Counting every edge from both endpoints, 300 random undirected graphs:

| tree | back | forward | cross |
| --- | --- | --- | --- |
| 2,547 | 1,487 + 2,547 | 1,487 | 0 |

Expected: **`forward` equals `back`-not-to-parent exactly**, because each is the *other end* of the
same physical edge. A back edge seen from the descendant is a forward edge seen from the ancestor.

### D2 (4) — deterministic

Classifying each physical edge on first encounter only:

| tree | back | forward | cross |
| --- | --- | --- | --- |
| 2,547 | 1,487 | **0** | **0** |

Theorem: **in an undirected graph every edge is a tree edge or a back edge.**

### D3 (4)

Smallest tree on which the parent-free version reports a cycle: **two vertices, one edge.** DFS goes
$0 \to 1$, then from 1 examines 0, finds it seen, and reports a cycle. (A 3-vertex path also works;
accept either, but 2 vertices is the true minimum.)

### D4 (6) — the assessed question

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

## Part E — Reading the Cost Model (16)

### E1 (6) — machine-dependent

| $V$ | $E$ | BFS | ns per $(V+E)$ |
| --- | --- | --- | --- |
| 10,000 | 30,000 | 3.2 ms | 80.6 |
| 50,000 | 149,996 | 46.8 ms | 234.2 |
| 200,000 | 600,000 | 258.2 ms | 322.8 |
| 1,000,000 | 2,999,996 | 1597.4 ms | 399.4 |

### E2 (4) — the assessed question

Expected: **the bound is not wrong.** $\Theta(V+E)$ counts *operations*, and the operation count is
exactly linear. What changes is the cost of one operation: a traversal of a random graph follows edges
to unpredictable memory addresses, so once the graph exceeds cache, most edge follows are cache
misses. The notation deliberately says nothing about memory hierarchy.

*A student who says "the bound is wrong" or "Python is slow" scores 0. A student who says "cache" with
no mechanism scores 2.*

### E3 (6) — machine-dependent, but the shape is not

| $V$ | grid: BFS | ns per $(V+E)$ |
| --- | --- | --- |
| 10,000 | 2.3 ms | 78.4 |
| 50,176 | 12.8 ms | 85.0 |
| 200,704 | 55.9 ms | 92.9 |
| 1,000,000 | 356.1 ms | 118.8 |

**The two columns start together (80.6 against 78.4) and diverge: random degrades 5.0×, grid 1.5×.**

Expected explanation: on a grid numbered $ik+j$, a vertex's neighbours are at $\pm 1$ and $\pm k$, so
they are near it in memory and mostly already in cache. This confirms E2's answer by controlling for
everything except graph structure.

Implication: **a graph-algorithm benchmark is close to meaningless without the graph family.** The same
implementation differs by 3.4× here on inputs of the same $V$ and $E$.

*4 for the table and the comparison, 2 for the implication about benchmarks.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 16 |
| B | 24 |
| C | 26 |
| D | 18 |
| E | 16 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. C3(b)'s circular-verification trap is the one to watch.** It is easy to "verify" the parenthesis
theorem using the same two arrays that define the thing being verified. The independent computation
must walk `parent`. Expect a meaningful fraction of the cohort to get this wrong while reporting a
confident zero, and check the code rather than the number.

**2. D4 will produce confident wrong answers from good students**, because the false claim is
well-attested online. That is the point of the question. Where a student has clearly *searched* and
reported what they found, give full credit even if their explanation of the mechanism is shaky.

**3. This problem set is due the same week as MIDTERM 1.** Parts A–C are the examinable material;
D and E are not. If time pressure shows in the submissions, it should show in D and E, and that is the
intended failure mode rather than a problem with the set.

**4. Carried forward.** Week 3's Lab 3 D1 asked students to distinguish a constant factor from a
trend. **E2 is the same question** in a new setting, and students who missed it there should be
pointed at their own Lab 3 answer. If the cohort misses it twice, raise it in the Week 5 lecture —
Dijkstra's running time has the same structure and it will cost them a third time.

**5. Forward.** C4's back-edge machinery becomes topological sort and strongly connected components in
**Week 5**. B5's bipartiteness returns in **Week 12** as 2-colouring, the one graph-colouring problem
that is *not* NP-complete — worth mentioning to strong students now.

---

*CS 102 · Week 4 · PS 4 Solutions · © CSE Department*
