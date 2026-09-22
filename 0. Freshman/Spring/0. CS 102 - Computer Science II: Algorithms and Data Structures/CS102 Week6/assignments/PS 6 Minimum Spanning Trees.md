# CS 102 · Problem Set 6
## Minimum Spanning Trees and Union-Find

**Released:** Friday 5 March 2027, 10:00 (after L21) · Week 6
**Due:** Friday 12 March 2027, 17:00 · Week 7 — late penalty from 17:01 (syllabus late policy)
**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4–5 hours

**Submit:** `ps6.py` (runnable end to end) and `ps6.md` (written answers, tables, proofs).
Written answers inside code comments will not be marked.

Graphs are **undirected**, connected, and 0-indexed. Represent them as an edge list
`edges = [(u, v, w), ...]` and build adjacency lists where an algorithm needs them.

## What this problem set uses

Weeks 0–6: BFS (L14) and Dijkstra (L17) from earlier weeks, the cut and cycle properties and the
minimax property (L19), Prim and Kruskal (L20), and union–find with both optimisations (L21).

**Not needed and not expected:** dynamic programming (Week 7). Timing Kruskal against Prim and MST
clustering are Lab 6's job, not this set's.

---

## Part A — The Two Properties (22 points)

**A1.** *(6)* Write a brute-force MST: enumerate every subset of $V-1$ edges, keep those forming a
spanning tree, return the minimum weight. This is your ground truth for Part B — it is exponential, so
keep $V \le 7$.

**A2.** *(8)* **Verify the cut property.** For at least 100 random graphs small enough to enumerate:
for **every** non-trivial cut, find the minimum-weight crossing edges and confirm that at least one of
them appears in at least one MST.

Report (graph, cut) pairs checked and violations.

Then: the property says a light crossing edge is in **some** MST. **Construct a graph and a cut where
a minimum crossing edge is in some MST but not in every MST**, and show both trees.

**A3.** *(8)* **Verify the cycle property**: the *strictly* heaviest edge on any cycle is in no MST.
Report cases checked and violations.

Then explain why "strictly" is necessary, by giving a cycle whose heaviest weight is **tied** and where
one of the tied edges *is* in an MST.

---

## Part B — Prim and Kruskal (22 points)

**B1.** *(6)* `kruskal(V, edges)` using your Part C union-find, returning total weight and edge list.

**B2.** *(6)* `prim_heap(V, adj, s)` using `heapq`, and `prim_dense(V, W)` in $\Theta(V^2)$ using a
`best[]` array and no priority queue.

**B3.** *(5)* Verify all three against the brute force of A1 on at least 100 graphs with $V \le 7$, and
against each other on at least 300 graphs with $V \le 40$. Report graphs tested and mismatches.

**B4.** *(5)* Prim and Dijkstra differ in **one expression**.

Put your `prim_heap` and your PS 5 `dijkstra` side by side, identify the difference, and explain in two
sentences why that single change turns "shortest path" into "minimum spanning tree".

---

## Part C — Union-Find (30 points)

**C1.** *(9)* One `DSU` class with a `kind` parameter selecting among four variants: **neither**
optimisation, **union by rank** only, **path compression** only, and **both**. Instrument it to count
parent-pointer steps.

**C2.** *(7)* For $n \in \{10^3, 5\times10^3, 2\times10^4, 10^5\}$, perform $n$ random unions then one
`find` per element. Tabulate the steps for all four variants.

State what the naive column's growth rate is, and give the speedup of *both* over *neither* at the
largest $n$.

**C3.** *(8)* **Construct the adversarial case.** Build a chain deliberately — union in an order that
makes the naive structure a path — then `find` every element.

Report steps for naive and for both-optimisations at $n \in \{10^3, 5\times10^3, 2\times10^4\}$. Give
**closed forms** for both columns and confirm your measurements match them exactly.

**C4.** *(6)* With both optimisations, report **steps per operation** for
$n \in \{10^3, 10^4, 10^5, 10^6\}$ alongside $\log_2 n$.

Then answer: the bound is $O(m\,\alpha(n))$ and $\alpha(n) \le 4$ for any storable $n$. **Is $\alpha$ a
constant?** Answer precisely in two sentences.

---

## Part D — Applications (26 points)

**D1.** *(9)* **Minimax.** Verify that for any $u, v$ the MST path minimises the maximum edge weight
over all $u$–$v$ paths. Your reference: the best possible maximum edge for $u$–$v$ is the smallest
weight $w$ such that $u$ and $v$ are connected using only edges of weight $\le w$ — test each
candidate $w$ with a BFS (Lecture 14). At least 200 graphs; report pairs checked and mismatches.

**D2.** *(8)* **Not a shortest-path tree.** Give the smallest graph you can find where the MST path
between two vertices is **longer** than their shortest path. Show both, and explain using the cycle
property why the MST *must* exclude the direct edge.

**D3.** *(9)* MST weights are invariant under adding a constant to every edge, but shortest paths are
not.

Verify the first claim on at least 100 graphs. Then explain the difference in two sentences — the
reason is a counting fact about spanning trees.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 22 | The cut and cycle properties, verified and probed at their edges |
| B | 22 | Both algorithms, and the one line that separates Prim from Dijkstra |
| C | 30 | Union-Find, the adversarial case, and what $lpha$ is |
| D | 26 | Minimax, and the invariance argument |
| **Total** | **100** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Counts are deterministic; timings are not.**

Verification (all should be 0):

| check | scale | result |
| --- | --- | --- |
| Prim = Kruskal = brute force | 295 graphs, $V \le 7$ | 0 |
| Prim = Kruskal | 500 graphs, $V \le 40$ | 0 |
| cut property | 3,191 (graph, cut) pairs | 0 |
| cycle property | 758 (cycle, heaviest edge) cases | 0 |
| minimax property | 15,988 (source, target) pairs | 0 |
| MST invariant under $+100$ on every edge | 300 graphs | 0 |

Union-find steps, $n$ random unions then one `find` each (C2):

| $n$ | neither | rank | compression | both |
| --- | --- | --- | --- | --- |
| 1,000 | 81,403 | 3,479 | 4,240 | 2,450 |
| 5,000 | 1,978,844 | 18,040 | 22,987 | 12,243 |
| 20,000 | 30,823,531 | 72,486 | 99,855 | 49,232 |
| 100,000 | 779,553,223 | 379,496 | 542,521 | 246,855 |

Adversarial chain (C3):

| $n$ | naive | both |
| --- | --- | --- |
| 1,000 | 499,500 | 999 |
| 5,000 | 12,497,500 | 4,999 |
| 20,000 | 199,990,000 | 19,999 |

Steps per operation with both optimisations (C4): **1.225, 1.222, 1.234, 1.235** at
$n = 10^3, 10^4, 10^5, 10^6$.

---

## A Note on Part C

**C3 and C4 ask for exact counts, not timings.** The closed forms in C3 are the whole point: the naive
structure pays $n(n-1)/2$ steps on the chain and the optimised one pays $n-1$, and your measurements
should match both exactly. C4 then asks what "$\alpha(n) \le 4$" does and does not mean — a bound
that never exceeds 4 in practice is still a growing function, and saying so precisely is the mark.

---

*CS 102 · Week 6 · Problem Set 6 · © CSE Department*
