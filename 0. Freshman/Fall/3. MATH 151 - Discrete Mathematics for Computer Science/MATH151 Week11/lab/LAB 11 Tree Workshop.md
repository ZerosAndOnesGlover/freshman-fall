# MATH 151 · Discrete Mathematics for Computer Science
## Lab 11 — Tree Workshop: Spanning Trees, MSTs, and Traversal
### Wednesday 16 December 2026, 15:00–16:50 · Week 12 | Duration: 2 hours | Covers Week 11 (all three lectures)

---

**Bring:** laptop with Python 3. Work in pairs; both submit. No external libraries.

**Theme:** Week 10 ended on problems no algorithm solves efficiently. This week everything is fast,
and the lab makes that concrete — you will implement four algorithms and every one of them runs in
near-linear time.

---

## Section 1 — By Hand (25 min)

### Exercise 1.1
For $T$: $V=\{a,\ldots,g\}$, $E=\{ab,ac,bd,be,cf,cg\}$ — verify it is a tree using **two** different
characterisations from Lecture 33.

### Exercise 1.2
Root $T$ at $a$. Tabulate depths, state the height, list leaves and internal vertices.
Then root it at $d$ and do the same. Explain the difference in one sentence.

### Exercise 1.3
Using the weighted graph below, run **Kruskal by hand**. Show every edge considered with its
accept/reject decision.

| Edge | $AB$ | $AC$ | $BC$ | $BD$ | $CD$ | $CE$ | $DE$ | $DF$ | $EF$ |
|---|---|---|---|---|---|---|---|---|---|
| Weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 3 | 2 |

### Exercise 1.4
Run **Prim by hand from $A$** on the same graph. Confirm the total matches Exercise 1.3.

---

## Section 2 — Tree Checking and Structure (25 min)

**2.1** *(4 pts)* Write `is_tree(V, E)` using the "connected and $n-1$ edges" characterisation. Test
it on $T$, on $T$ plus the edge $dg$, and on $T$ minus the edge $cg$. Explain each result.

**2.2** *(4 pts)* Write `leaves(adj)` and `internal(adj)`. Confirm $T$ has four leaves.

**2.3** *(5 pts)* Write `depths(adj, root)` returning a dictionary of depths, and `height(adj, root)`.
Run for **every** choice of root in $T$ and tabulate the heights. Which root minimises the height?

*(The minimising root is called a **centre** of the tree — worth knowing the name.)*

---

## Section 3 — Spanning Trees and MSTs (35 min)

**3.1** *(6 pts)* Implement Kruskal's algorithm with union–find:

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

Run it on the Section 1 graph. Confirm the total is **11** and that the tree has $n-1$ edges.

**3.2** *(6 pts)* Implement Prim's algorithm with a heap. Run it from **every** starting vertex and
tabulate the resulting edge sets and totals.

**Do all six runs give the same total? Do they give the same edge set?** Answer both explicitly.

**3.3** *(5 pts)* Modify the graph so two edges tie for a critical weight, and exhibit **two distinct
MSTs** with equal total. Then make all weights distinct and argue the MST is now unique.

**3.4** *(4 pts)* Verify Cayley's formula computationally for $n=4$ and $n=5$: enumerate all subsets
of $\binom n2$ edges of size $n-1$, count how many are trees, and compare with $n^{n-2}$.

*(Expect 16 and 125.)* Then compute — **do not run** — how many subsets the same brute force would test at $n=7$, $n=9$, and $n=11$, using $\binom{\binom n2}{n-1}$. State the largest $n$ you would be willing to run, and why.

---

## Section 4 — Traversal (25 min)

**4.1** *(5 pts)* Implement `bfs(adj, start)` and `dfs(adj, start)`. Run both on $T$ from $a$ and
from $b$. Tabulate all four orders.

**4.2** *(5 pts)* Write `bfs_distances(adj, start)` returning the distance to every vertex. Verify
against the depths from 2.3 and explain why they agree for a tree.

**4.3** *(6 pts)* Implement Kahn's topological sort:

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

Test on $a\to b$, $a\to c$, $b\to d$, $c\to d$, $d\to e$ (expect a valid order) and on
$a\to b\to c\to a$ (expect `None`). **Explain what `None` means to a build system.**

**4.4** *(4 pts)* Write `is_bipartite(adj)` using a single BFS with 2-colouring. Test on $C_4$, $C_5$,
and $T$. Why is every tree bipartite?

---

## Section 5 — Reflection (10 min)

1. Section 3.2 ran Prim from six different starts. What varied, what did not, and what does that tell
   you about MSTs?

2. Every algorithm in this lab runs in near-linear time, while Week 10's Hamilton search was
   factorial. What structural property of trees is responsible?

3. In 4.3, `toposort` returned `None` on the cyclic graph. Explain why this is not a failure of the
   algorithm.

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: all four hand exercises, with Kruskal and Prim both totalling 11
- [ ] 2.1: all three test cases explained
- [ ] 2.3: height table for all seven roots, minimising root identified
- [ ] 3.1: Kruskal returning total 11 with 5 edges
- [ ] 3.2: all six Prim runs tabulated, both questions answered explicitly
- [ ] 3.3: two distinct MSTs exhibited with equal totals
- [ ] 3.4: Cayley verified for $n=4,5$, with the $n=7$ infeasibility explained
- [ ] 4.1–4.4: all four traversal functions working, `None` case explained
