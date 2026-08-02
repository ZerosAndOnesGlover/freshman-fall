# MATH 151 · Traversal Algorithms Toolkit
## Week 11: Trees, MSTs, and Search

---

## Tree Checking

```python
def is_tree(V, E):
    return len(E) == len(V) - 1 and components(V, E) == 1
```

Both conditions are needed. $n-1$ edges alone permits a cycle plus an isolated vertex; connectivity
alone permits extra edges.

*Verified on $T = (\{a..g\},\ \{ab,ac,bd,be,cf,cg\})$:*

| Graph | Edges | Components | Tree? |
|---|---|---|---|
| $T$ | 6 | 1 | **yes** |
| $T + dg$ | 7 | 1 | no — too many edges (a cycle appeared) |
| $T - cg$ | 5 | 2 | no — disconnected |

---

## Depths and Height

```python
from collections import deque

def depths(adj, root):
    d = {root: 0}
    q = deque([root])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d

def height(adj, root):
    return max(depths(adj, root).values())
```

*Verified heights of $T$ by root:*

| Root | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ |
|---|---|---|---|---|---|---|---|
| Height | **2** | 3 | 3 | 4 | 4 | 4 | 4 |

---

## Kruskal with Union–Find

```python
def kruskal(V, W):
    parent = {v: v for v in V}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # path compression
            x = parent[x]
        return x
    tree, total = [], 0
    for u, v, w in sorted(W, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            tree.append((u, v, w))
            total += w
    return tree, total
```

**$\Theta(m\log m)$**, dominated by the sort. `find` with path compression is effectively constant.

*Verified output on the Week 11 graph:*
`[('B','C',1), ('B','D',2), ('E','F',2), ('A','C',3), ('D','F',3)]`, total **11**.

Note the third edge $EF$ joins a component disjoint from the rest — **Kruskal grows a forest.**

---

## Prim with a Heap

```python
import heapq

def prim(V, W, start):
    adj = {v: [] for v in V}
    for u, v, w in W:
        adj[u].append((w, v))
        adj[v].append((w, u))
    seen = {start}
    pq = [(w, start, v) for w, v in adj[start]]
    heapq.heapify(pq)
    tree, total = [], 0
    while pq and len(seen) < len(V):
        w, u, v = heapq.heappop(pq)
        if v in seen:
            continue
        seen.add(v)
        tree.append((u, v, w))
        total += w
        for w2, x in adj[v]:
            if x not in seen:
                heapq.heappush(pq, (w2, v, x))
    return tree, total
```

**$\Theta(m\log n)$.**

*Verified: from $A$ gives* `[('A','C',3), ('C','B',1), ('B','D',2), ('D','F',3), ('F','E',2)]`,
*total **11**; from $E$ also totals **11** with a different edge order.*

**Same total, different edge sequence** — the defining behaviour of MSTs with tied weights.

---

## BFS and DFS

```python
def bfs(adj, start):
    seen, order, q = {start}, [], deque([start])
    while q:
        u = q.popleft()                # FIFO
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    return order

def dfs(adj, start):
    seen, order, stack = set(), [], [start]
    while stack:
        u = stack.pop()                # LIFO
        if u in seen:
            continue
        seen.add(u); order.append(u)
        for v in reversed(adj[u]):
            if v not in seen:
                stack.append(v)
    return order
```

**The only difference is `popleft()` versus `pop()`.**

*Verified on $T$ with alphabetical neighbours:*

| Start | BFS | DFS |
|---|---|---|
| $a$ | $a,b,c,d,e,f,g$ | $a,b,d,e,c,f,g$ |
| $b$ | $b,a,d,e,c,f,g$ | $b,a,c,f,g,d,e$ |

---

## BFS Distances

```python
def bfs_distances(adj, start):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

Correct **only for unweighted graphs**. With weights, use Dijkstra — BFS is the all-weights-1 case.

For a tree, `bfs_distances(adj, r)` equals `depths(adj, r)`, because the unique path is the shortest
path.

---

## Topological Sort (Kahn)

```python
def toposort(D):
    indeg = {v: 0 for v in D}
    for u in D:
        for v in D[u]:
            indeg[v] += 1
    q = deque(sorted(v for v in D if indeg[v] == 0))
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in D[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out if len(out) == len(D) else None
```

*Verified: on $a\to b$, $a\to c$, $b\to d$, $c\to d$, $d\to e$ returns `['a','b','c','d','e']`
(and `['a','c','b','d','e']` is equally valid). On $a\to b\to c\to a$ returns `None`.*

**`None` means the graph has a cycle**, and therefore no valid order exists. This is a correct
report, not a failure.

---

## Bipartiteness by 2-Colouring

```python
def is_bipartite(adj):
    colour = {}
    for s in adj:
        if s in colour: continue
        colour[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]
                    q.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True
```

$\Theta(n+m)$. **Every tree is bipartite** — no cycles means no odd cycles.

---

## Cost Summary

| Operation | Cost |
|---|---|
| `is_tree` | $\Theta(n+m)$ |
| `depths` / `height` | $\Theta(n+m)$ |
| BFS / DFS | $\Theta(n+m)$ |
| `is_bipartite` | $\Theta(n+m)$ |
| `toposort` | $\Theta(n+m)$ |
| Kruskal | $\Theta(m\log m)$ |
| Prim | $\Theta(m\log n)$ |

**Every algorithm this week is near-linear.** Compare Week 10's Hamilton search at $\Theta(n!)$. The
difference is structural: trees and MSTs have properties (unique paths, the cut property) that let a
local choice be provably correct.

### Why brute force does not scale

Verifying Cayley's formula by enumerating $\binom{\binom n2}{n-1}$ edge subsets:

| $n$ | Subsets |
|---|---|
| 5 | 210 |
| 7 | 54 264 |
| 9 | 30 260 340 |
| 11 | 29 248 649 430 |

Feasible to about $n=8$; hopeless by $n=11$.

---

*MATH 151 · Week 11 · Reference · © CSE Department*
