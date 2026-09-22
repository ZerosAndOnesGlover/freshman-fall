# CS 102 · Problem Set 5 — Solutions
## Shortest Paths

**INSTRUCTOR / TA COPY — not for distribution**

Every number was produced by running code. **Deterministic** figures should match; **machine-dependent**
ones will not.

---

> **Revised 2026-09-22.** Removed: B4 and B5 (heap counts and the early exit — Lab 5 Part B does the
> early exit), C3 (a random-graph failure rate), and D4 (timing). C4 is now C3 and D5 is now D4;
> items were re-weighted to keep 100 points.

## Part A — DAGs (20)

### A1 (5), A2 (5)

Reference: 500 random DAGs, both algorithms, every edge respects the order. **0 failures.**

Expected answer to "do they produce the same order?": **usually not, and they need not.** A DAG
generally has many valid topological orders; both algorithms produce one. Marking against a specific
order is wrong — mark against the *property*.

*The error to look for in `topo_dfs` is appending on **discovery** rather than on **finish**. That
produces a preorder, which is not a topological order, and it works on paths and fails on branches.
If their A2 check passes with this bug, their verification is not checking every edge.*

### A3 (5) — deterministic: 0 mismatches

Reference: 500 random DAGs, **351 containing negative edges**, from every source — **3,607
(graph, source) pairs** — against Bellman–Ford. **0 mismatches.**

*The 351 is incidental (it depends on the RNG stream); the **0** is the result. Do not mark against
the 351.*

### A4 (5)

**(a) (3)** A DAG has no cycles, therefore no negative cycles, therefore shortest paths are always
well defined. And the topological order — not a distance-based greedy order — is what guarantees
every predecessor is final before a vertex is processed, so the argument never needs weights to be
non-negative.

*Full marks require both halves: "no negative cycles" **and** "the ordering does not come from the
weights". A student giving only the first has 2 of 3.*

**(b) (3)** Negation verified against a direct longest-path computation on 300 DAGs — **0
mismatches.**

Why it fails in general: negating turns positive cycles into negative ones, so the shortest-path
problem becomes ill-posed. And the underlying fact is that **longest simple path on a general graph is
NP-complete** (Week 12). Accept "NP-hard".

---

## Part B — Dijkstra (22)

### B1 (8), B2 (6)

Standard. B2's check is that the sum of edge weights along the recovered path equals `dist[t]`.

### B3 (8) — deterministic: 0 mismatches

Reference: **4,071 (graph, source) pairs** on random non-negative graphs, against Bellman–Ford.
**0 mismatches.**

## Part C — When Dijkstra Is Wrong (20)

**This is the part to read carefully when marking.**

### C1 (6) — deterministic

The textbook counterexample: $0\to1\ (-1)$, $0\to2\ (-2)$, $1\to2\ (-2)$. True distances
$[0, -1, -3]$.

- Textbook Dijkstra (no relaxation into a finalised vertex): $[0, -1, -2]$ — **wrong**.
- The lazy-deletion implementation of Lecture 17 §1: **correct**.

Expect most submissions to report "my implementation gets it right", which is the intended outcome.

### C2 (10) — deterministic

Expected explanation: the lazy version has **no `and not done[v]` guard** on the relaxation. It
relabels `dist[v]` even after $v$ has been finalised; it only refuses to **re-expand** $v$. So a late
correction still reaches the answer array, and is only lost if something downstream already consumed
the old value.

A graph that does break it:

```
0 -> 1  (1)      0 -> 2  (2)      2 -> 1  (-2)      1 -> 3  (1)
```

| | dist |
| --- | --- |
| lazy Dijkstra | `[0, 0, 2, 2]` |
| textbook Dijkstra | `[0, 1, 2, 2]` |
| **correct** | `[0, 0, 2, 1]` |

Smallest failing $V$, by exhaustive search over weights in $\{-2,-1,1,2\}$:

| implementation | smallest $V$ |
| --- | --- |
| textbook | **3** |
| lazy | **4** |

*4 for a genuine failing graph with all three answers; 2 for the exhaustive minimum. A student who
reports $V = 3$ for the lazy version has tested the textbook version — check which code they ran.*

### C3 (4)

The step is $\delta(s,y) \le \delta(s,u)$, where $y$ lies on a shortest path to $u$ — i.e. **a prefix
of a shortest path is no longer than the whole path**. With a negative edge later on the path, the
remainder can have negative length and the prefix can be *longer* than the whole, so $y$ need not be
popped before $u$.

*Award 0 for "because Dijkstra is greedy" or "because it finalises vertices" — the question asks for
the step in the proof.*

---

## Part D — Bellman–Ford (26)

### D1 (8), D4 (6) — deterministic

Detection verified against brute-force cycle enumeration on **600 digraphs (152 with a reachable
negative cycle) — 0 mismatches**.

For D5, the extraction that works:

