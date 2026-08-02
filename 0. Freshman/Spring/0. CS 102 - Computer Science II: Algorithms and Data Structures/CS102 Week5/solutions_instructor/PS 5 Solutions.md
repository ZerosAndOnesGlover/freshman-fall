# CS 102 · Problem Set 5 — Solutions
## Shortest Paths

**INSTRUCTOR / TA COPY — not for distribution**

Every number was produced by running code. **Deterministic** figures should match; **machine-dependent**
ones will not.

---

## Part A — DAGs (22)

### A1 (5), A2 (5)

Reference: 500 random DAGs, both algorithms, every edge respects the order. **0 failures.**

Expected answer to "do they produce the same order?": **usually not, and they need not.** A DAG
generally has many valid topological orders; both algorithms produce one. Marking against a specific
order is wrong — mark against the *property*.

*The error to look for in `topo_dfs` is appending on **discovery** rather than on **finish**. That
produces a preorder, which is not a topological order, and it works on paths and fails on branches.
If their A2 check passes with this bug, their verification is not checking every edge.*

### A3 (6) — deterministic: 0 mismatches

Reference: 500 random DAGs, **351 containing negative edges**, from every source — **3,607
(graph, source) pairs** — against Bellman–Ford. **0 mismatches.**

*The 351 is incidental (it depends on the RNG stream); the **0** is the result. Do not mark against
the 351.*

### A4 (6)

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

## Part B — Dijkstra (24)

### B1 (6), B2 (4)

Standard. B2's check is that the sum of edge weights along the recovered path equals `dist[t]`.

### B3 (6) — deterministic: 0 mismatches

Reference: **4,071 (graph, source) pairs** on random non-negative graphs, against Bellman–Ford.
**0 mismatches.**

### B4 (4)

Expected: pops can exceed $V$ because lazy deletion pushes a **duplicate entry** on every successful
relaxation rather than doing a `decrease_key`; the stale copies are popped and skipped. Pushes are at
most $E + 1$ — one per successful relaxation plus the source — so the heap is $O(E)$.

*A student who says pops are bounded by $V$ has not instrumented anything; their numbers will show
otherwise.*

### B5 (4)

Expected justification: **when $t$ is popped it is finalised**, and by the correctness theorem its
distance is already the true shortest distance. Nothing later can improve it, so the remaining work is
wasted.

On the Lab 5 road network the early exit is a large saving; on random graphs it is smaller, because a
random graph has no geometry and the frontier reaches everything at once.

---

## Part C — When Dijkstra Is Wrong (18)

**This is the part to read carefully when marking.**

### C1 (5) — deterministic

The textbook counterexample: $0\to1\ (-1)$, $0\to2\ (-2)$, $1\to2\ (-2)$. True distances
$[0, -1, -3]$.

- Textbook Dijkstra (no relaxation into a finalised vertex): $[0, -1, -2]$ — **wrong**.
- The lazy-deletion implementation of Lecture 17 §1: **correct**.

Expect most submissions to report "my implementation gets it right", which is the intended outcome.

### C2 (6) — deterministic

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

### C3 (4) — deterministic

**38 of 1,632** random negative-edge graphs without negative cycles give a wrong answer — **2.3%**.

Expected comment: a fault that appears on 2.3% of inputs will pass a small random test suite. Testing
cannot establish the absence of this bug; only the correctness argument can, and the argument tells
you the precondition rather than the symptom.

### C4 (3)

The step is $\delta(s,y) \le \delta(s,u)$, where $y$ lies on a shortest path to $u$ — i.e. **a prefix
of a shortest path is no longer than the whole path**. With a negative edge later on the path, the
remainder can have negative length and the prefix can be *longer* than the whole, so $y$ need not be
popped before $u$.

*Award 0 for "because Dijkstra is greedy" or "because it finalises vertices" — the question asks for
the step in the proof.*

---

## Part D — Bellman–Ford (24)

### D1 (6), D5 (3) — deterministic

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

### D2 (5) — deterministic

| $V$ | rounds | $V-1$ | $\log_2 V$ |
| --- | --- | --- | --- |
| 1,000 | 11 | 999 | 10.0 |
| 5,000 | 12 | 4,999 | 12.3 |
| 20,000 | 14 | 19,999 | 14.3 |

Expected: the rounds count measures the **maximum number of edges on any shortest path** — the graph's
hop-diameter — which on a random graph is $\Theta(\log V)$, not $\Theta(V)$.

*Full marks require naming the hop-diameter (or "most edges on a shortest path"). "It converges early"
is 2 of 5.*

### D3 (5) — deterministic

Path graph $0\to1\to\dots\to(V-1)$, edges presented in **reverse** order:

| $V$ | 5 | 10 | 20 | 50 |
| --- | --- | --- | --- | --- |
| rounds | 4 | 9 | 19 | **49** |

Same graph, edges in forward order: **2 rounds** at every $V$ (the second detects that nothing
changed).

Expected statement: **$O(VE)$ is a worst case over edge orderings**, not a property of the graph.

*This is the graded idea of Part D. A student who constructs a tight example but says the bound is
"about the graph" scores 3 of 5.*

### D4 (5) — machine-dependent

| $V$ | $E$ | Dijkstra | BF early | BF full | full/Dijkstra |
| --- | --- | --- | --- | --- | --- |
| 1,000 | 2,999 | 0.8 ms | 3.1 ms | 310.7 ms | **372×** |
| 3,000 | 8,998 | 3.3 ms | 8.9 ms | 2,615.9 ms | **793×** |

Mark the shape: early exit within a small constant of Dijkstra, no early exit hundreds of times
slower and getting worse.

---

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
| A | 22 |
| B | 24 |
| C | 18 |
| D | 24 |
| E | 12 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. Part C is the intellectual centre of this set** and will be the worst-answered. The sequence —
"you are told it fails", "the standard counterexample does not fail", "you must construct one",
"it fails 2.3% of the time" — is designed so that the only reliable route to the truth is the
correctness proof. Where a student got there, say so in the feedback; it is the skill the course is
for.

**2. Expect the D5 `TypeError`.** It is a genuine trap and I hit it myself writing these solutions.
Do not treat it as carelessness — it is caused by following the textbook's *detection* code and then
extending it to extraction, which is a reasonable thing to do and does not work.

**3. This set was released the week of MIDTERM 1.** Part A was flagged as doable beforehand. If the
submissions are weak in D and E specifically, that is time pressure and is the intended failure mode.

**4. Carried forward.** PS 4 E2 asked students to reconcile a bound with a measurement that seemed to
contradict it. **D2 and D3 are the same question again** — a bound that overstates the typical cost,
and a bound that is about something other than what students assume. Third time this has appeared
(Lab 3 D1, PS 4 E2, here); if a student has missed all three, that is worth a conversation rather than
another deduction.

**5. Forward.** Dijkstra's greedy correctness argument is the template for **Week 6**'s cut property
and **Week 9**'s exchange arguments. Bellman–Ford's recurrence over edge counts is a dynamic program,
and **Week 7 opens by pointing back at it** — flag this to students who ask what DP is.

---

*CS 102 · Week 5 · PS 5 Solutions · © CSE Department*
