# CS 102 · Problem Set 6
## Minimum Spanning Trees and Union-Find

**Released:** Friday, Week 6 · **Due:** Friday, Week 7, 23:59
**100 points · counts toward the Problem Sets component (35% of the final grade)**

**Submit:** `ps6.py` (runnable end to end) and `ps6.md` (written answers, tables, proofs).
Written answers inside code comments will not be marked.

Graphs are **undirected**, connected, and 0-indexed. Represent them as an edge list
`edges = [(u, v, w), ...]` and build adjacency lists where an algorithm needs them.

---

## Part A — The Two Properties (20 points)

**A1.** *(6)* Write a brute-force MST: enumerate every subset of $V-1$ edges, keep those forming a
spanning tree, return the minimum weight. This is your ground truth for Part B — it is exponential, so
keep $V \le 7$.

**A2.** *(7)* **Verify the cut property.** For at least 100 random graphs small enough to enumerate:
for **every** non-trivial cut, find the minimum-weight crossing edges and confirm that at least one of
them appears in at least one MST.

Report (graph, cut) pairs checked and violations.

Then: the property says a light crossing edge is in **some** MST. **Construct a graph and a cut where
a minimum crossing edge is in some MST but not in every MST**, and show both trees.

**A3.** *(7)* **Verify the cycle property**: the *strictly* heaviest edge on any cycle is in no MST.
Report cases checked and violations.

Then explain why "strictly" is necessary, by giving a cycle whose heaviest weight is **tied** and where
one of the tied edges *is* in an MST.

---

## Part B — Prim and Kruskal (20 points)

**B1.** *(6)* `kruskal(V, edges)` using your Part C union-find, returning total weight and edge list.

**B2.** *(6)* `prim_heap(V, adj, s)` using `heapq`, and `prim_dense(V, W)` in $\Theta(V^2)$ using a
`best[]` array and no priority queue.

**B3.** *(4)* Verify all three against the brute force of A1 on at least 100 graphs with $V \le 7$, and
against each other on at least 300 graphs with $V \le 40$. Report graphs tested and mismatches.

**B4.** *(4)* Prim and Dijkstra differ in **one expression**.

Put your `prim_heap` and your PS 5 `dijkstra` side by side, identify the difference, and explain in two
sentences why that single change turns "shortest path" into "minimum spanning tree".

---

## Part C — Union-Find (24 points)

**C1.** *(8)* One `DSU` class with a `kind` parameter selecting among four variants: **neither**
optimisation, **union by rank** only, **path compression** only, and **both**. Instrument it to count
parent-pointer steps.

**C2.** *(6)* For $n \in \{10^3, 5\times10^3, 2\times10^4, 10^5\}$, perform $n$ random unions then one
`find` per element. Tabulate the steps for all four variants.

State what the naive column's growth rate is, and give the speedup of *both* over *neither* at the
largest $n$.

**C3.** *(6)* **Construct the adversarial case.** Build a chain deliberately — union in an order that
makes the naive structure a path — then `find` every element.

Report steps for naive and for both-optimisations at $n \in \{10^3, 5\times10^3, 2\times10^4\}$. Give
**closed forms** for both columns and confirm your measurements match them exactly.

**C4.** *(4)* With both optimisations, report **steps per operation** for
$n \in \{10^3, 10^4, 10^5, 10^6\}$ alongside $\log_2 n$.

Then answer: the bound is $O(m\,\alpha(n))$ and $\alpha(n) \le 4$ for any storable $n$. **Is $\alpha$ a
constant?** Answer precisely in two sentences.

---

## Part D — Measuring (16 points)

**D1.** *(6)* Time Kruskal and Prim (heap) at $(V,E) \in \{(10^3, 5\times10^3),\ (5\times10^3,
2.5\times10^4),\ (2\times10^4, 10^5),\ (2\times10^3, 4\times10^5)\}$, best of 3. Confirm the MST
weights agree.

