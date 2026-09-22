# CS 102 · Computer Science II
## Lecture 20: Prim's and Kruskal's Algorithms

**Date:** Wednesday 3 March 2027 · 09:00–09:50 · Week 6

---

## 1. Two Ways to Apply One Theorem

The cut property says a minimum-weight edge across any cut is safe. It does not say *which* cut to
use, and that single freedom produces the two classic algorithms.

| | Prim | Kruskal |
| --- | --- | --- |
| maintains | one growing **tree** | a **forest** of fragments |
| the cut used | (tree so far) vs (everything else) | the components joined by the next edge |
| picks | the cheapest edge leaving the tree | the cheapest edge left in the graph |
| data structure | priority queue | disjoint-set union |

**Neither is more correct.** Both are the cut property; they differ in which cut they apply it to, and
therefore in what they need to maintain.

*(Verified: Prim and Kruskal agree with each other, and with a brute-force minimum over **all**
spanning trees, on 295 random graphs small enough to enumerate — **0 mismatches** — and agree with each
other on a further 500 graphs of up to 40 vertices.)*

---

## 2. Prim's Algorithm

Grow one tree from an arbitrary start vertex, repeatedly adding the cheapest edge that leaves it.

```python
def prim(V, adj, s=0):
    in_mst = [False] * V
    total = 0; tree = []
    pq = [(0, s, -1)]                              # (weight, vertex, parent)
    while pq:
        w, u, par = heapq.heappop(pq)
        if in_mst[u]: continue                     # stale entry
        in_mst[u] = True
        if par >= 0: total += w; tree.append((par, u, w))
        for v, ww in adj[u]:
            if not in_mst[v]: heapq.heappush(pq, (ww, v, u))
    return total, tree
```

**Compare this with Dijkstra, line by line.** They are the same algorithm with **one difference**:

```python
# Dijkstra:  push the total distance from the source
if d + w < dist[v]: heapq.heappush(pq, (dist[v], v))

# Prim:      push the weight of this single edge
heapq.heappush(pq, (ww, v, u))
```

Dijkstra's key is *distance from the source*; Prim's key is *distance from the tree*. That is the
whole difference, and it is exactly the difference between the two problems: Dijkstra cares how far
you have come, Prim only cares what the next edge costs.

**Cost:** $O((V+E)\log V)$ with a binary heap, identically to Dijkstra and for identical reasons.

**On a dense graph, do not use a heap.** With $E \approx V^2$ the simple $\Theta(V^2)$ version — keep a
`best[]` array and scan it for the minimum — wins, exactly as with Dijkstra. Lab 6 uses a complete
geometric graph, where the $\Theta(V^2)$ form is the right choice and is also simpler.

---

## 3. Kruskal's Algorithm

Sort all edges by weight. Take each in turn, keeping it if it joins two different components.

```python
def kruskal(V, edges):
    dsu = DSU(V)
    total = 0; tree = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):                        # False if already connected
            total += w; tree.append((u, v, w))
    return total, tree
```

**Why it is correct.** When we consider edge $(u,v)$ and they are in different components, consider
the cut separating $u$'s component from everything else. All lighter edges have been processed and
none of them crossed this cut — otherwise the components would already be joined. So $(u,v)$ is a
minimum-weight edge crossing that cut, and the cut property makes it safe.

When $u$ and $v$ are already connected, the path between them uses only lighter edges, so $(u,v)$ is
the strictly heaviest edge on the cycle it would close, and the **cycle property** rejects it.

**Kruskal needs both properties. Prim needs only the cut property.** That is the honest structural
difference between them.

**Cost:** $O(E \log E)$ for the sort, plus $E$ near-constant `union`/`find` operations — Lecture 21.
Since $E \le V^2$, $\log E \le 2\log V$, so this is also written $O(E\log V)$.

---

## 4. Which to Use

The textbook answer is: Kruskal on sparse graphs, Prim on dense ones. Measured, on this machine:

