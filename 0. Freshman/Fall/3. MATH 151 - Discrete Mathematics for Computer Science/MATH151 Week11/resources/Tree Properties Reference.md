# MATH 151 · Tree Properties Reference
## Week 11: Trees

---

## Definition and Equivalences

> A **tree** is a connected acyclic graph. A **forest** is an acyclic graph.

> **For a graph on $n$ vertices, these are equivalent:**
> 1. Connected and acyclic
> 2. Connected with exactly $n-1$ edges
> 3. Acyclic with exactly $n-1$ edges
> 4. A **unique** path between every pair of vertices
> 5. Connected, and removing **any** edge disconnects it

**(2) is the practical test.** **(4)** is why file systems and routing use trees. **(5)** says every
edge of a tree is a **bridge** — trees have zero redundancy.

---

## Counting Facts

| | |
|---|---|
| Edges | $n-1$ |
| Degree sum | $2(n-1)$ |
| Leaves ($n\ge2$) | At least **2** |
| Adding any edge | Creates exactly one cycle |
| Removing any edge | Disconnects into exactly two components |

*Verified on $T$: $V=\{a,\ldots,g\}$, $E=\{ab,ac,bd,be,cf,cg\}$ — 7 vertices, 6 edges, degrees
$(2,3,3,1,1,1,1)$ summing to 12, four leaves $d,e,f,g$.*

**Every tree is bipartite** — it has no cycles at all, so no odd ones.

---

## Rooted Trees

Choosing a root gives each non-root vertex a unique **parent**.

| Term | Meaning |
|---|---|
| Depth of $v$ | Path length from the root |
| Height | Maximum depth |
| Leaf | No children |
| Subtree at $v$ | $v$ and its descendants |

**Rooting is a choice, not a property.** Verified heights of $T$ by root:

| Root | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ |
|---|---|---|---|---|---|---|---|
| Height | **2** | 3 | 3 | 4 | 4 | 4 | 4 |

The height-minimising root ($a$ here) is a **centre** of the tree.

---

## Binary Trees

**Full**: every internal node has exactly 2 children. **Perfect**: full, with all leaves at the same
depth.

> Height $h$ ⟹ at most $2^{h+1}-1$ nodes, at least $h+1$.
> $n$ nodes ⟹ height at least $\lceil\log_2(n+1)\rceil-1$.

| $h$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Max nodes | 1 | 3 | 7 | 15 | 31 |
| Min nodes | 1 | 2 | 3 | 4 | 5 |

| $n$ | 7 | 8 | 15 | 16 | 1000 | $10^6$ |
|---|---|---|---|---|---|---|
| Min height | 2 | 3 | 3 | 4 | **9** | **19** |

**This is why balanced trees exist.** A BST on $10^6$ items can have height $10^6-1$ (a degenerate
path) or $19$. AVL and red–black trees force the second.

---

## Spanning Trees

> A **spanning tree** is a tree subgraph containing every vertex. Every connected graph has one.

**Cayley's formula:** $K_n$ has $n^{n-2}$ labelled spanning trees.

| $n$ | 2 | 3 | 4 | 5 | 6 | 7 | 10 |
|---|---|---|---|---|---|---|---|
| Trees | 1 | 3 | 16 | 125 | 1296 | 16 807 | $10^8$ |

*Verified by exhaustive enumeration for $n\le6$.*

---

## Minimum Spanning Trees

**Running example**, $V=\{A,\ldots,F\}$:

| Edge | $AB$ | $AC$ | $BC$ | $BD$ | $CD$ | $CE$ | $DE$ | $DF$ | $EF$ |
|---|---|---|---|---|---|---|---|---|---|
| Weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 3 | 2 |

### Kruskal — sort and add

Sort edges; add unless it makes a cycle; stop at $n-1$. **Verified:** $BC(1), BD(2), EF(2), AC(3),
DF(3)$ — total **11**. Uses union–find; $\Theta(m\log m)$. **Grows a forest.**

### Prim — grow one tree

From a start vertex, repeatedly add the cheapest edge leaving the tree. **Verified from $A$:**
$AC(3), CB(1), BD(2), DF(3), FE(2)$ — total **11**. Uses a heap; $\Theta(m\log n)$.
*From $E$: also 11.*

> **Different edge orders, different edge sets possible, always the same total.** With distinct
> weights the MST is unique; with ties the totals still agree.

### Why greedy works — the cut property

> For any partition of $V$ into two non-empty parts, the minimum-weight crossing edge is in some MST.

This is what MSTs have and the Travelling Salesman Problem lacks — which is why one is easy and the
other NP-hard.

---

## Traversal

| | Structure | Order on $T$ from $a$ | Finds |
|---|---|---|---|
| **BFS** | Queue (FIFO) | $a,b,c,d,e,f,g$ | Shortest paths (unweighted) |
| **DFS** | Stack (LIFO) | $a,b,d,e,c,f,g$ | Components, cycles, topological order |

Both $\Theta(n+m)$ on an adjacency list.

**Traversal order depends on the start vertex and on the adjacency-list ordering** — it is not
canonical.

*From $b$: BFS gives $b,a,d,e,c,f,g$; DFS gives $b,a,c,f,g,d,e$.*

**Weighted graphs need Dijkstra.** BFS is the special case where all weights are 1.

---

## Topological Sort

> A topological order exists **iff** the digraph is acyclic.

Kahn's algorithm: repeatedly remove a vertex of in-degree 0. If fewer than $n$ come out, there is a
cycle.

*Verified on $a\to b$, $a\to c$, $b\to d$, $c\to d$, $d\to e$: the orders are $abcde$ and $acbde$ —
**two** of them, since $b$ and $c$ are unordered relative to each other.*

*Verified on $a\to b\to c\to a$: reports failure, correctly.*

**Every build system does this.** "Circular dependency detected" is a topological sort failing — and
when the dependencies really do form a cycle, **no valid build order exists**.

---

## Common Errors

| ❌ | ✅ |
|---|---|
| Treating height as a property of the tree | It depends on the root |
| Assuming Kruskal builds one connected tree | It grows a **forest** that merges at the end |
| Expecting Kruskal and Prim to give identical edge sets | Only the **totals** must agree |
| Using BFS for shortest paths with weights | Use Dijkstra |
| Treating a BFS order as canonical | It depends on the adjacency-list order |
| Reading "no topological order" as a bug | It is a correct report of a cycle |

---

*MATH 151 · Week 11 · Reference · © CSE Department*
