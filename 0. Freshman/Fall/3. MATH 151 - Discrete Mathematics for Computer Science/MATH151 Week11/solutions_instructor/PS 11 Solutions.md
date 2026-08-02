# MATH 151 · Problem Set 11 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 100 points**, plus 8 bonus. All traces and values verified computationally.

$T$ denotes $V=\{a,\ldots,g\}$, $E=\{ab,ac,bd,be,cf,cg\}$.

---

## Part A — Tree Properties

### A1. *(6 pts)*
A tree on $n$ vertices has exactly $n-1$ edges, so **14 edges**. By the Handshake Theorem the degree
sum is $2\lvert E\rvert = \mathbf{28}$.

*Marking: 3 each, and both must cite the theorem rather than a drawing.*

---

### A2. *(6 pts)*
$n=10$, so there are 9 edges and the degree sum is 18. The 6 leaves contribute $6\times1=6$, leaving
$18-6=12$ across the 4 remaining vertices. Each therefore has degree $12/4 = \mathbf 3$.

*Marking: 2 degree sum, 2 leaf contribution, 2 division. The check that 3 is plausible (an internal
vertex must have degree $\ge2$) is worth mentioning in feedback.*

---

### A3. *(6 pts)*
There are exactly **three** non-isomorphic trees on 5 vertices, distinguished by degree sequence:

| Tree | Degree sequence |
|---|---|
| Path $P_5$ | $(1,1,2,2,2)$ |
| Star $K_{1,4}$ | $(1,1,1,1,4)$ |
| "Y" / spider | $(1,1,1,2,3)$ |

**Completeness argument:** any tree on 5 vertices has 4 edges and degree sum 8 across 5 vertices,
each of degree $\ge1$. The only partitions of 8 into 5 parts each $\ge1$ with maximum $\le4$ are
$(1,1,2,2,2)$, $(1,1,1,2,3)$, and $(1,1,1,1,4)$ — and each is realised by exactly one tree up to
isomorphism.

*Marking: 3 for the three trees, 3 for the completeness argument. Drawings alone earn 3 — the
question asks how they know the list is complete.*

---

### A4. *(8 pts)*
**Claim.** Every tree with $n\ge2$ vertices has at least two leaves.

**Proof.** The degree sum is $2(n-1) = 2n-2$. Every vertex has degree $\ge1$ (the tree is connected
and $n\ge2$). Suppose at most one vertex has degree 1. Then at least $n-1$ vertices have degree
$\ge2$, giving a degree sum of at least $1 + 2(n-1) = 2n-1 > 2n-2$ — a contradiction. ∎

**Exactly two leaves, for every $n$:** the **path** $P_n$. Its endpoints have degree 1 and every
interior vertex has degree 2.

*Marking: 5 for the counting proof, 3 for the path example. A proof by "remove a leaf repeatedly" is
circular unless the existence of one leaf is established first — deduct 2 if so.*

---

## Part B — Rooted and Binary Trees

### B1. *(6 pts)* $T$ rooted at $a$

| Vertex | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ |
|---|---|---|---|---|---|---|---|
| Depth | 0 | 1 | 1 | 2 | 2 | 2 | 2 |

**Height 2.** Leaves: $d, e, f, g$. Internal: $a, b, c$. *(Verified.)*

---

### B2. *(6 pts)* $T$ rooted at $d$

| Vertex | $d$ | $b$ | $a$ | $e$ | $c$ | $f$ | $g$ |
|---|---|---|---|---|---|---|---|
| Depth | 0 | 1 | 2 | 2 | 3 | 4 | 4 |

**Height 4.** *(Verified.)*

**Why it differs:** rooting is a *choice imposed on* the tree, not a property of it. The underlying
graph is unchanged; depth measures distance from the chosen root, and $d$ sits at the periphery while
$a$ sits centrally. The height-minimising root ($a$, height 2) is called a **centre** of the tree.

*Marking: 4 for the table, 2 for the explanation.*

---

### B3. *(5 pts)*

| Height $h$ | Max nodes $2^{h+1}-1$ | Min nodes $h+1$ |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 3 | 2 |
| 2 | 7 | 3 |
| 3 | 15 | 4 |

Maximum: every level full, level $i$ holding $2^i$ nodes, total $\sum_{i=0}^{h}2^i = 2^{h+1}-1$.
Minimum: a single chain, one node per level.

---

### B4. *(5 pts)*
$$h \ge \lceil\log_2(n+1)\rceil - 1$$

