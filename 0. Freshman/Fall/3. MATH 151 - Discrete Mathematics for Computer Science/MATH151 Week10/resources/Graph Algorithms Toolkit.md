# MATH 151 · Graph Algorithms Toolkit
## Week 10: Working With Graphs in Python

---

No external libraries. Everything below is lists and dictionaries — which keeps the cost model
visible, and is the point.

---

## Building the Representations

```python
def to_matrix(V, E):
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    A = [[0]*n for _ in range(n)]
    for u, w in E:
        A[idx[u]][idx[w]] = 1
        A[idx[w]][idx[u]] = 1
    return A, idx

def to_list(V, E):
    adj = {v: [] for v in V}
    for u, w in E:
        adj[u].append(w)
        adj[w].append(u)
    return adj
```

**Running example** $V=\{a,b,c,d,e\}$, $E=\{ab,ac,bc,bd,cd,de\}$:

```
A = [[0,1,1,0,0],
     [1,0,1,1,0],
     [1,1,0,1,0],
     [0,1,1,0,1],
     [0,0,0,1,0]]

adj = {a: [b,c], b: [a,c,d], c: [a,b,d], d: [b,c,e], e: [d]}
```

---

## Matrix Multiplication and Walk Counting

```python
def matmul(X, Y):
    n = len(X)
    return [[sum(X[i][k]*Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def triangles(A):
    A3 = matmul(matmul(A, A), A)
    return sum(A3[i][i] for i in range(len(A))) // 6
```

**Verified outputs:**

```
A^2 = [[2,1,1,2,0],
       [1,3,2,1,1],
       [1,2,3,1,1],
       [2,1,1,3,0],
       [0,1,1,0,1]]

diag(A^2) = [2,3,3,3,1]   # the degree sequence
trace(A^3) = 12           # triangles = 12/6 = 2
```

---

## Traversal

```python
from collections import deque

def bfs(adj, start):
    seen, order, q = {start}, [], deque([start])
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return order

def dfs(adj, start):
    seen, order, stack = set(), [], [start]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(u)
        for v in reversed(adj[u]):
            if v not in seen:
                stack.append(v)
    return order
```

Both run in $\Theta(n+m)$ on an adjacency list. *Verified: `bfs(adj, 'a')` gives
`['a','b','c','d','e']`.*

**Traversal order depends on the neighbour ordering in the list** — it is not canonical, so never
treat a BFS order as a property of the graph.

---

## Connectivity, Components, Cut Vertices

```python
def components(V, E):
    adj = to_list(V, E)
    seen, count = set(), 0
    for s in V:
        if s in seen:
            continue
        count += 1
        seen.update(bfs(adj, s))
    return count

def cut_vertices(V, E):
    base = components(V, E)
    out = []
    for v in V:
        Vr = [x for x in V if x != v]
        Er = [e for e in E if v not in e]
        if Vr and components(Vr, Er) > base:
            out.append(v)
    return out
```

*Verified: `components` gives 1 for $C_6$ and 2 for two disjoint triangles;
`cut_vertices` on the running example returns `['d']`.*

---

## Bipartiteness

```python
def is_bipartite(V, E):
    adj = to_list(V, E)
    colour = {}
    for s in V:
        if s in colour:
            continue
        colour[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]
                    stack.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True
```

*Verified: `True` for $C_4$, $C_6$, $K_{3,3}$; `False` for $C_5$.*

---

## Euler and Hamilton

```python
def has_euler(V, E):
    adj = to_list(V, E)
    odd = sum(1 for v in V if len(adj[v]) % 2)
    if components(V, E) > 1:
        return "neither"
    return {0: "circuit", 2: "trail"}.get(odd, "neither")
```

**Linear time**, because it only counts degrees.

```python
from itertools import permutations

def hamilton_cycle(V, E):
    adj = to_list(V, E)
    s = V[0]
    for perm in permutations(V[1:]):
        p = (s,) + perm
        if all(p[i+1] in adj[p[i]] for i in range(len(p)-1)) and p[0] in adj[p[-1]]:
            return p
    return None
```

**Factorial time**, because nothing better is known.

*Verified: `hamilton_cycle` finds `(0,1,2,3)` in $K_4$ and returns `None` for the Petersen graph.*

**The two functions above are the whole Euler/Hamilton lesson in code.** One counts; the other
searches.

---

## Invariants for Isomorphism Testing

```python
def invariants(V, E):
    adj = to_list(V, E)
    A, _ = to_matrix(V, E)
    return (len(V),
            len(E),
            sorted(len(adj[v]) for v in V),
            components(V, E),
            triangles(A),
            is_bipartite(V, E))
```

**Different invariant tuples ⟹ not isomorphic. Equal tuples prove nothing.**

*Verified: $C_6$ gives `(6, 6, [2]*6, 1, 0, True)` and two triangles give `(6, 6, [2]*6, 2, 2, False)`
— separated by the component count, the triangle count, and bipartiteness.*

---

## Cost Summary

| Operation | Adjacency list |
|---|---|
| BFS / DFS | $\Theta(n+m)$ |
| Components | $\Theta(n+m)$ |
| Bipartite test | $\Theta(n+m)$ |
| Euler existence | $\Theta(n+m)$ |
| Cut vertices (brute force) | $\Theta(n(n+m))$ |
| Hamilton cycle (brute force) | $\Theta(n!)$ |
| Isomorphism (brute force) | $\Theta(n!\,m)$ |

$20! \approx 2.4\times10^{18}$ — which is why the last two rows are unusable beyond about $n=11$.

---

*MATH 151 · Week 10 · Reference · © CSE Department*
