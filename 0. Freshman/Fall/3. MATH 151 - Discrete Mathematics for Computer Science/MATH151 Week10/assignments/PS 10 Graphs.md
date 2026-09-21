# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 10: Graphs
### Released: Friday 4 December 2026, 14:00 (after the Friday lecture) | Due: Friday 11 December 2026, 17:00 (Week 11)

---

> *Revised 2026-09-21.* The optional bonus section was removed to keep the set to 100 points of
> this week's material.

**Instructions:**
- Draw every graph you are asked to construct, and label the vertices.
- For any isomorphism claim, **exhibit the bijection**; for any non-isomorphism claim, **name the invariant**.
- Show all work. Submit as a single PDF.

**Scoring:** 100 points total.

---

## Part A — Terminology and the Handshake Theorem (24 points)

**A1.** *(6 pts)* A graph has 8 vertices, each of degree 3. How many edges does it have? Give an
example of such a graph.

**A2.** *(6 pts)* Two impossible degree sequences, for two different reasons.

- (a) Show $(1,1,2,3)$ is ruled out by the handshake corollary.
- (b) Show the corollary does **not** rule out $(1,2,3,4)$, then give the separate reason it is still
  impossible for a simple graph.

**A3.** *(6 pts)* Compute the number of edges in $K_{10}$, $K_{4,7}$, $C_9$, and $Q_4$.

**A4.** *(6 pts)* Prove that in any simple graph with at least two vertices, some two vertices have
the same degree. *(Hint: the possible degrees are $0,\ldots,n-1$, but $0$ and $n-1$ cannot both
occur. Then apply Week 8.)*

---

## Part B — Representations (22 points)

**B1.** *(6 pts)* Write the adjacency matrix and the adjacency list for $C_5$ with vertices
$1,\ldots,5$ in cyclic order. State two properties the matrix must have because the graph is simple
and undirected.

**B2.** *(8 pts)* For the graph $V=\{a,b,c,d,e\}$, $E=\{ab,ac,bc,bd,cd,de\}$:

- (a) Write $A$ and compute $A^2$.
- (b) State what $(A^2)_{ad}$ counts and list those walks explicitly.
- (c) Explain why the diagonal of $A^2$ is the degree sequence.
- (d) Compute the number of triangles using $\operatorname{trace}(A^3)/6$ and verify by inspection.

**B3.** *(8 pts)* A graph has 100 vertices and 300 edges.

- (a) How many entries does the adjacency matrix have? How many are non-zero?
- (b) How much space does the adjacency list need, in terms of $n$ and $m$?
- (c) Which representation would you choose, and for which operation would the other be faster?

---

## Part C — Isomorphism (24 points)

**C1.** *(6 pts)* Show $K_{3,3}$ and $C_6$ are not isomorphic. Name the invariant you use.

**C2.** *(6 pts)* Give two non-isomorphic graphs with the **same degree sequence** and the **same
number of components**. Prove they are not isomorphic.

**C3.** *(6 pts)* List five graph invariants. Explain precisely why matching on all five does not
prove two graphs isomorphic.

**C4.** *(6 pts)* Determine whether these are isomorphic, and either exhibit a bijection or name a
distinguishing invariant:

$$G_1: V=\{1..6\},\ E=\{12,23,34,45,56,61\} \qquad G_2: V=\{1..6\},\ E=\{12,23,31,45,56,64\}$$

---

## Part D — Connectivity, Euler, Hamilton (30 points)

**D1.** *(6 pts)* For the graph of B2, find all cut vertices and bridges. Justify each.

**D2.** *(6 pts)* For which $n$ does $K_n$ have an Euler circuit? For which $m,n$ does $K_{m,n}$?
Justify both from the degree criterion.

**D3.** *(6 pts)* The Königsberg bridges give degrees $5,3,3,3$. State precisely why no Euler trail
exists, and say what minimum change to the bridge layout would create one.

**D4.** *(6 pts)* Find a Hamilton cycle in $K_{3,3}$ or prove none exists. Then explain why the same
question for a general graph has no comparable shortcut.

**D5.** *(6 pts)* Prove that a graph with a cut vertex has no Hamilton cycle.

---

## Grading

| Part | Topic | Points |
|---|---|---|
| A | Terminology and handshake | 24 |
| B | Representations | 22 |
| C | Isomorphism | 24 |
| D | Connectivity, Euler, Hamilton | 30 |
| **Total** | | **100** |