$n=1000$: $\lceil\log_2 1001\rceil - 1 = 10-1 = \mathbf 9$.
$n=10^6$: $\lceil\log_2(10^6{+}1)\rceil - 1 = 20-1 = \mathbf{19}$. *(Both verified.)*

**Relevance:** a binary search tree on $n$ items has height anywhere from $\lceil\log_2(n+1)\rceil-1$
to $n-1$. At $n=10^6$ that is the difference between **19** comparisons and **999,999**. AVL and
red–black trees exist solely to force the lower end; the bound proves the target is attainable.

*Marking: 2 values, 1 formula, 2 relevance.*

---

## Part C — Spanning Trees and MSTs

### C1. *(8 pts)* Kruskal — verified trace

Edges sorted by weight: $BC(1)$, $BD(2)$, $EF(2)$, $AC(3)$, $DF(3)$, $AB(4)$, $CD(4)$, $CE(5)$, $DE(7)$.

| Step | Edge | Weight | Decision | Reason |
|---|---|---|---|---|
| 1 | $BC$ | 1 | **accept** | $B$, $C$ in different components |
| 2 | $BD$ | 2 | **accept** | $D$ separate |
| 3 | $EF$ | 2 | **accept** | forms a second, disjoint component |
| 4 | $AC$ | 3 | **accept** | joins $A$ |
| 5 | $DF$ | 3 | **accept** | merges the two components — 5 edges, stop |

**Tree:** $\{BC, BD, EF, AC, DF\}$. **Total: $1+2+2+3+3 = 11$.**

*Note step 3: Kruskal maintains a **forest**, and the pieces merge only at step 5. Students who
reject $EF$ because "it isn't connected to the tree yet" have confused Kruskal with Prim — a common
and worth-flagging error.*

*Marking: 5 for the trace with reasons, 3 for the tree and total.*

---

### C2. *(8 pts)* Prim from $A$ — verified trace

| Step | Edge added | Weight | Tree vertices after |
|---|---|---|---|
| 1 | $AC$ | 3 | $A, C$ |
| 2 | $CB$ | 1 | $A, B, C$ |
| 3 | $BD$ | 2 | $A, B, C, D$ |
| 4 | $DF$ | 3 | $A, B, C, D, F$ |
| 5 | $FE$ | 2 | all six |

**Total: $3+1+2+3+2 = 11$** ✓

*Step 1 is the discriminator: from $A$ the choices are $AB(4)$ and $AC(3)$, so $AC$ wins. Students who
start with the globally cheapest edge $BC(1)$ are running Kruskal.*

---

### C3. *(4 pts)*

**Same total (11), same edge set** here: both produce $\{AC, BC, BD, DF, EF\}$ — though Kruskal adds
them in weight order and Prim in connectivity order.

**What determines uniqueness:** if all edge weights are **distinct**, the MST is unique. When weights
tie, several MSTs may exist — but **every MST has the same total weight**, since the total is the
optimum of a well-defined minimisation.

*Marking: 2 for comparing the edge sets, 2 for the uniqueness criterion. Students who assert the edge
sets must always differ have over-generalised.*

---

### C4. *(5 pts)*
**Cayley's formula:** $K_n$ has $n^{n-2}$ labelled spanning trees.

$$K_7:\ 7^5 = \mathbf{16{,}807} \qquad K_{10}:\ 10^8 = \mathbf{100{,}000{,}000}$$

*(Verified by exhaustive enumeration for $n \le 6$: 1, 3, 16, 125, 1296.)*

---

### C5. *(5 pts)*
Let $e$ be the **unique** heaviest edge of some cycle $C$, and suppose an MST $T$ contains it.

Removing $e$ splits $T$ into two components. The cycle $C$ crosses that split at some other edge $f
\ne e$, and since $e$ is the *unique* heaviest, $w(f) < w(e)$. Then $T - e + f$ is again a spanning
tree, of strictly smaller total weight — contradicting minimality. ∎

*Marking: 2 for the removal argument, 2 for producing $f$ from the cycle, 1 for the contradiction.
The word **unique** matters: with a tie, $w(f)=w(e)$ and the swap gives an equally good tree, so the
heaviest edge may appear in some MST.*

---

## Part D — Traversal

### D1. *(6 pts)* Verified orders, neighbours alphabetical

