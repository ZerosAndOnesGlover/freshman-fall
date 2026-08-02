# MATH 151 · Graph Terminology Reference
## Week 10: Graphs

---

## Core Definitions

$G=(V,E)$ — vertices and edges. **No geometry**: only which vertices are joined.

| Term | Meaning |
|---|---|
| Adjacent | Joined by an edge |
| Incident | An edge and its endpoint |
| $\deg(v)$ | Number of edges at $v$ |
| Isolated / pendant | Degree 0 / degree 1 |
| Simple | No loops, no repeated edges |
| Multigraph | Repeated edges allowed |
| Digraph | Ordered edges; in-degree and out-degree |
| Subgraph | Subset of vertices, subset of the edges among them |
| Complement $\overline G$ | Same vertices, exactly the missing edges |

---

## The Handshake Theorem

$$\sum_{v\in V}\deg(v)=2\lvert E\rvert$$

**Corollary: the number of odd-degree vertices is even.**

*Verified on $V=\{a,b,c,d,e\}$, $E=\{ab,ac,bc,bd,cd,de\}$: degrees $2,3,3,3,1$ sum to $12 = 2\times6$;
odd-degree vertices are $b,c,d,e$ — four of them.*

**Two ways a degree sequence can be impossible:**

| Sequence | Fails because |
|---|---|
| $(1,1,2,3)$ | Three odd degrees — violates the corollary |
| $(1,2,3,4)$ | Corollary is satisfied, but degree 4 needs 5 vertices |

Check **both** the parity and the maximum.

---

## Standard Families

| Family | Vertices | Edges | Notes |
|---|---|---|---|
| $K_n$ | $n$ | $\binom n2=\frac{n(n-1)}2$ | Every pair joined |
| $C_n$ | $n$ | $n$ | Cycle |
| $P_n$ | $n$ | $n-1$ | Path |
| $K_{m,n}$ | $m+n$ | $mn$ | Complete bipartite |
| $Q_n$ | $2^n$ | $n\,2^{n-1}$ | Hypercube |

**Verified:** $K_5$ → 10; $K_{10}$ → 45; $K_{3,4}$ → 12; $K_{4,7}$ → 28; $Q_3$ → 8 vertices, 12
edges; $Q_4$ → 16 vertices, 32 edges.

---

## Bipartite Graphs

> $G$ is bipartite **iff** it has no odd cycle.

Equivalently, $G$ is 2-colourable. *Verified: $C_6$ bipartite, $C_5$ not.*

Test by 2-colouring during a traversal — $\Theta(n+m)$.

---

## Representations

| | Adjacency matrix | Adjacency list |
|---|---|---|
| Space | $\Theta(n^2)$ | $\Theta(n+m)$ |
| Edge test | $\Theta(1)$ | $\Theta(\deg u)$ |
| Neighbours of $u$ | $\Theta(n)$ | $\Theta(\deg u)$ |
| Suits | Dense | **Sparse — the usual case** |

*For $n=100$, $m=300$: matrix has $10{,}000$ entries of which only $600$ are non-zero; the list needs
about $n+2m = 700$. For $n=10^6$, $m=5\times10^6$: the matrix would need $10^{12}$ entries.*

For a simple undirected graph, $A$ is **symmetric with zero diagonal**, and row sums are the degrees.

### Matrix powers

$(A^k)_{ij}$ = number of **walks** of length $k$ from $i$ to $j$.

- Diagonal of $A^2$ = degree sequence
- $\operatorname{trace}(A^3)/6$ = number of triangles

*Verified on the running example: $(A^2)_{ad}=2$ (walks $a\to b\to d$, $a\to c\to d$);
$\operatorname{trace}(A^3)=12$, giving 2 triangles — $\{a,b,c\}$ and $\{b,c,d\}$.*

**A walk is not a path.** Walks may repeat.

---

## Isomorphism

> A **bijection** $f:V_1\to V_2$ with $uv\in E_1 \iff f(u)f(v)\in E_2$.

**Invariants** (preserved by isomorphism): vertex count, edge count, degree sequence, component
count, bipartiteness, triangle count, cycle lengths present.

> **Invariants prove graphs different. They never prove them the same.**

*Standing counterexample: $C_6$ and two disjoint triangles agree on vertices (6), edges (6), and
degree sequence $(2,2,2,2,2,2)$ — but have 1 and 2 components respectively.*

To prove isomorphism, **exhibit the bijection**. Brute force costs $n!$; $20! \approx 2.4\times10^{18}$.

Graph isomorphism has no known polynomial algorithm and is not known to be NP-complete. **Subgraph**
isomorphism *is* NP-complete.

---

## Connectivity

| Term | Meaning |
|---|---|
| Connected | A path between every pair |
| Component | A maximal connected piece |
| Cut vertex | Removal increases the component count |
| Bridge | An edge whose removal increases it |

*Verified on the running example: $d$ is the only cut vertex, and $de$ is a bridge.*

**Cut vertices are single points of failure.**

---

## Euler and Hamilton — The Central Contrast

| | **Euler** | **Hamilton** |
|---|---|---|
| Covers | every **edge** once | every **vertex** once |
| Circuit criterion | connected, **all degrees even** | **none known** |
| Trail/path criterion | connected, **exactly two odd** degrees | none known |
| Decidable in | linear time | **NP-complete** |

**Königsberg:** degrees $5,3,3,3$ — four odd, so no Euler trail exists. Euler's 1736 argument is
pure degree parity.

**Verified contrast:** $K_4$ has a Hamilton cycle ($0\to1\to2\to3\to0$); the **Petersen graph** — 10
vertices, 15 edges, 3-regular, connected, vertex-transitive — has **none**, as exhaustive search
confirms.

**Dirac's theorem** (sufficient only): $n\ge3$ and every degree $\ge n/2$ ⟹ Hamiltonian. It says
nothing when it fails, and it fails for Petersen.

| Graph | Euler circuit? |
|---|---|
| $K_n$ | Iff $n$ is **odd** (degrees are $n-1$) |
| $K_{m,n}$ | Iff $m$ and $n$ are **both even** |
| $C_n$ | Always (all degrees 2) |

---

## Common Errors

| ❌ | ✅ |
|---|---|
| Same degree sequence ⟹ isomorphic | It does not — see $C_6$ vs two triangles |
| Checking parity only for a degree sequence | Also check $\max \deg \le n-1$ |
| Confusing walk and path | Walks repeat; paths do not |
| Euler = vertices | Euler is **edges**; Hamilton is vertices |
| Expecting a Hamilton criterion | There is none — it is NP-complete |
| Using a matrix for a sparse graph | $\Theta(n^2)$ when $\Theta(n+m)$ would do |

---

*MATH 151 · Week 10 · Reference · © CSE Department*
