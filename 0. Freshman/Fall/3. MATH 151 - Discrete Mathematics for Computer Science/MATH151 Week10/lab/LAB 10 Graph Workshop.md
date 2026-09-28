# MATH 151 · Discrete Mathematics for Computer Science
## Lab 10 — Graph Workshop: Representations, Invariants, Connectivity
### Wednesday 9 December 2026, 15:00–16:50 · Week 11 | Duration: 2 hours | Covers Week 10 (all three lectures)

---

**Bring:** laptop with Python 3. Work in pairs; both submit.

**No external libraries.** Everything here is built from lists and dictionaries — partly because it
is easy, and mostly because writing the representation yourself is what makes the cost trade-offs
concrete.

---

## Section 1 — By Hand (25 min)

Use $G$: $V=\{a,b,c,d,e\}$, $E=\{ab, ac, bc, bd, cd, de\}$ throughout.

### Exercise 1.1
Draw $G$. Write its degree sequence and verify the Handshake Theorem.

### Exercise 1.2
Write the adjacency matrix and the adjacency list.

### Exercise 1.3
Find all cut vertices and bridges by inspection. Justify each.

### Exercise 1.4
Does $G$ have an Euler circuit? An Euler trail? Justify from the degree criterion, not by searching.

---

## Section 2 — Building the Representations (30 min)

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

def matmul(X, Y):
    n = len(X)
    return [[sum(X[i][k]*Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
```

**2.1** *(3 pts)* Build both for $G$ and check them against your hand answers.

**2.2** *(4 pts)* Compute $A^2$ and $A^3$. Confirm:
- the diagonal of $A^2$ is the degree sequence;
- $(A^2)_{ad} = 2$, and name the two walks;
- $\operatorname{trace}(A^3)/6$ gives the triangle count. Verify by listing the triangles.

**2.3** *(3 pts)* Write `degree_sequence(adj)` and `is_handshake_ok(V, E)` returning whether
$\sum\deg = 2|E|$. Test on $G$, $K_5$, and $C_6$.

---

## Section 3 — Connectivity by Brute Force (35 min)

> *Revised 2026-09-21.* This section used to start from breadth-first search, which is taught in
> Week 11 (Lecture 35). It now uses only Lecture 32's definition of connectivity — a path between two
> vertices — and Week 7's product rule for the colouring search.

```python
def reachable(adj, start):
    """Every vertex joined to start by a path: keep adding neighbours until nothing new appears."""
    found = {start}
    changed = True
    while changed:
        changed = False
        for u in list(found):
            for v in adj[u]:
                if v not in found:
                    found.add(v)
                    changed = True
    return found
```

**3.1** *(5 pts)* Explain in two sentences why `reachable` returns exactly the vertices joined to
`start` by a path (Lecture 32's definition). Run it from every vertex of $G$. What does the output say
about whether $G$ is connected?

**3.2** *(4 pts)* Write `components(V, E)` counting connected components: take any vertex not yet
covered, remove everything `reachable` from it, and repeat. Test on $C_6$ (expect 1) and on two
disjoint triangles (expect 2).

**3.3** *(5 pts)* Write `cut_vertices(V, E)` by brute force: remove each vertex and count components.
Confirm your Exercise 1.3 answer.

**3.4** *(5 pts)* Write `is_bipartite(V, E)` by brute force: try every 2-colouring and check whether
some colouring gives every edge two different colours. To list the colourings, loop `k` over `range(2 **
len(V))` and give the vertex at position `i` in `V` the colour `(k // 2 ** i) % 2`, which is the `i`-th
binary digit of `k`. How many colourings does a graph with $n$ vertices need in the worst case? Test on
$C_4$, $C_5$, $C_6$, $K_{3,3}$, and $G$. State which are bipartite and relate the results to the
odd-cycle theorem.

---

## Section 4 — Invariants and Isomorphism (15 min)

**4.1** *(4 pts)* Write `invariants(V, E)` returning a tuple of: vertex count, edge count, sorted
degree sequence, component count, triangle count, and whether bipartite.

**4.2** *(4 pts)* Compare $C_6$ against two disjoint triangles. Which invariants agree? Which
separates them?

**4.3** *(4 pts)* Compare $K_{3,3}$ against $C_6$, and $C_6$ against $Q_3$. Report the first
distinguishing invariant in each case.

---

## Section 5 — Reflection (5 min)

1. Checking isomorphism directly means trying all $n!$ bijections; compute $20!$ in the REPL. What does that
   tell you about using invariants first?

2. You built the matrix and the list. For a graph with $10^6$ vertices and $5\times10^6$ edges, which
   would you use, and roughly how much memory would the other one need?

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: all four hand answers, with the Euler question justified by degrees
- [ ] 2.2: diagonal, walk count, and triangle count all confirmed
- [ ] 3.1–3.3: `reachable` explained, components correct on both tests, cut vertices matching Section 1
- [ ] 3.4: bipartite results for all five graphs, related to the odd-cycle theorem
- [ ] 4.2–4.3: distinguishing invariants identified in every pair
