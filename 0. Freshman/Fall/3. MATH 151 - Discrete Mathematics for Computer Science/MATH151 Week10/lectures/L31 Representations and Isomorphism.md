# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 31 (L31) — Representations and Isomorphism
### Thursday, Week 10

**Date:** Thursday 3 December 2026 · 13:00–13:50 · Week 10

---

## 1. Storing a Graph

A graph is an abstract object; a program needs a concrete encoding. There are two standard ones, and
the choice between them is a genuine engineering decision.

### Adjacency matrix

An $n\times n$ matrix $A$ with $A_{ij}=1$ when $i$ and $j$ are adjacent, else $0$.

For the running example $V=\{a,b,c,d,e\}$, $E=\{ab,ac,bc,bd,cd,de\}$:

$$A=\begin{pmatrix}
0&1&1&0&0\\
1&0&1&1&0\\
1&1&0&1&0\\
0&1&1&0&1\\
0&0&0&1&0
\end{pmatrix}$$

For an undirected simple graph $A$ is **symmetric** with a **zero diagonal**, and the row sums are
the degrees — check: $2,3,3,3,1$ ✓

### Adjacency list

Each vertex stores its neighbours:

```
a: b, c
b: a, c, d
c: a, b, d
d: b, c, e
e: d
```

### Which to use

| | Adjacency matrix | Adjacency list |
|---|---|---|
| Space | $\Theta(n^2)$ | $\Theta(n+m)$ |
| "Is $uv$ an edge?" | $\Theta(1)$ | $\Theta(\deg u)$ |
| Iterate neighbours of $u$ | $\Theta(n)$ | $\Theta(\deg u)$ |
| Good for | **Dense** graphs | **Sparse** graphs |

**Almost every real graph is sparse**, so adjacency lists are the default. A social network with
$10^9$ users has average degree in the hundreds — the matrix would need $10^{18}$ entries, virtually
all zero. Week 11's traversals all assume adjacency lists, and that is where their $\Theta(n+m)$
running times come from.

---

## 2. Matrix Powers Count Walks

> **Theorem.** The $(i,j)$ entry of $A^k$ is the number of **walks** of length exactly $k$ from
> vertex $i$ to vertex $j$.

**Why:** $(A^2)_{ij}=\sum_k A_{ik}A_{kj}$ counts the intermediate vertices $k$ adjacent to both — that
is, the two-step routes. Induction extends it.

**Verified on the running example:**

$$A^2=\begin{pmatrix}
2&1&1&2&0\\
1&3&2&1&1\\
1&2&3&1&1\\
2&1&1&3&0\\
0&1&1&0&1
\end{pmatrix}$$

- $(A^2)_{ad}=2$: the walks $a\to b\to d$ and $a\to c\to d$ ✓
- $(A^2)_{ae}=0$: $e$'s only neighbour is $d$, and $a$ is not adjacent to $d$ ✓
- $(A^2)_{aa}=2 = \deg(a)$ — the diagonal of $A^2$ is always the degree

**A walk is not a path.** Walks may repeat vertices and edges; $(A^2)_{aa}=2$ counts $a\to b\to a$
and $a\to c\to a$.

### Counting triangles

The diagonal of $A^3$ counts closed walks of length 3, each of which is a triangle traversed from one
of 3 starting points in either of 2 directions:

$$\#\text{triangles} = \frac{\operatorname{trace}(A^3)}{6}$$

**Verified:** $\operatorname{trace}(A^3) = 2+4+4+2+0 = 12$, giving $12/6 = \mathbf{2}$ triangles — and
enumeration finds exactly $\{a,b,c\}$ and $\{b,c,d\}$ ✓

---

## 3. Isomorphism

The same graph can be drawn in unlimited ways. When are two graphs "the same"?

> **Definition.** $G_1=(V_1,E_1)$ and $G_2=(V_2,E_2)$ are **isomorphic** if there is a **bijection**
> $f:V_1\to V_2$ such that $uv\in E_1 \iff f(u)f(v)\in E_2$.

The bijection is Week 5's notion doing real work: a relabelling of vertices that preserves adjacency
exactly.

### Invariants — for proving graphs are *different*

A property preserved by isomorphism is an **invariant**. If two graphs differ on any invariant, they
are not isomorphic.

| Invariant |
|---|
| Number of vertices |
| Number of edges |
| Degree sequence |
| Number of connected components |
| Cycle lengths present |
| Bipartite or not |
| Number of triangles |

**Invariants can only prove graphs different, never the same.** Matching on every invariant you check
is evidence, not proof.

**Verified example.** $C_6$ and two disjoint triangles both have 6 vertices, 6 edges, and degree
sequence $(2,2,2,2,2,2)$ — identical on three invariants. But $C_6$ has **1** connected component and
the triangle pair has **2**, so they are not isomorphic. *(Confirmed by connectivity search.)*

### To prove graphs *are* isomorphic

Exhibit the bijection and check every edge. There is no shortcut.

---

## 4. The Difficulty of Isomorphism

Checking all bijections costs $n!$ — for $n=20$ that is $2.4\times10^{18}$.

**No polynomial-time algorithm for graph isomorphism is known**, yet the problem is not known to be
NP-complete either. It sits in an unusual middle ground; Babai's 2015 quasi-polynomial algorithm is
the best general result. In practice, tools like `nauty` refine by invariants and settle almost all
graphs quickly.

**Contrast with subgraph isomorphism** — "does $G_1$ appear inside $G_2$?" — which *is* NP-complete.
A small change in the question produces a large change in difficulty, which is worth noticing.

---

## 5. Summary

| | |
|---|---|
| Adjacency matrix | $\Theta(n^2)$ space, $\Theta(1)$ edge query |
| Adjacency list | $\Theta(n+m)$ space — the default, since real graphs are sparse |
| $A$ symmetric, zero diagonal | for undirected simple graphs; row sums are degrees |
| $(A^k)_{ij}$ | number of **walks** of length $k$ |
| $\operatorname{trace}(A^3)/6$ | number of triangles |
| Isomorphism | an adjacency-preserving **bijection** of vertices |
| Invariants | prove graphs **different**; never prove them the same |
| Same degree sequence | does not imply isomorphic — $C_6$ vs two triangles |

---

## 6. End-of-Lecture Exercises

1. Write the adjacency matrix and adjacency list for $C_4$ with vertices $1,2,3,4$ in order.

2. For the running example, compute $(A^2)_{be}$ by hand and name the walks it counts.

3. A graph has 100 vertices and 300 edges. How much space does each representation need, in rough terms? Which would you choose?

4. Show that $K_{3,3}$ and $C_6$ are not isomorphic, using an invariant.

5. Give two non-isomorphic graphs with the same degree sequence **and** the same number of components.

6. **(Stretch.)** Prove that isomorphism preserves the number of triangles, by showing $\operatorname{trace}(A^3)$ is unchanged when vertices are relabelled.

---

## Reading

- **Rosen, 8e §10.3** — Representing graphs and graph isomorphism
- **Epp, 5e §10.3** — Matrix representations
- **Levin, 3e §4.2** — Isomorphism

*Next: Lecture 32 — Paths, Connectivity, Euler and Hamilton*
