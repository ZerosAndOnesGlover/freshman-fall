# MATH 151 — Discrete Mathematics for Computer Science
## Lecture 10.3 (L32) — Paths, Connectivity, Euler and Hamilton
### Friday, Week 10

---

## 1. Walks, Trails, Paths

Three words that students use interchangeably and the subject does not.

| Term | May repeat vertices? | May repeat edges? |
|---|---|---|
| **Walk** | yes | yes |
| **Trail** | yes | **no** |
| **Path** | **no** | no |

A **circuit** is a closed trail; a **cycle** is a closed path. The distinction matters this lecture,
because Euler is about **edges** (trails) and Hamilton is about **vertices** (paths).

**The length of a walk is its number of edges**, not vertices.

---

## 2. Connectivity

> **Definition.** $G$ is **connected** if there is a path between every pair of vertices. Otherwise
> it splits into **connected components**.

**Verified:** $C_6$ has **1** component; two disjoint triangles have **2** — the invariant that
separated them on Wednesday.

> **Definition.** A **cut vertex** is a vertex whose removal increases the number of components. A
> **bridge** is such an edge.

**Verified on the running example** $V=\{a,b,c,d,e\}$, $E=\{ab,ac,bc,bd,cd,de\}$: removing each
vertex in turn leaves 1 component — except **$d$**, whose removal disconnects $e$ from everything.
So $d$ is the unique cut vertex, and $de$ is a bridge.

**Cut vertices are single points of failure.** In a network they are exactly the routers whose loss
partitions the system, which is why redundancy is designed to eliminate them.

---

## 3. Euler Circuits — Every Edge Exactly Once

The subject begins with a real question. Königsberg had four land masses joined by seven bridges;
could one walk crossing each bridge exactly once?

> **Definition.** An **Euler trail** uses every edge exactly once. An **Euler circuit** is one that
> returns to its start.

> **Theorem (Euler, 1736).** A connected graph has
> - an **Euler circuit** ⟺ **every** vertex has even degree;
> - an **Euler trail** but no circuit ⟺ **exactly two** vertices have odd degree.

**Why even degree is necessary:** every visit to a vertex enters by one edge and leaves by another,
consuming two. If the trail starts and ends elsewhere, every vertex is entered and left equally
often, so all degrees are even. For an open trail the two endpoints are entered once more than they
are left — those two, and only those, are odd.

*That the condition is also **sufficient** is the substantial half, and it is what makes this a
theorem rather than an observation.*

### Königsberg

The four land masses have degrees $5, 3, 3, 3$ — **four** odd vertices. Since a trail permits at most
two, **no such walk exists**. *(Verified.)*

Euler's answer was not "I could not find one" but "none can exist" — and the argument depends on
nothing but the degree parity of Monday's handshake corollary.

### Where it is used

Route inspection — street sweeping, postal delivery, drone survey — where every *edge* must be
covered. When odd vertices exist, the Chinese Postman Problem asks which edges to repeat, and it is
solvable in polynomial time.

---

## 4. Hamilton Cycles — Every Vertex Exactly Once

> **Definition.** A **Hamilton path** visits every vertex exactly once; a **Hamilton cycle** returns
> to the start.

The definitions look parallel to Euler's. The difficulty is not.

> **There is no known efficient criterion for Hamiltonicity.** Deciding it is **NP-complete**.

**Verified contrast:**

| Graph | Vertices | Edges | Hamilton cycle? |
|---|---|---|---|
| $K_4$ | 4 | 6 | **Yes** — $0\to1\to2\to3\to0$ |
| Petersen | 10 | 15 | **No** — exhaustive search finds none |

The Petersen graph is 3-regular, connected, highly symmetric, and has no Hamilton cycle. Nothing
about its degree sequence reveals this; only search does.

**Sufficient conditions exist but are one-directional.** Dirac's theorem: if $n\ge3$ and every degree
is at least $n/2$, a Hamilton cycle exists. It does not apply to Petersen (degrees are 3, and
$n/2=5$), and its failure tells you nothing.

### The lesson worth carrying

| | Euler | Hamilton |
|---|---|---|
| Concerns | Edges | Vertices |
| Criterion | Degree parity | **None known** |
| Decidable in | Linear time | NP-complete |

**Two problems whose statements differ by one word — "edge" versus "vertex" — differ by the entire
gap between tractable and intractable.** This is the clearest example in the course of a theme you
met in Week 8's subset-sum: superficial similarity says nothing about difficulty.

The Travelling Salesman Problem is a weighted Hamilton cycle, which is why it is hard.

---

## 5. Shortest Paths, Briefly

In an **unweighted** graph, the shortest path is found by breadth-first search in $\Theta(n+m)$ —
Week 11's algorithm. With non-negative weights, Dijkstra's algorithm applies.

Note the asymmetry: shortest *path* is easy; longest path is NP-hard, because a longest path in a
complete graph is a Hamilton path.

---

## 6. Summary

| | |
|---|---|
| Walk / trail / path | repeats: both / edges no / neither |
| Connected | a path between every pair |
| Cut vertex | removal increases components — a single point of failure |
| **Euler circuit** | ⟺ connected and **all degrees even** |
| **Euler trail** | ⟺ connected and **exactly two odd** degrees |
| Königsberg | degrees $5,3,3,3$ — four odd, so impossible |
| **Hamilton** | no known criterion; **NP-complete** |
| Petersen | 3-regular, symmetric, **not** Hamiltonian |
| Dirac | $\deg \ge n/2$ ⟹ Hamiltonian (sufficient only) |

---

## 7. End-of-Lecture Exercises

1. For which $n$ does $K_n$ have an Euler circuit? *(Consider the degree of each vertex.)*

2. For which $m,n$ does $K_{m,n}$ have an Euler circuit?

3. The running example has degrees $2,3,3,3,1$. Does it have an Euler trail? An Euler circuit? Justify from the theorem.

4. Find a Hamilton cycle in $K_{3,3}$, or prove none exists.

5. Show that a graph with a cut vertex cannot have a Hamilton cycle. *(Hint: what must a cycle do at that vertex?)*

6. **(Stretch.)** Prove that if $G$ is connected with exactly two odd-degree vertices, any Euler trail must **begin and end** at those two vertices.

---

## Reading

- **Rosen, 8e §10.4–10.5** — Connectivity; Euler and Hamilton paths
- **Epp, 5e §10.2** — Trails, paths, and circuits
- **Levin, 3e §4.4** — Euler paths and circuits

*Next: Week 11 — Trees, Spanning Trees, and Graph Algorithms (BFS/DFS)*
