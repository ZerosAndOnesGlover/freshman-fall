# MATH 151 · Problem Set 10 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 100 points**, plus 8 bonus. All computations verified.

Throughout, $G$ denotes $V=\{a,b,c,d,e\}$, $E=\{ab,ac,bc,bd,cd,de\}$.

---

## Part A — Terminology and Handshake

### A1. *(6 pts)*
$$\lvert E\rvert=\frac{8\times3}{2}=\mathbf{12}$$

Such a graph exists — **$Q_3$, the cube**: 8 vertices, each of degree 3, 12 edges. *(Verified.)*

*Marking: 3 for the count, 3 for a valid example. Accept any 3-regular graph on 8 vertices.*

---

### A2. *(6 pts)*

**(a)** $(1,1,2,3)$ has odd degrees $1, 1, 3$ — **three** of them. The corollary requires an even
number, so no graph has this degree sequence. *(Sum is $7$, also odd, which is the same objection.)*

**(b)** $(1,2,3,4)$ has odd degrees $1$ and $3$ — **two**, which is even, so the corollary is
satisfied and rules nothing out. The sum is $10$, giving 5 edges.

The separate obstruction: the sequence has 4 vertices, so in a **simple** graph the maximum possible
degree is $n-1=3$. A vertex of degree 4 would need a loop or a repeated edge. **Impossible.**

*Marking: 3 each. The point of the pair is that **two independent checks** are needed — parity and
maximum degree. Students who apply only one will accept an impossible sequence sooner or later.*

---

### A3. *(6 pts, 1.5 each)*

| | Edges |
|---|---|
| $K_{10}$ | $\binom{10}2 = \mathbf{45}$ |
| $K_{4,7}$ | $4\times7 = \mathbf{28}$ |
| $C_9$ | $\mathbf 9$ |
| $Q_4$ | $4\cdot2^3 = \mathbf{32}$ |

---

### A4. *(6 pts)* Two vertices share a degree

In a simple graph on $n\ge2$ vertices, each degree lies in $\{0,1,\ldots,n-1\}$ — $n$ possible values
for $n$ vertices, so pigeonhole does not immediately apply.

**But $0$ and $n-1$ cannot both occur:** a vertex of degree $0$ is joined to nothing, while a vertex
of degree $n-1$ is joined to everything including that vertex — a contradiction.

So the degrees actually lie in a set of size at most $n-1$. Now $n$ vertices (pigeons) into at most
$n-1$ degree values (pigeonholes) forces two vertices to share a degree. ∎

*Marking: 2 for the range, 3 for the mutual-exclusion argument, 1 for the pigeonhole conclusion. The
exclusion step is the whole problem — without it there is no pigeonhole.*

---

## Part B — Representations

### B1. *(6 pts)* $C_5$

$$A=\begin{pmatrix}0&1&0&0&1\\1&0&1&0&0\\0&1&0&1&0\\0&0&1&0&1\\1&0&0&1&0\end{pmatrix}
\qquad
\begin{aligned}
1&: 2, 5\\ 2&: 1, 3\\ 3&: 2, 4\\ 4&: 3, 5\\ 5&: 1, 4
\end{aligned}$$

**Two required properties:** $A$ is **symmetric** (edges are unordered) and has a **zero diagonal**
(no loops in a simple graph).

*Marking: 2 matrix, 2 list, 2 properties.*

---

### B2. *(8 pts)*

**(a)**
$$A=\begin{pmatrix}0&1&1&0&0\\1&0&1&1&0\\1&1&0&1&0\\0&1&1&0&1\\0&0&0&1&0\end{pmatrix}
\qquad
A^2=\begin{pmatrix}2&1&1&2&0\\1&3&2&1&1\\1&2&3&1&1\\2&1&1&3&0\\0&1&1&0&1\end{pmatrix}$$

**(b)** $(A^2)_{ad}=2$ counts **walks of length 2** from $a$ to $d$: namely $a\to b\to d$ and
$a\to c\to d$.

**(c)** $(A^2)_{vv}=\sum_k A_{vk}A_{kv}=\sum_k A_{vk}^2=\sum_k A_{vk}=\deg(v)$, since entries are
$0$ or $1$. Combinatorially: a closed 2-walk from $v$ goes out along an edge and back along the same
one, so there is exactly one per incident edge.

