# MATH 151 · Discrete Mathematics for Computer Science
## Week 10 — Graphs: Terminology, Representations, Paths, Connectivity

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 10 of 12 |

---

### Week 10 Overview

A graph is the least structure that can still say something: a set of things, and a record of which
pairs are connected. No distances, no positions, no order. That poverty is exactly why graphs model
road networks, molecules, web links, build dependencies, social ties and control flow with the same
vocabulary.

Monday builds that vocabulary and proves the one theorem everything rests on — the **Handshake
Theorem**, that the degrees sum to twice the edge count. Its corollary, that odd-degree vertices come
in pairs, looks like a curiosity and turns out to settle a 300-year-old puzzle on Friday.

Wednesday is about **representation** and **sameness**. The adjacency matrix and adjacency list are
not interchangeable — the choice decides whether your algorithm is feasible on a graph with a million
vertices. And "are these two graphs the same?" turns out to be a genuinely hard question: invariants
can prove two graphs *different*, but nothing short of exhibiting a bijection proves them the same.

Friday sets **Euler** against **Hamilton**, and this is the week's real lesson. Euler asks for a walk
using every edge once, and is settled by counting degrees in linear time. Hamilton asks for a walk
visiting every vertex once, and is NP-complete. The statements differ by one word. **Superficial
similarity is no guide to difficulty** — the same lesson Week 8's subset-sum taught from the other
direction.

---

### Week 10 Contents

```
MATH151 Week10/
├── README.md
├── lectures/
│   ├── L30 Graph Terminology.md                     ← Lecture 31 (Monday)
│   ├── L31 Representations and Isomorphism.md       ← Lecture 32 (Wednesday)
│   └── L32 Paths Connectivity Euler Hamilton.md     ← Lecture 33 (Friday)
├── assignments/
│   └── PS 10 Graphs.md
├── lab/
│   └── LAB 10 Graph Workshop.md
├── quiz/
│   ├── QUIZ 10 Recurrences.md
│   └── QUIZ 11 Preview.md
├── resources/
│   ├── Graph Terminology Reference.md
│   └── Graph Algorithms Toolkit.md
└── solutions_instructor/
    ├── LAB 10 Solutions.md
    ├── PS 10 Solutions.md
    └── QUIZ 10 Solutions.md
```

---

### Learning Objectives

By the end of Week 10 you should be able to:

- Use graph vocabulary precisely, and distinguish walk, trail, path, circuit, and cycle
- State and prove the Handshake Theorem and its odd-degree corollary
- Compute edge counts for $K_n$, $C_n$, $K_{m,n}$, and $Q_n$
- Decide bipartiteness, and connect it to the absence of odd cycles
- Choose between adjacency matrix and adjacency list, and justify it by density
- Use $(A^k)_{ij}$ to count walks, and $\operatorname{trace}(A^3)/6$ to count triangles
- Prove two graphs non-isomorphic by exhibiting an invariant, and isomorphic by exhibiting a bijection
- Identify cut vertices and bridges, and explain their significance
- Apply Euler's criterion, and explain why Hamilton admits no analogue

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday | Quiz 10 (15 min) | Covers Week 9: recurrences and generating functions |
| Monday | Lecture 31 | Terminology; the Handshake Theorem; standard families; bipartiteness |
| Wednesday | Lecture 32 | Matrices and lists; walk counting; isomorphism and invariants |
| Wednesday | Lab 10 | Graph workshop: build both representations, traverse, test invariants |
| Friday | Lecture 33 | Paths, connectivity, cut vertices; Euler and Hamilton |
| Friday | PS 10 Released | Due Week 11 Friday |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §10.1–10.2 (Terminology), §10.3 (Representation, isomorphism), §10.4–10.5 (Connectivity, Euler, Hamilton) |
| Epp, 5e | §10.1 (Definitions), §10.2 (Trails and circuits), §10.3 (Matrix representations) |
| Levin, 3e | §4.1–4.2, §4.4 |

---

### Key Results

| | |
|---|---|
| Handshake | $\sum\deg(v)=2\lvert E\rvert$ |
| Corollary | The number of odd-degree vertices is even |
| $K_n$ / $K_{m,n}$ / $Q_n$ | $\binom n2$ / $mn$ / $n2^{n-1}$ edges |
| Bipartite | ⟺ no odd cycle |
| Matrix vs list | $\Theta(n^2)$ vs $\Theta(n+m)$ — real graphs are sparse |
| $(A^k)_{ij}$ | walks of length $k$ |
| $\operatorname{trace}(A^3)/6$ | triangles |
| Isomorphism | a bijection preserving adjacency |
| Invariants | prove difference, never sameness |
| Euler circuit | ⟺ connected, all degrees even |
| Euler trail | ⟺ connected, exactly two odd degrees |
| Königsberg | degrees $5,3,3,3$ ⟹ impossible |
| Hamilton | **NP-complete**; Petersen is a 3-regular non-Hamiltonian example |

---

### Graphs in Computer Science

| Structure | Vertices | Edges |
|---|---|---|
| Road network | Junctions | Roads |
| The web | Pages | Hyperlinks |
| Social network | People | Friendships |
| Build system | Tasks | Dependencies |
| Compiler | Basic blocks | Control flow |
| Git history | Commits | Parent links |
| File system | Directories | Containment |

**Git and every dependency system are directed acyclic graphs.** Acyclicity is precisely what
guarantees a valid build order exists — and finding one, topological sort, is next week.

---

### Connections

**Back:** Week 5's bijections are what isomorphism is built from. Week 8's pigeonhole proves the
stretch result that some two vertices always share a degree. Week 9's recurrences will analyse next
week's traversals.

**Forward:** Week 11 restricts attention to **trees** — connected acyclic graphs — where nearly every
hard question above becomes easy, and develops BFS and DFS properly.

**Sideways:** CS 101's hash tables, CS 102's algorithms course, and every network you will ever
debug are graphs. The Euler/Hamilton contrast is the same tractable-versus-intractable boundary that
CS 101 Week 11 approaches from computability.

---

*MATH 151 · Week 10 · © CSE Department*
