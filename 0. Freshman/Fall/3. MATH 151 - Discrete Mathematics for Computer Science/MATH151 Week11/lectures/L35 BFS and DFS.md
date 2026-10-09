# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 35 (L35) — Breadth-First and Depth-First Search
### Friday, Week 11

*“A mathematical problem should be difficult in order to entice us, yet not completely inaccessible, lest it mock at our efforts. It should be to us a guide post on the mazy paths to hidden truths.”* — David Hilbert, "Mathematical Problems" (1900)

**Date:** Friday 11 December 2026 · 13:00–13:50 · Week 11

**Reading:** Rosen, 8e §11.4 · Epp, 5e §10.6 *(details at the end of the lecture)*

**Coursework:** 📝 **PS 10** due today 17:00 · 📝 **PS 11** released today 14:00, due Fri 18 Dec 17:00 · 📊 **Quiz 12** Mon 14 Dec 13:00–13:15 · 🔬 **Lab 11** Wed 16 Dec 15:00–16:50 · 📕 **Final exam** Mon 21 Dec 08:00–10:00

---

## 1. One Algorithm, Two Data Structures

Both traversals do the same thing: start somewhere, keep a collection of vertices discovered but not
yet processed, and repeatedly take one out and add its unvisited neighbours.

**The only difference is which end of the collection you take from.**

| | Collection | Take from | Explores |
|---|---|---|---|
| **BFS** | Queue | Front (FIFO) | Level by level |
| **DFS** | Stack | Top (LIFO) | One branch to the end |

```python
def bfs(adj, start):
    seen, order, q = {start}, [], deque([start])
    while q:
        u = q.popleft()          # FIFO
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    return order
```

Replace `q.popleft()` with `stack.pop()` and you have DFS. **That one method call is the entire
distinction**, and everything below follows from it.

Both run in $\Theta(n+m)$ on an adjacency list: each vertex enters the collection once, and each edge
is examined once from each end.

---

## 2. The Traversals Compared

Using Monday's tree $V=\{a,\ldots,g\}$, $E=\{ab,ac,bd,be,cf,cg\}$ with neighbours in alphabetical
order:

| | Order from $a$ |
|---|---|
| **BFS** | $a,\ b,\ c,\ d,\ e,\ f,\ g$ |
| **DFS** (preorder) | $a,\ b,\ d,\ e,\ c,\ f,\ g$ |

*(Both verified.)*

BFS finishes depth 1 ($b,c$) before touching depth 2. DFS commits to $b$, exhausts everything below
it, and only then returns to $c$.

> **Traversal order is not a property of the graph.** It depends on the start vertex *and* on the
> order neighbours appear in the adjacency list. Never treat a BFS order as canonical.

---

## 3. What Each One Is Good For

### BFS finds shortest paths

> **Theorem.** In an **unweighted** graph, BFS from $s$ visits every vertex in non-decreasing order
> of distance from $s$, and the BFS tree path from $s$ to $v$ is a shortest path.

**Why:** the queue holds vertices in discovery order, and a vertex at distance $k$ can only be
discovered from one at distance $k-1$. The FIFO discipline guarantees all of level $k-1$ is processed
before any of level $k$.

**This fails the moment edges have weights.** Then "fewest edges" and "shortest distance" diverge, and
you need Dijkstra's algorithm. BFS is Dijkstra with all weights equal to 1.

**Uses:** shortest routes, degrees of separation in a social graph, web crawling by link depth,
solving a puzzle in the fewest moves.

### DFS reveals structure

DFS naturally computes, in a single pass:

| Task | How |
|---|---|
| Connected components | One DFS per unvisited vertex |
| Cycle detection | An edge to a vertex already on the current stack |
| Topological sort | Reverse order of finishing times |
| Bridges and cut vertices | Tarjan's low-link values |
| Strongly connected components | Two passes of DFS |

**Uses:** dependency resolution, maze generation, backtracking search, garbage collection's mark
phase.

---

## 4. Topological Sort

> **Definition.** A **topological order** of a directed graph lists the vertices so that every edge
> points forwards.

> **Theorem.** A topological order exists **iff** the graph is acyclic (a DAG).

**Verified example.** With $a\to b$, $a\to c$, $b\to d$, $c\to d$, $d\to e$, Kahn's algorithm —
repeatedly remove a vertex of in-degree 0 — yields

$$a,\ b,\ c,\ d,\ e$$

*(Note $b$ and $c$ could be swapped; topological orders are generally not unique.)*

**And on a cycle it correctly reports failure.** For $a\to b\to c\to a$ the algorithm finds no vertex
of in-degree 0 and terminates having output fewer than $n$ vertices — *verified*.

**This is what every build system does.** `make`, `cargo`, `npm`, and every package manager
topologically sorts a dependency DAG. When you see "circular dependency detected", a topological sort
just failed exactly as above — and the error is not a limitation of the tool. **If the dependencies
genuinely form a cycle, no valid build order exists.**

---

## 5. Trees From Traversals

Running BFS or DFS on a connected graph and recording the edge that first discovered each vertex
produces a **spanning tree** — the BFS tree or DFS tree.

| | Shape | Property |
|---|---|---|
| BFS tree | Short and wide | Root-to-$v$ paths are shortest paths |
| DFS tree | Tall and narrow | Non-tree edges connect ancestors to descendants |

Both are spanning trees of the same graph, generally different, both with $n-1$ edges. This gives a
third construction to add to Thursday's Kruskal and Prim — though neither traversal tree is
minimum-weight, since neither consults the weights.

---

## 6. Summary

| | |
|---|---|
| BFS / DFS differ only in | queue vs stack |
| Both cost | $\Theta(n+m)$ on an adjacency list |
| BFS order on the example | $a,b,c,d,e,f,g$ |
| DFS preorder on the example | $a,b,d,e,c,f,g$ |
| Traversal order | Depends on start **and** on adjacency-list order |
| **BFS** | Shortest paths in **unweighted** graphs |
| Weighted graphs | Need Dijkstra; BFS is the all-weights-1 case |
| **DFS** | Components, cycles, topological sort, bridges, SCCs |
| Topological order exists | **iff** the graph is a DAG |
| Traversal trees | Both are spanning trees; neither is minimum |

---

## 7. End-of-Lecture Exercises

1. Give the BFS and DFS orders from $b$ on the running tree, with neighbours in alphabetical order.

2. Explain why BFS from $s$ can be used to compute the distance from $s$ to every other vertex, but DFS cannot.

3. Find all topological orders of the DAG $a\to b$, $a\to c$, $b\to d$, $c\to d$, $d\to e$.

4. A graph is bipartite iff it has no odd cycle. Describe how to test bipartiteness with a single BFS.

5. Give a graph where the BFS tree and the DFS tree from the same start vertex differ, and draw both.

6. **(Stretch.)** Show that a directed graph has a cycle iff some DFS encounters an edge to a vertex currently on the recursion stack. Why is "already visited" not enough?

---

## Reading

- **Rosen, 8e §11.4** — Spanning trees, BFS and DFS
- **Epp, 5e §10.6** — Spanning trees and a shortest path algorithm

*Next: Week 12 — Number Theory: Divisibility, Primes, Modular Arithmetic*
