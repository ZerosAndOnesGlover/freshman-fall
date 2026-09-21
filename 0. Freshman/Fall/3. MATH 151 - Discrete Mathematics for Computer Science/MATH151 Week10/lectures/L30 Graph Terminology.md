# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 30 (L30) — Graphs: Terminology and Basic Results
### Monday, Week 10

**Date:** Monday 30 November 2026 · 13:00–13:50 · Week 10

---

## 1. What a Graph Is

> **Definition.** A **graph** $G = (V, E)$ consists of a set $V$ of **vertices** and a set $E$ of
> **edges**, each edge being an unordered pair of vertices.

That is the whole definition, and its emptiness is the point. A graph carries **no geometry** — no
positions, no lengths, no angles. Two drawings that look nothing alike may be the same graph. All
that exists is *which vertices are joined*.

This abstraction is why graphs model so much: road networks, molecules, web links, task
dependencies, social ties, program control flow. Anything that is "things, and connections between
them" is a graph.

### The running example

$$V=\{a,b,c,d,e\},\qquad E=\{ab,\ ac,\ bc,\ bd,\ cd,\ de\}$$

Every claim in this lecture is checked against it.

---

## 2. Vocabulary

| Term | Meaning |
|---|---|
| **Adjacent** | Two vertices joined by an edge |
| **Incident** | An edge and one of its endpoints |
| **Degree** $\deg(v)$ | Number of edges at $v$ |
| **Isolated** | Degree 0 |
| **Pendant** | Degree 1 |
| **Simple** | No loops, no repeated edges |
| **Multigraph** | Repeated edges allowed |
| **Directed** (digraph) | Edges are ordered pairs; in-degree and out-degree |
| **Weighted** | Each edge carries a number |

In the running example, $\deg(a)=2$, $\deg(b)=\deg(c)=\deg(d)=3$, $\deg(e)=1$ — so $e$ is a
**pendant** vertex.

---

## 3. The Handshake Theorem

> **Theorem.** $\displaystyle\sum_{v\in V}\deg(v) = 2\lvert E\rvert$

**Proof.** Each edge has two endpoints, so it contributes exactly 2 to the total degree. Summing over
edges counts each contribution once. ∎

**Verified** on the running example: degrees $2+3+3+3+1 = 12$, and $2|E| = 2 \times 6 = 12$ ✓

> **Corollary.** The number of odd-degree vertices is **even**.

**Proof.** The total degree is even. The even-degree vertices contribute an even amount, so the
odd-degree vertices must contribute an even amount in total — which requires an even number of them. ∎

*Verified: the running example has odd-degree vertices $b, c, d, e$ — four of them.*

**This corollary is why nobody has ever attended a party where an odd number of people shook hands an
odd number of times.** It sounds like a triviality and is the basis of Friday's Euler-circuit
criterion.

---

## 4. Special Graphs

| Name | Notation | Vertices | Edges |
|---|---|---|---|
| Complete | $K_n$ | $n$ | $\binom n2 = \dfrac{n(n-1)}{2}$ |
| Cycle | $C_n$ | $n$ | $n$ |
| Path | $P_n$ | $n$ | $n-1$ |
| Complete bipartite | $K_{m,n}$ | $m+n$ | $mn$ |
| Hypercube | $Q_n$ | $2^n$ | $n\,2^{n-1}$ |

**Verified:** $K_5$ has 10 edges; $K_{3,4}$ has 12; $C_6$ has 6; $Q_3$ has **8 vertices and 12
edges**.

*$Q_3$ is the ordinary cube. Its vertices are the 3-bit strings, and two are joined when they differ
in exactly one bit — which is why hypercubes appear as network topologies: every neighbour is one bit
flip away.*

---

## 5. Bipartite Graphs

> **Definition.** $G$ is **bipartite** if $V$ splits into two sets with every edge running *between*
> them, never inside one.

Equivalently: $G$ can be 2-coloured so that adjacent vertices differ.

> **Theorem.** $G$ is bipartite **iff** it contains no cycle of odd length.

**Verified:** $C_6$ is bipartite; $C_5$ is not. Try to 2-colour a 5-cycle and the colours collide
when you return to the start — an odd cycle forces it.

**Where it matters:** matching problems (students to projects, jobs to machines), and any situation
with two distinct kinds of thing. Testing bipartiteness is a two-colouring pass during a breadth-first
search — Week 11's algorithm.

---

## 6. Subgraphs, Complements, and Degree Sequences

- A **subgraph** uses a subset of the vertices and a subset of the edges among them.
- The **complement** $\overline G$ has the same vertices, with exactly the edges $G$ lacks.
- The **degree sequence** is the list of degrees, sorted.

The running example's degree sequence is $(1,2,3,3,3)$.

> **Warning, and it is the important one.** The degree sequence does **not** determine the graph.

**Verified counterexample:** $C_6$ (a single 6-cycle) and two disjoint triangles both have degree
sequence $(2,2,2,2,2,2)$ — yet $C_6$ is connected and the pair of triangles is not. **Same numbers,
different graphs.**

This is the first hint that deciding whether two graphs are "the same" is subtle, which is
Thursday's subject.

---

## 7. Graphs in Computer Science

| Structure | Vertices | Edges |
|---|---|---|
| Road network | Junctions | Roads |
| The web | Pages | Hyperlinks |
| Social network | People | Friendships |
| Build system | Tasks | Dependencies |
| Compiler | Basic blocks | Control flow |
| Neural network | Neurons | Weighted connections |
| File system | Directories | Containment |
| Git history | Commits | Parent links |

**Git is a directed acyclic graph, and so is every dependency system.** Acyclicity is what makes a
build order exist, and the algorithm that finds one — topological sort — is Week 11.

---

## 8. Summary

| | |
|---|---|
| Graph | $(V,E)$ — connections only, no geometry |
| Handshake | $\sum\deg(v) = 2\lvert E\rvert$ |
| Corollary | The number of odd-degree vertices is even |
| $K_n$ | $\binom n2$ edges |
| $K_{m,n}$ | $mn$ edges |
| $Q_n$ | $2^n$ vertices, $n2^{n-1}$ edges |
| Bipartite | ⟺ no odd cycle |
| Degree sequence | Does **not** determine the graph |

---

## 9. End-of-Lecture Exercises

1. A graph has 8 vertices each of degree 3. How many edges? Does such a graph exist?

2. Two impossible degree sequences, for two different reasons. Show that $(1,1,2,3)$ is ruled out by the handshake corollary, and that $(1,2,3,4)$ is **not** — then find the separate reason $(1,2,3,4)$ is still impossible for a simple graph.

3. How many edges does $K_{10}$ have? $K_{4,7}$? $Q_4$?

4. Draw two non-isomorphic graphs with degree sequence $(2,2,2,2)$, or explain why none exist.

5. Show that $C_7$ is not bipartite by attempting a 2-colouring and identifying where it fails.

6. **(Stretch.)** Prove that in any simple graph with at least two vertices, some two vertices have the same degree. *(Hint: the possible degrees are $0$ through $n-1$, but $0$ and $n-1$ cannot both occur. Then apply Week 8.)*

---

## Reading

- **Rosen, 8e §10.1–10.2** — Graphs and graph terminology
- **Epp, 5e §10.1** — Graphs: definitions and basic properties
- **Levin, 3e §4.1** — Introduction to graph theory

*Next: Lecture 31 — Representations and Isomorphism*
