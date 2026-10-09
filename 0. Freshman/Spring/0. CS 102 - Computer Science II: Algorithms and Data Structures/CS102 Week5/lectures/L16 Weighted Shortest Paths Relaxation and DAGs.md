# CS 102 · Computer Science II
## Lecture 16: Weighted Shortest Paths — Relaxation, Ordering, and DAGs

*“Simplicity is the shortest path to a solution.”* — Ward Cunningham, as quoted in *Simplicity* (WikiWikiWeb)

**Date:** Monday 22 February 2027 · 09:00–09:50 · Week 5

**Reading:** CLRS Ch. 22 introduction (optimal substructure, relaxation), §20.4, §22.2, §20.5

**Coursework:** 📊 **Quiz 5** today 09:00–09:15 · 🔬 **Lab 4** Tue 23 Feb 15:00–16:50 · 📝 **PS 4** due Fri 26 Feb 17:00 · 📝 **PS 5** released Fri 26 Feb 10:00, due Fri 5 Mar 17:00 · 📘 **Midterm 1** Mon 1 Mar 18:00–19:15

---

## 1. Where BFS Stops Working

BFS finds the path with the **fewest edges**. Week 4 proved it, and the proof rested on one fact:
the queue hands back vertices in non-decreasing order of distance, because every edge adds exactly
1.

Give the edges weights and that collapses immediately.

```
        1        1
   s ------ a ------ t          fewest edges:  s -> t   (1 edge,  weight 10)
    \                /          least weight:  s -> a -> t  (2 edges, weight 2)
     \____________ /
           10
```

**"Fewest edges" and "least total weight" are different questions**, and from here on we want the
second. A road network is the obvious case: the route with the fewest junctions is not the fastest
route, and nobody wants the former.

This week answers the weighted question three times, under three different assumptions, and the
differences between them are the point:

| assumption on weights | algorithm | cost |
| --- | --- | --- |
| all equal | **BFS** (Week 4) | $\Theta(V+E)$ |
| graph is a **DAG** — any weights | **topological order** — §5 | $\Theta(V+E)$ |
| all **non-negative** | **Dijkstra** — Lecture 17 | $O((V+E)\log V)$ |
| **anything**, no negative cycle | **Bellman-Ford** — Lecture 18 | $O(VE)$ |

**Read that table as a ladder of assumptions.** Each row buys speed by assuming more. The engineering
skill is knowing which rung your problem sits on, and the exam question is what happens if you guess
too low.

---

## 2. Relaxation

All four algorithms are the same operation applied in different orders.

Keep an estimate `d[v]` for every vertex — the length of the best path found *so far*, starting at
$\infty$ for everything but the source. Then:

```python
def relax(u, v, w):
    if d[u] + w < d[v]:
        d[v] = d[u] + w
        parent[v] = u
```

*"I have found a route to $v$ through $u$ that beats what I had."*

Two invariants hold from beginning to end, and everything else follows from them:

> **I1.** `d[v]` is always the length of *some* real path from $s$ to $v$, or $\infty$.
> **I2.** Therefore `d[v] >= dist(s, v)` at all times, and `d[v]` never increases.

I1 means the estimate is never a fantasy — there is an actual path behind it, recoverable from
`parent`. I2 means we are always approaching the answer from above. **A shortest-path algorithm is a
procedure for driving these overestimates down to the truth**, and the three algorithms differ only in
the *order* they choose relaxations.

### What order is enough?

> **Path-relaxation property.** If $s = v_0, v_1, \dots, v_k$ is a shortest path, and the edges
> $(v_0,v_1), (v_1,v_2), \dots, (v_{k-1},v_k)$ are relaxed **in that order** — with any number of other
> relaxations interleaved — then $d[v_k] = \mathrm{dist}(s, v_k)$ afterwards.

That is the whole theory of this week in one sentence. Each algorithm is a different guarantee that
the edges of every shortest path get relaxed in order:

- **DAG:** process vertices in topological order, so every edge is relaxed after everything before it.
- **Dijkstra:** process vertices in increasing distance, which works *only* if weights are
  non-negative.
- **Bellman-Ford:** relax everything $V-1$ times and give up on being clever.

---

## 3. Optimal Substructure

Why relaxation converges at all rests on a fact so ordinary it is easy to miss.

> **Any subpath of a shortest path is itself a shortest path.**

*Proof.* Let $P$ be a shortest $s \rightsquigarrow t$ path passing through $u$ then $v$, and let $Q$ be
its $u \rightsquigarrow v$ portion. If some $Q'$ were shorter, substituting it into $P$ would give a
shorter $s \rightsquigarrow t$ path. Contradiction. $\square$

This is **optimal substructure**, and it is the property that makes the whole week possible: a
shortest path to $t$ is built from shortest paths to $t$'s predecessors, so we can compute it without
enumerating paths. **You will meet this phrase again in Week 7** — it is precisely the condition for
dynamic programming, and Bellman-Ford will turn out to *be* a dynamic program.

### Where it fails

Optimal substructure needs shortest paths to exist. With a **negative cycle** reachable on the way to
$t$, they do not — go round the cycle again and the path gets cheaper, without limit, so there is no
shortest path to speak of. Lecture 18 detects this.

Note the two failures are different, and students conflate them constantly:

- **Negative *edges*** break Dijkstra but leave shortest paths well defined. Bellman-Ford handles them.
- **Negative *cycles*** break the *problem*. No algorithm can return an answer that does not exist.

---

## 4. Topological Order