| Start | BFS | DFS |
|---|---|---|
| $a$ | $a, b, c, d, e, f, g$ | $a, b, d, e, c, f, g$ |
| $b$ | $b, a, d, e, c, f, g$ | $b, a, c, f, g, d, e$ |

*Marking: 1.5 each. Note DFS from $b$ visits $a$ first, then descends into $c$'s whole subtree before
returning for $d$ and $e$ — students often stop after $a$'s branch.*

---

### D2. *(5 pts)*
BFS uses a **queue**, so vertices leave in discovery order and a vertex at distance $k$ can only be
discovered from one at distance $k-1$. All of level $k-1$ is therefore processed before any of level
$k$, and the first time a vertex is reached is along a shortest path.

DFS uses a **stack** and commits to one branch entirely, so it may reach a vertex by a long detour
before ever considering the short route. Its first arrival carries no distance guarantee.

**With weights**, "fewest edges" and "least total weight" come apart, and BFS answers the wrong
question. **Dijkstra's algorithm** is required; BFS is exactly the special case where every weight
is 1.

*Marking: 2 BFS, 1 DFS, 2 weighted case.*

---

### D3. *(6 pts)*
**Two** topological orders exist:

$$a, b, c, d, e \qquad\text{and}\qquad a, c, b, d, e$$

*(Verified by exhaustive search.)*

**Why more than one:** $a$ must come first (in-degree 0) and $e$ last. Both $b$ and $c$ depend only
on $a$, and **neither depends on the other**, so no constraint orders them. A topological order is
unique precisely when the DAG has a Hamiltonian path — that is, when every consecutive pair is
directly constrained.

*Marking: 4 for both orders, 2 for the explanation. Students giving only one order earn 2.*

---

### D4. *(5 pts)*
Run BFS from any unvisited vertex, colouring the start 0 and each newly discovered vertex the
opposite colour to its discoverer. If an edge is ever found joining two vertices of the **same**
colour, the graph is not bipartite; if the traversal completes with no such edge, it is. Repeat for
each component.

**Running time $\Theta(n+m)$** — one pass, constant work per edge.

This works because the colour of a vertex is the parity of its BFS level, and a same-colour edge
closes a cycle of odd length.

*Marking: 3 for the method, 1 for the running time, 1 for the odd-cycle connection.*

---

## Bonus Solutions

### Bonus 1. *(4 pts)* The cut property

Let $(S, V\setminus S)$ be a partition with both parts non-empty, and let $e=(u,v)$ be a
minimum-weight edge crossing it. Suppose some MST $T$ omits $e$.

$T$ is spanning, so it contains a path from $u$ to $v$. That path starts in $S$ and ends outside, so
it crosses the partition at some edge $f$, and $w(f) \ge w(e)$ since $e$ is a minimum crossing edge.

Consider $T' = T - f + e$. Adding $e$ to $T$ creates exactly one cycle — the path plus $e$ — and $f$
lies on it, so removing $f$ leaves a spanning tree. Its weight is $w(T) - w(f) + w(e) \le w(T)$.

Since $T$ is minimum, $w(T') = w(T)$, so $T'$ is also an MST — and it contains $e$. ∎

*Marking: 1 setup, 2 exchange argument, 1 conclusion. Note the conclusion is "**some** MST", not
"every MST" — with ties, other MSTs may omit $e$.*

---

### Bonus 2. *(4 pts)* Cycle detection by DFS

**(⟸)** If DFS finds an edge $u\to v$ with $v$ currently on the recursion stack, then $v$ is an
ancestor of $u$ in the DFS tree, so a path $v \rightsquigarrow u$ exists; adding $u\to v$ closes a
cycle.

**(⟹)** If a cycle exists, consider the first of its vertices that DFS visits, say $v$. Every other
cycle vertex is reachable from $v$, so DFS explores them all before $v$ finishes — meaning $v$ is
still on the stack when the cycle's edge back into $v$ is examined.

**Why "already visited" is insufficient:** in a DAG such as $a\to b$, $a\to c$, $b\to d$, $c\to d$,
DFS reaches $d$ from $b$, finishes it, then examines $c\to d$ and finds $d$ already visited — with no
cycle present. The distinction is between a vertex that is *finished* (safe) and one that is *still
open on the stack* (a cycle). Implementations use three colours: white, grey, black.

*Marking: 1 per direction, 2 for the insufficiency example. The three-colour scheme earns full credit
on the last part.*

---

*MATH 151 · Week 11 · PS 11 Solutions · Instructor copy — do not distribute*