| $V$ | $E$ | Kruskal | Prim (heap) | winner |
| --- | --- | --- | --- | --- |
| 1,000 | 5,000 | 3.7 ms | 4.1 ms | Kruskal |
| 5,000 | 25,000 | 23.7 ms | 32.9 ms | Kruskal |
| 20,000 | 100,000 | 124.3 ms | 300.5 ms | **Kruskal, 2.4×** |
| 2,000 | 400,000 | 505.5 ms | 1,705.4 ms | **Kruskal, 3.4×** |

*(Total MST weights identical in every case.)*

**Kruskal wins every row, including the dense one** — which is not what the textbook advice predicts.
The reason is a Python fact, not a graph fact: Kruskal's dominant cost is `sorted()`, which is C, while
Prim's inner loop is interpreted bytecode running once per edge. Prim's advantage on dense graphs
comes from *not sorting*, and in CPython not sorting is not much of an advantage.

Rewrite both in C and the ordering would change. **This is the fourth time this term** — after
`SortedList` in Week 2, heap sort in Week 3, and `heapq.merge` in Week 3 — that the asymptotically
indicated choice has lost to the one with more work happening in a lower-level language. It should
now be an expectation rather than a surprise.

> **What to actually do.** Use Kruskal when edges arrive already sorted or nearly so, when you want
> the clustering by-product of Lecture 21 §5, or when you are in a language where sorting is cheap.
> Use Prim — the $\Theta(V^2)$ array version, not the heap — when the graph is dense and especially
> when it is *implicit*, as in Lab 6, where materialising all $\binom{n}{2}$ edges is the expensive
> part.

---

## 5. Where Kruskal's Time Goes

Kruskal is $O(E\log E)$ for the sort and $O(E\,\alpha(V))$ for the disjoint-set work, so the sort
should dominate. Measured:

| $V$ | $E$ | sort | union-find | union/sort |
| --- | --- | --- | --- | --- |
| 1,000 | 5,000 | 1.0 ms | 1.7 ms | 1.72 |
| 5,000 | 25,000 | 5.8 ms | 10.4 ms | 1.78 |
| 20,000 | 100,000 | 31.1 ms | 63.2 ms | 2.03 |
| 50,000 | 300,000 | 116.6 ms | 210.2 ms | 1.80 |

**The union-find phase costs about 1.8× the sort**, stably across sizes — the opposite of what the
complexity says.

Both facts are true at once, and holding them together is the point:

- **Asymptotically the sort dominates.** $\log E$ grows without bound; $\alpha(V)$ is at most 4 for any
  input that fits in memory. At large enough $E$ the sort must win.
- **At every size measured here it does not**, because `sorted()` is a C routine and the union-find
  loop is interpreted Python, and the ratio between those constants is larger than $\log E / \alpha(V)$
  over this whole range.

The ratio is flat at ~1.8 rather than shrinking, which tells you $\log E$ has not begun to matter yet.
**A complexity comparison tells you the shape of the curve, not where you are on it.**

---

## 6. Other Algorithms

**Borůvka's algorithm** (1926, the oldest of the three). In each round, every component simultaneously
picks its own cheapest outgoing edge; add them all and merge. The component count at least halves each
round, so it finishes in $O(\log V)$ rounds of $O(E)$ work — $O(E\log V)$.

Its virtue is that the rounds are **independent across components**, so it parallelises where Prim and
Kruskal do not. Every practical parallel and distributed MST algorithm descends from it.

**Better bounds exist.** Karger–Klein–Tarjan gives a randomised **linear-time** MST algorithm, and
Chazelle's deterministic $O(E\,\alpha(V))$ is very nearly linear. Neither is used in practice: the
constants are large and the implementations are difficult. **Kruskal and Prim remain what everyone
writes**, which is worth knowing about the relationship between the literature and practice.

---

## 7. What to Do

- Read CLRS §21.2 — both algorithms, and the proofs, in 10 pages.
- **PS 6** implements both and compares them, and asks you to explain the timing result in §4 rather
  than to repeat the textbook advice.
- **Lab 6** lays cable on a campus, where the graph is complete and implicit.
- Next lecture: the disjoint-set structure that makes Kruskal work, and what MSTs are used for.

---

*CS 102 · Week 6 · Lecture 20 · © CSE Department*
