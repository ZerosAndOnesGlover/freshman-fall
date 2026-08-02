# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 11.2 (L34) — Spanning Trees and Minimum Spanning Trees
### Wednesday, Week 11

---

## 1. Keeping Everything Connected, Cheaply

> **Definition.** A **spanning tree** of a connected graph $G$ is a subgraph that is a tree and
> includes **every** vertex of $G$.

It keeps the graph connected using as few edges as possible: exactly $n-1$, by Monday's theorem.

> **Theorem.** Every connected graph has a spanning tree.

**Proof.** If $G$ has a cycle, delete any edge of that cycle. The graph stays connected — the deleted
edge's endpoints are still joined by the rest of the cycle. Repeat. Each step removes one edge and
$G$ is finite, so the process terminates, and it stops precisely when no cycle remains: a connected
acyclic spanning subgraph. ∎

**The proof is an algorithm**, though a poor one. Wednesday's real algorithms build up rather than
tear down.

---

## 2. How Many Spanning Trees?

> **Theorem (Cayley, 1889).** The complete graph $K_n$ has $n^{n-2}$ **labelled** spanning trees.

**Verified by exhaustive enumeration** over all $\binom{\binom n2}{n-1}$ edge subsets:

| $n$ | Trees found | $n^{n-2}$ |
|---|---|---|
| 2 | 1 | 1 |
| 3 | 3 | 3 |
| 4 | 16 | 16 |
| 5 | 125 | 125 |
| 6 | 1296 | 1296 |

$K_{10}$ therefore has $10^8 = 100$ million spanning trees. **The number of spanning trees is
enormous, which is exactly why we need a way to find a good one without enumerating them.**

*(The general count for an arbitrary graph is given by the Matrix–Tree Theorem — a determinant of the
Laplacian. Beyond this course, but worth knowing it exists.)*

---

## 3. Minimum Spanning Trees

Now weight the edges — cost of laying cable, distance, latency.

> **Definition.** A **minimum spanning tree** (MST) is a spanning tree whose total edge weight is
> smallest.

### The running example

$$V=\{A,B,C,D,E,F\}$$

| Edge | Weight | | Edge | Weight |
|---|---|---|---|---|
| $AB$ | 4 | | $CD$ | 4 |
| $AC$ | 3 | | $CE$ | 5 |
| $BC$ | 1 | | $DE$ | 7 |
| $BD$ | 2 | | $DF$ | 3 |
| | | | $EF$ | 2 |

---

## 4. Kruskal's Algorithm — Sort and Add

> Sort all edges by weight. Add each edge in turn **unless it would create a cycle**. Stop at $n-1$
> edges.

**Verified trace:**

| Step | Edge | Weight | Action |
|---|---|---|---|
| 1 | $BC$ | 1 | add |
| 2 | $BD$ | 2 | add |
| 3 | $EF$ | 2 | add |
| 4 | $AC$ | 3 | add |
| 5 | $DF$ | 3 | add — now $5 = n-1$ edges, stop |

**Total weight: $1+2+2+3+3 = \mathbf{11}$**

Note step 3 adds $EF$ while $\{E,F\}$ is a component entirely separate from $\{B,C,D\}$. **Kruskal
grows a forest, not a tree**, and the pieces merge only at the end.

**Cycle detection** uses a *disjoint-set* (union–find) structure: two vertices already in the same
set means adding the edge closes a cycle. With union–find, Kruskal runs in $\Theta(m\log m)$,
dominated by the sort.

---

## 5. Prim's Algorithm — Grow One Tree

> Start at any vertex. Repeatedly add the **cheapest edge leaving the tree built so far**.

**Verified trace from $A$:**

| Step | Edge added | Weight | Tree vertices |
|---|---|---|---|
| 1 | $AC$ | 3 | $A,C$ |
| 2 | $CB$ | 1 | $A,B,C$ |
| 3 | $BD$ | 2 | $A,B,C,D$ |
| 4 | $DF$ | 3 | $A,B,C,D,F$ |
| 5 | $FE$ | 2 | all six |

**Total weight: $3+1+2+3+2 = \mathbf{11}$** — the same as Kruskal ✓

**The edge sets differ in order and the algorithms behave differently, yet the totals agree.** That is
not a coincidence: when edge weights are distinct the MST is unique; when they tie, different MSTs
may exist but **all have the same total weight**.

Prim runs in $\Theta(m\log n)$ with a binary heap.

---

## 6. Why Greedy Works Here

Greedy algorithms usually fail. They work for MSTs because of a structural fact:

> **Cut property.** For any partition of $V$ into two non-empty sets, the **minimum-weight edge
> crossing** between them belongs to some MST.

**Sketch.** Suppose an MST $T$ omits that minimum crossing edge $e$. Adding $e$ to $T$ creates a
cycle, which must cross the partition a second time, at some edge $f$ with weight $\ge$ that of $e$.
Swapping $f$ for $e$ keeps a spanning tree and does not increase the weight. ∎

Both algorithms are instances of this: Prim takes the cheapest edge across the cut (tree, rest);
Kruskal takes the globally cheapest edge that crosses *some* cut it has not yet bridged.

**Contrast with the Travelling Salesman Problem.** Greedy fails badly there, and TSP is NP-hard. The
difference is that MSTs have the cut property — the *local* cheapest choice is provably part of a
*global* optimum. Week 10's Euler-versus-Hamilton lesson again: structure, not effort, decides
whether a problem is easy.

---

## 7. Applications

| Application | What the MST gives |
|---|---|
| Network design | Cheapest cabling connecting all sites |
| Cluster analysis | Delete the $k-1$ heaviest MST edges to get $k$ clusters |
| Image segmentation | Regions as components after cutting expensive edges |
| Circuit layout | Minimum wire connecting all pins |
| Spanning Tree Protocol | Loop-free Ethernet routing — a live MST on the network |

**Ethernet switches genuinely run this.** A network with redundant links would broadcast-storm
forever without a spanning tree; the protocol computes one and disables the remaining links, keeping
them for failover.

---

## 8. Summary

| | |
|---|---|
| Spanning tree | Tree subgraph on all $n$ vertices; $n-1$ edges |
| Existence | Every connected graph has one |
| Cayley | $K_n$ has $n^{n-2}$ labelled spanning trees |
| **Kruskal** | Sort edges, add if no cycle; $\Theta(m\log m)$; grows a forest |
| **Prim** | Grow one tree by cheapest outgoing edge; $\Theta(m\log n)$ |
| Both on the example | Total weight $\mathbf{11}$ |
| Distinct weights | MST is unique |
| Tied weights | MSTs may differ, but the total is the same |
| Why greedy works | The **cut property** |

---

## 9. End-of-Lecture Exercises

1. How many labelled spanning trees does $K_7$ have? $K_{10}$?

2. Run Kruskal on the running example but break the weight-2 tie the other way ($BD$ after $EF$). Do you get the same tree? The same total?

3. Run Prim from $E$ instead of $A$. Tabulate the trace and confirm the total is still 11.

4. Give a connected weighted graph with two different MSTs, and verify their totals are equal.

5. Explain why an MST never contains the unique heaviest edge of a cycle.

6. **(Stretch.)** Prove the cut property in full, filling in the sketch of §6.

---

## Reading

- **Rosen, 8e §11.4–11.5** — Spanning trees and minimum spanning trees
- **Epp, 5e §10.6** — Spanning trees and shortest paths
- **Levin, 3e §4.3** — Trees and spanning trees

*Next: Lecture 11.3 — Breadth-First and Depth-First Search*