**(d)** $\operatorname{trace}(A^3)=2+4+4+2+0=12$, so triangles $=12/6=\mathbf 2$ — namely
$\{a,b,c\}$ and $\{b,c,d\}$, confirmed by inspection. The $6$ is $3$ starting vertices $\times$ $2$
directions.

*Marking: 2/2/2/2. (c) may be answered algebraically or combinatorially.*

---

### B3. *(8 pts)*

**(a)** $100^2 = \mathbf{10{,}000}$ entries, of which $2\times300 = \mathbf{600}$ are non-zero — **6%
occupancy**.

**(b)** About $n + 2m = 100 + 600 = \mathbf{700}$ stored items.

**(c)** **Adjacency list**, roughly 14× smaller here and far better as the graph grows. The matrix
would be faster for the single operation "is $uv$ an edge?", which is $\Theta(1)$ against
$\Theta(\deg u)$.

*Marking: 3/2/3. Full marks on (c) require naming the operation where the matrix wins — the question
asks for the trade-off, not a verdict.*

---

## Part C — Isomorphism

### C1. *(6 pts)* $K_{3,3}$ vs $C_6$

Both have 6 vertices. But $K_{3,3}$ has $3\times3=\mathbf 9$ edges and $C_6$ has $\mathbf 6$.
**Edge count is an invariant**, so they are not isomorphic. ∎

*(Degree sequences also differ: $(3,3,3,3,3,3)$ against $(2,2,2,2,2,2)$ — either invariant suffices.)*

---

### C2. *(6 pts)* Same degree sequence and same component count

Take $K_{3,3}$ and the triangular prism $C_3\times K_2$. Both have 6 vertices, 9 edges, degree
sequence $(3,3,3,3,3,3)$, and **1** component.

They are **not** isomorphic: the prism contains triangles (two of them), while $K_{3,3}$ is bipartite
and so contains none. **Triangle count separates them.**

*Marking: 3 for a valid pair, 3 for the distinguishing invariant with justification. $C_6$ vs two
triangles does **not** answer this question — the component counts differ, and the question requires
them equal. Expect this error and deduct 3.*

---

### C3. *(6 pts)*

Five invariants: vertex count, edge count, degree sequence, number of connected components,
bipartiteness. *(Also acceptable: triangle count, cycle lengths present, complement's degree
sequence.)*

**Why matching does not prove isomorphism:** each invariant is a *necessary* condition, obtained by
projecting the graph onto a single number or list. Agreement means the two graphs are
indistinguishable *by those measurements* — but a finite list of measurements cannot capture the full
adjacency structure. Isomorphism requires a bijection on vertices that preserves **every** edge, and
only exhibiting one establishes that.

*Formally: invariants define an equivalence coarser than isomorphism.*

*Marking: 2 for the list, 4 for the explanation. "Because you might be unlucky" earns 1.*

---

### C4. *(6 pts)*

$G_1$ has edges $12,23,34,45,56,61$ — a single 6-cycle. $G_2$ has $12,23,31$ and $45,56,64$ — **two
disjoint triangles**.

Both have 6 vertices, 6 edges, and degree sequence $(2,2,2,2,2,2)$. But $G_1$ has **1** connected
component and $G_2$ has **2**. *(Verified by component count.)*

**Not isomorphic**, by the component-count invariant.

*Marking: 2 for identifying the structures, 2 for noting the shared invariants, 2 for the separating
one.*

---

## Part D — Connectivity, Euler, Hamilton

### D1. *(6 pts)*

Removing each vertex of $G$ in turn and recounting components *(verified)*:

| Removed | Components | Cut vertex? |
|---|---|---|
| $a$ | 1 | no |
| $b$ | 1 | no |
| $c$ | 1 | no |
| **$d$** | **2** | **yes** |
| $e$ | 1 | no |

**$d$ is the only cut vertex**: removing it isolates $e$, whose sole neighbour is $d$.

**$de$ is the only bridge**, for the same reason. Every other edge lies on a cycle
($abc$, $bcd$), and an edge on a cycle is never a bridge.

*Marking: 3 cut vertices, 3 bridges. The justification "$e$ is pendant, so its edge must be a bridge"
is worth full marks.*

---

### D2. *(6 pts)*

**$K_n$:** every vertex has degree $n-1$, which is even iff $n$ is **odd**. So $K_n$ has an Euler
circuit exactly when $n$ is odd (and $n\ge3$). *Verified: $K_3, K_5, K_7$ yes; $K_4, K_6$ no.*

