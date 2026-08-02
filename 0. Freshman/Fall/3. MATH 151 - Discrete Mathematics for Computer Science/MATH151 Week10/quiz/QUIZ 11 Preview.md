# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 11 — Scope Preview
### Quiz administered: Monday, Week 11 (first 15 minutes of lecture)

---

**Coverage:** Week 10 material — graph terminology, representations, isomorphism, connectivity,
Euler and Hamilton.

---

## What You Must Know Cold

### 1. The Handshake Theorem

$$\sum_{v\in V}\deg(v) = 2\lvert E\rvert$$

and its corollary: **the number of odd-degree vertices is even**. Both are one-line arguments and
both appear constantly.

### 2. Standard graph families

| Family | Vertices | Edges |
|---|---|---|
| $K_n$ | $n$ | $\binom n2$ |
| $C_n$ | $n$ | $n$ |
| $K_{m,n}$ | $m+n$ | $mn$ |
| $Q_n$ | $2^n$ | $n2^{n-1}$ |

### 3. Representations

Matrix: $\Theta(n^2)$ space, $\Theta(1)$ edge test. List: $\Theta(n+m)$ space, $\Theta(\deg u)$ edge
test. **Real graphs are sparse, so lists are the default.**

Know that $(A^k)_{ij}$ counts **walks** of length $k$, that the diagonal of $A^2$ is the degree
sequence, and that $\operatorname{trace}(A^3)/6$ counts triangles.

### 4. Isomorphism

A **bijection** on vertices preserving adjacency. **Invariants prove graphs different, never the
same.** Know at least five: vertex count, edge count, degree sequence, component count, bipartiteness,
triangle count.

Remember the standing counterexample: $C_6$ and two disjoint triangles share a degree sequence and
are not isomorphic.

### 5. Euler versus Hamilton — the most likely question

| | Euler | Hamilton |
|---|---|---|
| Covers | every **edge** once | every **vertex** once |
| Criterion | **all degrees even** (circuit); exactly two odd (trail) | **none known** |
| Cost | linear | NP-complete |

Königsberg has degrees $5,3,3,3$ — four odd, so no trail exists.

### 6. Connectivity

Connected, components, cut vertex, bridge. A cut vertex is a single point of failure — and a graph
with one cannot have a Hamilton cycle.

---

## Sample Quiz 11 Problems (Week 10 portion)

**Problem 1.** (4 pts) Can a graph have 7 vertices each of degree 3? Justify from the Handshake
Theorem. Then state how many edges a graph with 12 vertices each of degree 5 would have.

**Problem 2.** (4 pts) For which $n$ does $K_n$ have an Euler circuit? Justify from degrees.

**Problem 3.** (4 pts) Give two non-isomorphic graphs with degree sequence $(2,2,2,2,2,2)$ and name
the invariant that separates them.

**Problem 4.** (4 pts) A graph has 50 vertices and 100 edges. Compare the space needed by each
representation and say which you would choose.

**Problem 5.** (4 pts) Does $K_{2,3}$ have an Euler circuit? An Euler trail? Justify.

---

## Study Recommendations

1. **Compute degrees first, always.** Most Week 10 questions dissolve once the degree sequence is on the page.
2. **Memorise the four graph families' edge counts.** They appear in nearly every question.
3. **Drill the Euler criterion until it is automatic** — it is the one crisp decision procedure in the whole week.
4. **Never claim an isomorphism without the bijection**, and never claim non-isomorphism without naming the invariant.

---

*MATH 151 · Week 10 · © CSE Department*