The textbook advice is "Kruskal for sparse, Prim for dense." **Do your measurements support it?**

**D2.** *(6)* Instrument Kruskal to time the **sort** and the **union-find loop** separately, at the
same sizes. Report both and the ratio.

Kruskal is $O(E\log E)$ for the sort and $O(E\,\alpha(V))$ for the unions, so the sort should dominate.
**Does it?** Explain your measurement without contradicting the complexity analysis.

**D3.** *(4)* Both of the following are true:

- asymptotically, the sort dominates;
- at every size you measured, it does not.

Reconcile them in three sentences or fewer, and state what would have to change for the asymptotic
prediction to become visible.

---

## Part E — Applications (20 points)

**E1.** *(5)* **Minimax.** Verify that for any $u, v$ the MST path minimises the maximum edge weight
over all $u$–$v$ paths, by comparing against a modified Dijkstra on the full graph. At least 200
graphs; report pairs checked and mismatches.

**E2.** *(5)* **Not a shortest-path tree.** Give the smallest graph you can find where the MST path
between two vertices is **longer** than their shortest path. Show both, and explain using the cycle
property why the MST *must* exclude the direct edge.

**E3.** *(6)* **Clustering.** Given $n$ points in the plane, build the MST of the complete Euclidean
graph, delete the $k-1$ heaviest edges, and report the resulting cluster sizes.

Test on 300 points in 4 well-separated Gaussian clusters. Report sizes for $k = 2 \dots 6$ **and the
weight of the smallest deleted edge at each $k$**.

Then: **how could you have chosen $k$ from that last column alone?**

**E4.** *(4)* MST weights are invariant under adding a constant to every edge, but shortest paths are
not.

Verify the first claim on at least 100 graphs. Then explain the difference in two sentences — the
reason is a counting fact about spanning trees.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 20 | The cut and cycle properties, verified and probed at their edges |
| B | 20 | Both algorithms, and the one line that separates Prim from Dijkstra |
| C | 24 | Union-Find, the adversarial case, and what $\alpha$ is |
| D | 16 | Measuring, and reconciling it with the analysis |
| E | 20 | Minimax, clustering, and the invariance argument |
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

Kruskal, sort against union-find (D2):

| $V$ | $E$ | sort | union-find | ratio |
| --- | --- | --- | --- | --- |
| 1,000 | 5,000 | 1.0 ms | 1.7 ms | 1.72 |
| 5,000 | 25,000 | 5.8 ms | 10.4 ms | 1.78 |
| 20,000 | 100,000 | 31.1 ms | 63.2 ms | 2.03 |
| 50,000 | 300,000 | 116.6 ms | 210.2 ms | 1.80 |

Kruskal against Prim (D1):

| $V$ | $E$ | Kruskal | Prim (heap) |
| --- | --- | --- | --- |
| 1,000 | 5,000 | 3.7 ms | 4.1 ms |
| 5,000 | 25,000 | 23.7 ms | 32.9 ms |
| 20,000 | 100,000 | 124.3 ms | 300.5 ms |
| 2,000 | 400,000 | 505.5 ms | 1,705.4 ms |

---

## A Note on Parts D and E3

**D2 and D3 ask you to explain a measurement that appears to contradict the complexity analysis.**
Neither is wrong. Complexity tells you the shape of a curve; it does not tell you where on that curve
your input sits, and it says nothing about whether one phase runs in C and the other in interpreted
bytecode. You have now met this four times — `SortedList` in Week 2, heap sort and `heapq.merge` in
Week 3, BFS locality in Week 4 — and it should be an expectation.

**E3's last question is the interesting one.** You are not told $k$. The MST's own edge weights tell
you: the deleted edges are large and similar while the clusters are genuinely separated, and then
there is a sudden drop. Finding that gap is how $k$ is chosen in practice, and it is a good example of
a data structure answering a question nobody built it for.

---

*CS 102 · Week 6 · Problem Set 6 · © CSE Department*