```python
x = None
for i in range(V):                    # V rounds, NOT V-1
    x = None
    for u, v, w in edges:
        if d[u] != INF and d[u] + w < d[v]:
            d[v] = d[u] + w; par[v] = u; x = v      # relax AND remember
    if x is None: break
if x is None: return d, None
for _ in range(V): x = par[x]         # now guaranteed on the cycle
cyc = [x]; y = par[x]
while y != x: cyc.append(y); y = par[y]
```

**The common bug**: detecting the improving edge in a separate final pass *without performing the
relaxation*, then walking `par` from that vertex. If that vertex had `d = INF`, its parent is `None`
and the walk raises `TypeError`. The fix is to relax during the detecting round so the parent exists.

Reference: **1,114 cycles extracted from 3,000 random graphs; all simple, all negative; 0 invalid.**

*3 for extraction that is verified simple and negative. A student whose code crashes on some inputs
has met the bug above — give 1 and point them at it.*

### D2 (6) — deterministic

| $V$ | rounds | $V-1$ | $\log_2 V$ |
| --- | --- | --- | --- |
| 1,000 | 11 | 999 | 10.0 |
| 5,000 | 12 | 4,999 | 12.3 |
| 20,000 | 14 | 19,999 | 14.3 |

Expected: the rounds count measures the **maximum number of edges on any shortest path** — the graph's
hop-diameter — which on a random graph is $\Theta(\log V)$, not $\Theta(V)$.

*Full marks require naming the hop-diameter (or "most edges on a shortest path"). "It converges early"
is 2 of 5.*

### D3 (6) — deterministic

Path graph $0\to1\to\dots\to(V-1)$, edges presented in **reverse** order:

| $V$ | 5 | 10 | 20 | 50 |
| --- | --- | --- | --- | --- |
| rounds | 4 | 9 | 19 | **49** |

Same graph, edges in forward order: **2 rounds** at every $V$ (the second detects that nothing
changed).

Expected statement: **$O(VE)$ is a worst case over edge orderings**, not a property of the graph.

*This is the graded idea of Part D. A student who constructs a tight example but says the bound is
"about the graph" scores 3 of 5.*

## Part E — Choosing (12)

2 each. Complexity must be stated.

| | expected answer |
| --- | --- |
| **E1** | **BFS.** All weights equal, so no priority queue is justified. $\Theta(V+E)$. Bidirectional BFS is a strong bonus answer at this scale. |
| **E2** | **Dijkstra with a binary heap**, or **A\*** for point-to-point. Weights non-negative, graph sparse. $O((V+E)\log V)$. |
| **E3** | **DAG longest path** by topological order — the *critical path*. $\Theta(V+E)$. **Not Dijkstra**: this is a maximisation on a DAG. |
| **E4** | **Bellman–Ford** on edge weights $-\log(\text{rate})$, looking for a **negative cycle**. $O(VE)$ with $V=200$, trivial. Accept Floyd–Warshall. |
| **E5** | **Dijkstra with an array**, not a heap: $E \approx V^2$, so $\Theta(V^2)$ beats $O(V^2\log V)$. |
| **E6** | **Bellman–Ford.** Negative edges, no negative cycles guaranteed. $O(VE)$ — note $E$ is small for a tile map, so this is fine. |

*E3 and E5 are the discriminating ones.* E3 catches students who reach for Dijkstra reflexively; E5
catches students who believe a heap is always an improvement. Deduct fully on E5 for "Dijkstra with a
heap" with no discussion of density.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 20 |
| B | 22 |
| C | 20 |
| D | 26 |
| E | 12 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. Part C is the intellectual centre of this set** and will be the worst-answered. The sequence —
"you are told it fails", "the standard counterexample does not fail", "you must construct one" — is designed so that the only reliable route to the truth is the
correctness proof. Where a student got there, say so in the feedback; it is the skill the course is
for.

**2. Expect the D4 `TypeError`.** It is a genuine trap and I hit it myself writing these solutions.
Do not treat it as carelessness — it is caused by following the textbook's *detection* code and then
extending it to extraction, which is a reasonable thing to do and does not work.

**3. MIDTERM 1 falls inside this set's window** (Monday 1 March, Weeks 0–4). Part A was flagged as
doable beforehand; nothing on the set is on the paper.

**4. Carried forward.** Lab 3 D1 and Quiz 5 Q6 asked students to reconcile a bound with a measurement
that seemed to contradict it. **D2 and D3 are the same question again** — a bound that overstates the
typical cost, and a bound that is about something other than what students assume. If a student has
missed it every time, that is worth a conversation rather than another deduction.

**5. Forward.** Dijkstra's greedy correctness argument is the template for **Week 6**'s cut property
and **Week 9**'s exchange arguments. Bellman–Ford's recurrence over edge counts is a dynamic program,
and **Week 7 opens by pointing back at it** — flag this to students who ask what DP is.

---

*CS 102 · Week 5 · PS 5 Solutions · © CSE Department*
