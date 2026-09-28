# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 10: Graphs
### Released: Friday 4 December 2026, 14:00 (after the Friday lecture) | Due: Friday 11 December 2026, 17:00 (Week 11)

---

**Instructions:**
- Draw every graph you are asked to construct, and label the vertices.
- For any isomorphism claim, **exhibit the bijection**; for any non-isomorphism claim, **name the invariant**.
- Show all work. Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Terminology and the Handshake Theorem (36 points)

**A1.** *(10 pts)* A graph has 8 vertices, each of degree 3. How many edges does it have? Give an
example of such a graph.

**A2.** *(12 pts)* Two impossible degree sequences, for two different reasons.

- (a) Show $(1,1,2,3)$ is ruled out by the handshake corollary.
- (b) Show the corollary does **not** rule out $(1,2,3,4)$, then give the separate reason it is still
  impossible for a simple graph.

**A3.** *(14 pts)* Prove that in any simple graph with at least two vertices, some two vertices have
the same degree. *(Hint: the possible degrees are $0,\ldots,n-1$, but $0$ and $n-1$ cannot both
occur. Then apply Week 8.)*

---

## Part B — Representations (12 points)

**B1.** *(12 pts)* Write the adjacency matrix and the adjacency list for $C_5$ with vertices
$1,\ldots,5$ in cyclic order. State two properties the matrix must have because the graph is simple
and undirected.

---

## Part C — Isomorphism (14 points)

**C1.** *(14 pts)* Give two non-isomorphic graphs with the **same degree sequence** and the **same
number of components**. Prove they are not isomorphic.

---

## Part D — Connectivity, Euler, Hamilton (38 points)

**D1.** *(12 pts)* For which $n$ does $K_n$ have an Euler circuit? For which $m,n$ does $K_{m,n}$?
Justify both from the degree criterion.

**D2.** *(12 pts)* Find a Hamilton cycle in $K_{3,3}$ or prove none exists. Then explain why the same
question for a general graph has no comparable shortcut.

**D3.** *(14 pts)* Prove that a graph with a cut vertex has no Hamilton cycle.

---

## Grading

| Part | Topic | Points |
|---|---|---|
| A | Terminology and handshake | 36 |
| B | Representations | 12 |
| C | Isomorphism | 14 |
| D | Connectivity, Euler, Hamilton | 38 |
| **Total** | | **100** |