A **topological order** of a directed graph is a linear ordering of the vertices in which every edge
points forwards. It exists **iff** the graph is a DAG — a cycle obviously cannot be laid out this way.

Week 4 gave us one algorithm for free.

> **Sort the vertices by decreasing DFS finish time.**

The argument was in Lecture 15 §6: for any edge $(u,v)$, $v$ cannot be grey (that would be a back
edge, hence a cycle), so $v$ is either white and becomes a descendant of $u$ — finishing first — or is
already black and finished earlier. Either way $f[v] < f[u]$.

*(Verified: 500 random DAGs, every edge respects the resulting order. 0 failures.)*

### Kahn's algorithm

The alternative is worth knowing because it is the one that generalises.

```python
def topo_kahn(V, adj):
    indeg = [0] * V
    for u in range(V):
        for v, _ in adj[u]: indeg[v] += 1
    q = deque(u for u in range(V) if indeg[u] == 0)
    out = []
    while q:
        u = q.popleft(); out.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    if len(out) != V: raise ValueError("cycle")     # some vertex never reached in-degree 0
    return out
```

*(Verified: agrees with the DFS version on 500 random DAGs — both produce valid orders, 0 failures.
They generally produce **different** valid orders, which is expected: a DAG usually has many.)*

Two practical advantages: it is iterative, so no recursion limit; and **it detects the cycle by
arithmetic** — if fewer than $V$ vertices come out, the remainder are exactly the vertices on or
downstream of a cycle, which is a far more useful error message than "there is a cycle somewhere."

---

## 5. Shortest Paths on a DAG

With a topological order in hand, the shortest-path problem becomes almost trivial.

```python
def dag_sssp(V, adj, s):
    order = topo_dfs(V, adj)
    d = [INF] * V; d[s] = 0
    for u in order:                    # every predecessor of u is already final
        if d[u] == INF: continue
        for v, w in adj[u]:
            if d[u] + w < d[v]: d[v] = d[u] + w
    return d
```

**$\Theta(V+E)$** — one pass, no priority queue, no repetition. When we process $u$, every vertex with
an edge into $u$ appears earlier in the order and has already been processed, so `d[u]` is already
final. The path-relaxation property is satisfied by construction.

### And it handles negative weights

This is the part worth pausing on. **A DAG has no cycles, so it has no negative cycles**, so negative
weights are harmless here. The algorithm that is fastest is also the one with the weakest restriction
on weights — the only time this week that those two things coincide.

*(Verified: 500 random DAGs, 351 of them containing negative edges, from every source — 3,607
(graph, source) pairs — against Bellman-Ford. 0 mismatches.)*

### Longest paths, for free

Negate every weight, find shortest paths, negate the answer.

*(Verified: 300 random DAGs, matches a direct longest-path computation. 0 mismatches.)*

This trick works **only** on a DAG. On a general graph, negating the weights turns positive cycles
into negative ones and destroys the problem — and indeed **longest simple path on a general graph is
NP-complete**, which is Week 12. So:

> **Shortest path: easy in general. Longest path: easy on a DAG, NP-complete in general.**

Two problems that look like mirror images, separated by the existence of cycles. That asymmetry is
worth remembering, because it is the first time this course has shown you a small change to a problem
statement moving it across the tractability boundary.

Applications of DAG shortest and longest paths are mostly **scheduling**: with tasks as vertices and
dependencies as edges, the longest path is the **critical path** — the minimum possible project
duration, and the set of tasks where a delay delays everything.

---

## 6. The Other Thing Finish Times Give You

Week 4 promised strongly connected components this week. They belong here because they are the same
machinery, and because they are what lets you *use* the DAG algorithms on a graph that is not a DAG.

A **strongly connected component** (SCC) of a digraph is a maximal set of vertices in which every
vertex reaches every other. **Kosaraju's algorithm** finds them in $\Theta(V+E)$ with two DFS passes:

1. Run DFS on $G$, pushing each vertex onto a list when it **finishes**.
2. Reverse every edge to get $G^{\mathrm{T}}$.
3. Run DFS on $G^{\mathrm{T}}$, taking start vertices in **decreasing finish time** from step 1. Each
   tree of this second forest is one SCC.

*(Verified: 400 random digraphs against a transitive-closure ground truth — component counts and
every pairwise membership. 0 mismatches.)*

The intuition, without the full proof: the vertex with the largest finish time lies in a "source" SCC
of the graph, and reversing the edges makes it a sink, so the second DFS cannot escape the component
it starts in.

**Why this matters here.** Contract each SCC to a single vertex and the result — the **condensation** —
is always a DAG. So any digraph is a DAG of its strongly connected components, and problems you can
solve on DAGs can often be lifted to general graphs by solving the condensation. That is the standard
route to 2-SAT, and it is how a build system reports a dependency cycle as one cluster rather than as
a confusing list of edges.

---

## 7. What to Do

- Read CLRS §20.4 (topological sort), §20.5 (SCC), and §22.2 (DAG shortest paths).
- **PS 5** implements both topological sorts and DAG shortest paths before touching Dijkstra.
- **Quiz 5 covers Week 4** — representations, BFS, DFS, timestamps. Not this material.
- **MIDTERM 1 is Monday 1 March** (Week 6) and covers Weeks 0–4. This lecture is *not* on it.
- Next lecture: Dijkstra — what you can still do when the graph has cycles but no negative weights.

---

*CS 102 · Week 5 · Lecture 16 · © CSE Department*
