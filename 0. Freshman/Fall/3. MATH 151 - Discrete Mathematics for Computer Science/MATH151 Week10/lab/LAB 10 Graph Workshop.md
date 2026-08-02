# MATH 151 · Discrete Mathematics for Computer Science
## Lab 10 — Graph Workshop: Representations, Invariants, Traversal
### Wednesday, Week 10 | Duration: 2 hours

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

## Section 3 — Traversal and Connectivity (35 min)

**3.1** *(5 pts)* Implement breadth-first search returning visit order:

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
```

Run from every vertex of $G$ and tabulate the orders. Explain why they differ.

**3.2** *(4 pts)* Write `components(V, E)` counting connected components. Test on $C_6$ (expect 1)
and on two disjoint triangles (expect 2).

**3.3** *(5 pts)* Write `cut_vertices(V, E)` by brute force: remove each vertex and count components.
Confirm your Exercise 1.3 answer.

**3.4** *(5 pts)* Write `is_bipartite(V, E)` by 2-colouring during a traversal. Test on $C_4$, $C_5$,
$C_6$, $K_{3,3}$, and $G$. State which are bipartite and relate the results to the odd-cycle theorem.

---

## Section 4 — Invariants and Isomorphism (25 min)

**4.1** *(4 pts)* Write `invariants(V, E)` returning a tuple of: vertex count, edge count, sorted
degree sequence, component count, triangle count, and whether bipartite.

**4.2** *(4 pts)* Compare $C_6$ against two disjoint triangles. Which invariants agree? Which
separates them?

**4.3** *(4 pts)* Compare $K_{3,3}$ against $C_6$, and $C_6$ against $Q_3$. Report the first
distinguishing invariant in each case.

**4.4** *(4 pts)* Write a brute-force `is_isomorphic(G1, G2)` trying all $n!$ bijections. Time it for
$n = 6, 7, 8$ and state the growth. **Why is this approach hopeless at $n = 20$?** Compute $20!$ to
support your answer.

---

## Section 5 — Euler and Hamilton (15 min)

**5.1** *(3 pts)* Write `has_euler(V, E)` returning `"circuit"`, `"trail"`, or `"neither"` from the
degree criterion. Test on $C_6$, $K_4$, $K_5$, and $G$.

**5.2** *(4 pts)* Write a brute-force Hamilton-cycle finder. Confirm $K_4$ has one and the **Petersen
graph does not**. Report how long each search took.

**5.3** *(3 pts)* Your two functions differ enormously in cost. Explain why in one paragraph,
referring to Lecture 10.3.

---

## Section 6 — Reflection (10 min)

1. In 4.4 you measured factorial growth directly. What does this tell you about invariant-based
   filtering as a practical strategy?

2. Euler is decidable by counting degrees; Hamilton needs search. Both questions look alike. What is
   the structural difference that makes one easy?

3. You built the matrix and the list. For a graph with $10^6$ vertices and $5\times10^6$ edges, which
   would you use, and roughly how much memory would the other one need?

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: all four hand answers, with the Euler question justified by degrees
- [ ] 2.2: diagonal, walk count, and triangle count all confirmed
- [ ] 3.1–3.3: BFS working, components correct on both tests, cut vertices matching Section 1
- [ ] 3.4: bipartite results for all five graphs, related to the odd-cycle theorem
- [ ] 4.2–4.3: distinguishing invariants identified in every pair
- [ ] 4.4: timing reported, $20!$ computed
- [ ] 5.2: Petersen confirmed non-Hamiltonian
