# MATH 151: Discrete Mathematics for Computer Science
## Week 11 — Trees, Spanning Trees, and Graph Algorithms

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 11 of 12 |

---

### Week 11 Overview

Week 10 ended on a discouraging note: isomorphism has no known efficient algorithm, and
Hamiltonicity is NP-complete. This week is the counterweight. **Every algorithm here runs in
near-linear time**, and the reason is a single structural restriction — no cycles.

Removing cycles removes choice. In a tree there is exactly one path between any two vertices, so
there is nothing to search for and nothing to optimise over. Monday develops that, along with the
five equivalent characterisations of a tree and the height bound that explains why balanced binary
search trees exist at all.

Wednesday asks a harder question: given a graph with weighted edges, find the cheapest subset that
keeps everything connected. **Kruskal and Prim both answer it greedily and both are correct** — which
is unusual, since greedy algorithms normally fail. The reason they work is the **cut property**, and
that property is exactly what the Travelling Salesman Problem lacks.

Friday covers BFS and DFS, which differ by one line — a queue instead of a stack — and by everything
in what they are good for. BFS gives shortest paths; DFS gives components, cycles, and topological
order. Every build system you will ever use runs the last of these, and "circular dependency
detected" is a topological sort correctly reporting that no valid order exists.

---

### Week 11 Contents

```
MATH151 Week11/
├── README.md
├── lectures/
│   ├── L33 Trees and Their Properties.md     ← Lecture 34 (Monday)
│   ├── L34 Spanning Trees.md                 ← Lecture 35 (Wednesday)
│   └── L35 BFS and DFS.md                    ← Lecture 36 (Friday)
├── assignments/
│   └── PS 11 Trees.md
├── lab/
│   └── LAB 11 Tree Workshop.md
├── quiz/
│   ├── QUIZ 11 Graphs.md
│   └── QUIZ 12 Preview.md
├── resources/
│   ├── Tree Properties Reference.md
│   └── Traversal Algorithms Toolkit.md
└── solutions_instructor/
    ├── LAB 11 Solutions.md
    ├── PS 11 Solutions.md
    └── QUIZ 11 Solutions.md
```

---

### Learning Objectives

By the end of Week 11 you should be able to:

- State the five equivalent characterisations of a tree and use the appropriate one
- Prove that a tree on $n$ vertices has $n-1$ edges, and that it has at least two leaves
- Compute depths and height for a rooted tree, and explain why they depend on the root
- Apply the binary-tree height bounds and connect them to balanced search trees
- State Cayley's formula and verify it for small $n$
- Execute Kruskal's and Prim's algorithms by hand, tabulating each step
- Explain the cut property and why greedy succeeds for MSTs but fails for TSP
- Implement BFS and DFS, and say which problems each solves
- Produce a topological order, and recognise what its absence means

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday | Quiz 11 (15 min) | Covers Week 10: graphs, isomorphism, Euler and Hamilton |
| Monday | Lecture 34 | Trees; equivalences; rooted and binary trees; height bounds |
| Wednesday | Lecture 35 | Spanning trees; Cayley; Kruskal and Prim; the cut property |
| Wednesday | Lab 11 | Tree workshop: implement all four algorithms |
| Friday | Lecture 36 | BFS, DFS, topological sort |
| Friday | PS 11 Released | Due Week 12 Friday |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §11.1 (Trees), §11.4 (Spanning trees, BFS/DFS), §11.5 (Minimum spanning trees) |
| Epp, 5e | §10.5 (Trees), §10.6 (Spanning trees, shortest paths) |
| Levin, 3e | §4.3 (Trees), §4.5 (Traversal) |

---

### Key Results

| | |
|---|---|
| Tree | Connected and acyclic; $n-1$ edges; unique paths |
| Every edge of a tree | Is a bridge |
| Leaves | At least 2 when $n\ge2$ |
| Height depends on the root | $T$ has height 2 from $a$, 4 from $d$ |
| Binary tree, height $h$ | At most $2^{h+1}-1$ nodes |
| Binary tree, $n$ nodes | Height $\ge \lceil\log_2(n+1)\rceil-1$; $n=10^6$ gives 19 |
| Cayley | $K_n$ has $n^{n-2}$ labelled spanning trees |
| Kruskal | $\Theta(m\log m)$; sorts and adds; grows a forest |
| Prim | $\Theta(m\log n)$; grows one tree |
| Both on the example | Total weight **11** |
| MST uniqueness | Guaranteed when all weights are distinct |
| Cut property | The cheapest crossing edge is in some MST |
| BFS vs DFS | Queue vs stack; both $\Theta(n+m)$ |
| BFS | Shortest paths in **unweighted** graphs |
| Topological order | Exists **iff** the digraph is acyclic |

---

### Trees in Computer Science

| Application | Structure |
|---|---|
| File system | Directory tree — the unique path is the absolute path |
| Binary search tree | $\Theta(\log n)$ search when balanced |
| Heap | Complete binary tree with an ordering invariant |
| Parse tree | Syntactic structure of source code |
| Huffman coding | Optimal prefix-free encoding |
| Spanning Tree Protocol | Loop-free Ethernet routing — a live MST |
| `make`, `cargo`, `npm` | Topological sort of a dependency DAG |
| Git | Commit DAG; trees as directory snapshots |

---

### Connections

**Back:** Week 10's graph vocabulary is the substrate — a tree is just a graph with a strong
restriction. Week 3's induction proves nearly every tree theorem, always by removing a leaf. Week 8's
pigeonhole underlies the "at least two leaves" argument.

**Forward:** Week 12 turns to number theory, closing the course. In CS 102, these algorithms are
implemented and analysed properly; Dijkstra generalises BFS to weighted graphs, and Huffman coding
builds an optimal tree greedily by the same kind of exchange argument as the cut property.

**Sideways:** CS 101's recursion and CS 102's data structures both rest on the height bound proved
here — it is the reason a balanced tree is worth the implementation effort.

---

*MATH 151 · Week 11 · © CSE Department*