**$K_{m,n}$:** the $m$ vertices on one side have degree $n$, the $n$ on the other have degree $m$. All
degrees are even iff **$m$ and $n$ are both even**. *Verified: $K_{2,2}$ and $K_{4,2}$ yes;
$K_{2,3}$ and $K_{3,3}$ no.*

*Marking: 3 each; the justification must come from degrees, not from drawing.*

---

### D3. *(6 pts)*

Degrees are $5,3,3,3$ — **four odd-degree vertices**. Euler's theorem permits an Euler trail only
when there are exactly $0$ or $2$; with four, **no trail exists**, and certainly no circuit.

**Minimum change:** adding one bridge between two of the odd-degree land masses makes both even,
leaving exactly two odd vertices — enough for an Euler **trail** (starting and ending at those two).
To get a **circuit** you would need to fix all four, requiring two added bridges.

*Marking: 3 for the impossibility argument, 3 for the modification. Answers proposing to *remove* a
bridge also work if the parity argument is correct.*

---

### D4. *(6 pts)*

**$K_{3,3}$ has a Hamilton cycle**, for instance

$$1 \to 4 \to 2 \to 5 \to 3 \to 6 \to 1$$

alternating between the two sides. *(Verified by search.)*

This works because the parts have **equal size**: a Hamilton cycle in a bipartite graph must
alternate sides, so it needs $\lvert X\rvert=\lvert Y\rvert$. *(Hence $K_{2,3}$ has none.)*

**Why no general shortcut:** Hamiltonicity is **NP-complete**. Unlike Euler's degree criterion, no
efficient test is known, and none is expected. Sufficient conditions such as Dirac's ($\deg\ge n/2$)
exist but are one-directional — the Petersen graph fails Dirac and is also non-Hamiltonian, while
other graphs fail Dirac and are Hamiltonian, so failure is uninformative.

*Marking: 3 for the cycle, 3 for the explanation.*

---

### D5. *(6 pts)*

Let $v$ be a cut vertex, so $G-v$ has components $C_1, C_2, \ldots$ with $k\ge2$.

Suppose a Hamilton cycle $H$ exists. Deleting $v$ from $H$ leaves a **path** on the remaining
vertices — a path is connected. But those remaining vertices are exactly $V\setminus\{v\}$, which
$G-v$ splits into $k\ge2$ components with no edges between them.

Every edge of that path is an edge of $G-v$, so the path would connect vertices lying in different
components — impossible. Hence no Hamilton cycle exists. ∎

*Marking: 2 for setting up $G-v$, 3 for "deleting one vertex from a cycle leaves a path", 1 for the
contradiction. That middle step is the key insight.*

---

## Bonus Solutions

### Bonus 1. *(4 pts)*

Let $u,w$ be the two odd-degree vertices and suppose an Euler trail starts at $x\notin\{u,w\}$.

At any vertex that is neither the start nor the end, each visit uses two edges (one in, one out), so
its degree must be even. Since $u$ has odd degree and is not an endpoint under this assumption, the
trail must at some point arrive at $u$ and be unable to leave — but then $u$ is the end, contrary to
assumption.

Therefore the trail's endpoints are exactly the odd-degree vertices. ∎

*Marking: 2 for the parity-at-interior-vertices argument, 2 for the conclusion.*

---

### Bonus 2. *(4 pts)*

The Petersen graph: 10 vertices, 15 edges, 3-regular, connected, vertex-transitive. **Exhaustive
search over all Hamilton cycle candidates finds none** *(verified computationally)*.

The standard hand argument: any Hamilton cycle would have to use some number of spokes; a parity
analysis of the outer 5-cycle, inner pentagram, and spokes shows every case forces a shorter cycle to
close prematurely.

**Dirac's theorem does not apply:** it requires every degree $\ge n/2 = 5$, but Petersen is 3-regular.
Dirac is a **sufficient** condition, so its failure gives no information either way — the Petersen
graph simply lies outside its scope.

*Marking: 2 for establishing non-Hamiltonicity, 2 for the correct reading of Dirac. Students who say
"Dirac fails, therefore not Hamiltonian" have inverted the logic — deduct 2.*

---

*MATH 151 · Week 10 · PS 10 Solutions · Instructor copy — do not distribute*
