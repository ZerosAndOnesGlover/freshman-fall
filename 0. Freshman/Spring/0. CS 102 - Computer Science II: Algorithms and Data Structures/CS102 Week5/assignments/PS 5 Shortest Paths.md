# CS 102 · Problem Set 5
## Shortest Paths

**Released:** Friday 26 February 2027, 10:00 (after L18) · Week 5
**Due:** Friday 5 March 2027, 17:00 · Week 6 — late penalty from 17:01 (syllabus late policy)
**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4–5 hours

**Submit:** `ps5.py` (runnable end to end) and `ps5.md` (written answers, tables, proofs).
Written answers inside code comments will not be marked.

Graphs are **directed** and 0-indexed unless stated otherwise. Use `heapq` for priority queues.
Represent graphs as an adjacency list `adj[u] = [(v, w), ...]` **and** an edge list
`edges = [(u, v, w), ...]` — Bellman–Ford wants the second.

## What this problem set uses

Weeks 0–5: DFS finish times from Week 4 (L15), relaxation, topological order and DAG shortest paths
(L16), Dijkstra with lazy deletion and its proof (L17), Bellman–Ford, early termination and negative
cycles (L18), and `heapq` (L12).

**Not needed and not expected:** A\* (Lab 5's job), Floyd–Warshall (Week 8), minimum spanning trees
(Week 6). No timing is asked for.

> **Midterm 1 is Monday 1 March 2027, 18:00** and covers Weeks 0–4, so nothing on this set is on it.
> Do Part A before the paper and the rest after.

---

## Part A — DAGs (20 points)

**A1.** *(5)* `topo_dfs(V, adj)` — topological order by decreasing DFS finish time, raising an error
on a cycle. `topo_kahn(V, adj)` — the in-degree method.

**A2.** *(5)* Verify both on at least 200 random DAGs: the output is a permutation of $0 \dots V-1$
and **every edge points forwards**. Report DAGs tested and failures.

Then answer: do the two algorithms produce the **same** order? Should they? One sentence.

**A3.** *(5)* `dag_sssp(V, adj, s)` in $\Theta(V+E)$ using a topological order.

Verify against Bellman–Ford on at least 200 random DAGs **from every source**, including DAGs with
**negative** edge weights. Report the number of DAGs, how many contained negative edges, and the
mismatches.

**A4.** *(5)* Answer both:

- **(a)** *(2)* `dag_sssp` handles negative weights, but Dijkstra does not. **Why is that safe here?**
  Two sentences.
- **(b)** *(3)* Compute **longest** paths on a DAG by negating weights, and verify against a direct
  computation on at least 200 DAGs. Then explain why the same trick fails on a general graph — and
  name what is true about longest paths on general graphs.

---

## Part B — Dijkstra (22 points)

**B1.** *(8)* `dijkstra(V, adj, s)` with a binary heap and lazy deletion, returning `dist` and
`parent`.

**B2.** *(6)* `path(parent, s, t)`. Verify that its total weight equals `dist[t]` on at least 100
random queries.

**B3.** *(8)* Verify Dijkstra against Bellman–Ford on at least 300 random **non-negative** graphs,
**from every source**. Report (graph, source) pairs compared and mismatches.

---

## Part C — When Dijkstra Is Wrong (20 points)

**C1.** *(6)* The textbook counterexample is $0\to1$ with weight $-1$, $0\to2$ with weight $-2$, and
$1\to2$ with weight $-2$.

Run **your** Dijkstra from B1 on it and report the answer alongside Bellman–Ford's. **Does your
implementation get it wrong?**

**C2.** *(10)* You should find that it does **not**. Explain why, then **find a graph on which your
implementation does fail.**

Report the graph, both answers, and the true distances. Establish the smallest $V$ for which your
implementation can fail, by exhaustive search over small weighted digraphs.

> Compare with the smallest $V$ for the textbook version. They are not the same number, and the
> difference is the point of Part C.

**C3.** *(4)* Identify the **single step** of the correctness proof in Lecture 17 §2 that uses
non-negativity, and state what goes wrong there without it.

---

## Part D — Bellman–Ford (26 points)

**D1.** *(8)* `bellman_ford(V, edges, s)` with the $V-1$ rounds and the extra detection round,
returning `None` (or raising) when a negative cycle is reachable from $s$.

**D2.** *(6)* Add **early termination**. Then, on random graphs of average degree 6 with
$V \in \{10^3, 5\times10^3, 2\times10^4\}$, report the rounds actually used alongside $V-1$ and
$\log_2 V$.

State what the rounds count actually measures — it is a property of the graph, and it is not $V$.

**D3.** *(6)* Show the $V-1$ bound is **tight**. Construct a graph and an *edge ordering* forcing
$V-1$ rounds, and report the rounds used for $V \in \{5, 10, 20, 50\}$.

Then reorder the same edge list so that it converges in 2 rounds, and report that too.

**State precisely what the $O(VE)$ bound is a worst case over.**

**D4.** *(6)* **Extract** a negative cycle rather than merely detecting one: return the actual vertex
sequence. Verify on at least 500 random graphs that every cycle you return is **simple** and has
**negative total weight**. Report counts.

---

## Part E — Choosing (12 points)

For each situation, name the algorithm you would use and justify it in two sentences. State the
complexity you get.

**E1.** *(2)* A social network, 10⁸ users, all edges weight 1. Distance between two given users.

**E2.** *(2)* A road network, 10⁷ junctions, weights are travel times in seconds.

**E3.** *(2)* A build system, 10⁴ tasks with dependencies and durations. The earliest possible
completion time.

**E4.** *(2)* A currency exchange with 200 currencies and a rate between every pair. Determine whether
a profitable sequence of trades exists.

**E5.** *(2)* A dense graph, $V = 3{,}000$, $E \approx 4.5\times10^6$, non-negative weights,
single-source.

**E6.** *(2)* A game map where moving onto a health pack has **negative** cost, 10⁵ tiles, and it is
guaranteed no loop gains health indefinitely.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 20 | Topological order and DAG shortest/longest paths |
| B | 22 | Dijkstra, verified against an independent reference |
| C | 20 | Finding the failure yourself, not being told about it |
| D | 26 | Bellman–Ford, the rounds bound, and negative cycles |
| E | 12 | Picking the right rung of the assumption ladder |
| **Total** | **100** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Counts are deterministic; timings are not.**

Verification totals — all should be **0 mismatches**:

| check | scale | result |
| --- | --- | --- |
| Dijkstra vs Bellman–Ford, non-negative | 4,071 (graph, source) pairs | 0 |
| DAG SSSP vs Bellman–Ford | 500 DAGs (351 with negative edges), 3,607 pairs | 0 |
| DAG longest path via negation | 300 DAGs | 0 |
| Topological order, both algorithms | 500 DAGs | 0 |
| Negative-cycle detection vs brute force | 600 digraphs (152 with a cycle) | 0 |

Part C:

| | smallest failing $V$ |
| --- | --- |
| textbook Dijkstra (no relaxation into finalised vertices) | **3** |
| lazy-deletion Dijkstra (as in Lecture 17 §1) | **4** |

Part D2, rounds used with early termination, random graphs of average degree 6:

| $V$ | rounds | $V-1$ | $\log_2 V$ |
| --- | --- | --- | --- |
| 1,000 | 11 | 999 | 10.0 |
| 5,000 | 12 | 4,999 | 12.3 |
| 20,000 | 14 | 19,999 | 14.3 |

---

## A Note on Part C

Every other part of this problem set asks you to build something that works. **Part C asks you to
break something you have already built**, and to establish exactly how hard it is to break.

You will be told, correctly, that Dijkstra fails on negative weights. You will then find that the
standard counterexample does not break your code, that a graph which does break it needs one more
vertex. (Lecture 17 §4 adds that on random inputs the failure rate is a couple of per cent.)

None of that makes Dijkstra safe on negative weights. It makes the bug **hard to find by testing** —
which is a different and more useful thing to know. A correctness argument is not a formality you
perform after the tests pass; on this problem it is the only thing that would have told you.

---

*CS 102 · Week 5 · Problem Set 5 · © CSE Department*
