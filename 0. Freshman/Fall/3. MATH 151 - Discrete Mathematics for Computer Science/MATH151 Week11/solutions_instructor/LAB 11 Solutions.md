# MATH 151 · Week 11
## LAB 11 Solutions — INSTRUCTOR ONLY

*(Revised 2026-09-28: the lab listed 120 minutes. Exercises 3.2 (Prim from every start), 3.4 (Cayley enumeration) and 4.4
(bipartite BFS — Lab 10 already tests bipartiteness) and reflection Q1 are no longer asked; old 3.3 is 3.2.)*

All outputs produced by running the lab code. $T = (\{a..g\},\ \{ab,ac,bd,be,cf,cg\})$.

---

## Section 1 Solutions — By Hand

**1.1** Two characterisations:
- **Connected with $n-1$ edges:** 7 vertices, 6 edges, and a traversal reaches all 7 ✓
- **Unique path between every pair:** e.g. $d \to e$ has only $d\,b\,e$; there is no alternative ✓

*(Also acceptable: acyclic with $n-1$ edges, or every edge a bridge.)*

**1.2**

| Root | Depths | Height | Leaves | Internal |
|---|---|---|---|---|
| $a$ | $a$:0, $b$:1, $c$:1, $d$:2, $e$:2, $f$:2, $g$:2 | **2** | $d,e,f,g$ | $a,b,c$ |
| $d$ | $d$:0, $b$:1, $a$:2, $e$:2, $c$:3, $f$:4, $g$:4 | **4** | $e,f,g,a$? — see note | |

> **Note for the demonstrator.** Rooted at $d$, the leaves are the vertices with no children:
> $e, f, g$. Vertex $a$ has child $c$, so it is internal. Students who list $a$ as a leaf have
> carried over the unrooted notion (degree 1) instead of the rooted one (no children) — worth
> correcting on the spot, since it recurs.

**Explanation:** the graph is unchanged; depth measures distance from the chosen root, and $d$ is
peripheral while $a$ is central.

**1.3 / 1.4** Kruskal and Prim both total **11** — full traces in the PS 11 solutions.

---

## Section 2 Solutions

**2.1** *(4 pts)*

| Graph | Edges | Components | `is_tree` | Why |
|---|---|---|---|---|
| $T$ | 6 | 1 | **True** | $6 = 7-1$ and connected |
| $T + dg$ | 7 | 1 | **False** | $7 \ne 6$ — the extra edge created a cycle $d\,b\,a\,c\,g\,d$ |
| $T - cg$ | 5 | 2 | **False** | $g$ is isolated; connectivity fails |

*Both conditions are needed — this is why the exercise has three cases.*

**2.2** *(4 pts)* Leaves of $T$ (degree 1): $d, e, f, g$ — **four**. Internal: $a, b, c$.

**2.3** *(5 pts)* Verified heights by root:

| Root | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ |
|---|---|---|---|---|---|---|---|
| Height | **2** | 3 | 3 | 4 | 4 | 4 | 4 |

**Minimum height 2, at root $a$** — the unique centre of this tree.

*A tree has one or two centres, never more. Worth stating; students often expect many.*

---

## Section 3 Solutions

**3.1** *(6 pts)* Kruskal returns

```
[('B','C',1), ('B','D',2), ('E','F',2), ('A','C',3), ('D','F',3)]   total = 11
```

5 edges $= n-1$ ✓

**3.2** *(6 pts)* Prim from all six starts:

| Start | Total | Edge set |
|---|---|---|
| $A$ | 11 | $\{AC, BC, BD, DF, EF\}$ |
| $B$ | 11 | same |
| $C$ | 11 | same |
| $D$ | 11 | same |
| $E$ | 11 | same |
| $F$ | 11 | same |

**Both questions answered: all six give the same total, and on this graph all six give the same edge
set** — because the weights that matter here are unambiguous. The *order* of insertion differs, which
is the only thing the starting vertex controls.

*Do not let students conclude that Prim always gives one edge set; 3.3 exists to break that.*

**3.3** *(5 pts)* Retie the weights: set $AB = 3$ (equal to $AC$). Then $\{AB, BC, BD, DF, EF\}$ and
$\{AC, BC, BD, DF, EF\}$ are **both** spanning trees of total **11**. Two distinct MSTs, equal totals.

Make every weight distinct and the MST becomes unique: at each step of the exchange argument the
inequality $w(f) \ge w(e)$ becomes strict, so no alternative optimum survives.

**3.4** *(4 pts)* Cayley verification:

| $n$ | Subsets tested | Trees found | $n^{n-2}$ |
|---|---|---|---|
| 4 | 20 | 16 | 16 ✓ |
| 5 | 210 | 125 | 125 ✓ |

Growth of the brute force, $\binom{\binom n2}{n-1}$:

| $n$ | 7 | 9 | 11 |
|---|---|---|---|
| Subsets | 54 264 | 30 260 340 | 29 248 649 430 |

**$n=7$ is comfortably runnable; $n=9$ is a minute or two; $n=11$ is out of reach.** A reasonable
answer names 8 or 9 as the practical limit.

*Marking: full credit requires computing the three counts, not guessing. Students who claim $n=7$ is
infeasible have not computed it.*

---

## Section 4 Solutions

**4.1** *(5 pts)*

| Start | BFS | DFS |
|---|---|---|
| $a$ | $a,b,c,d,e,f,g$ | $a,b,d,e,c,f,g$ |
| $b$ | $b,a,d,e,c,f,g$ | $b,a,c,f,g,d,e$ |

**4.2** *(5 pts)* `bfs_distances(adj, a)` gives $a$:0, $b$:1, $c$:1, $d$:2, $e$:2, $f$:2, $g$:2 —
identical to `depths(adj, a)`.

**They agree because a tree has a unique path between any two vertices**, so the only path from the
root is necessarily the shortest one. In a general graph the two notions diverge: depth in a
traversal tree can exceed the true distance.

**4.3** *(6 pts)*
- On the DAG: `['a','b','c','d','e']` (and `['a','c','b','d','e']` is equally valid).
- On $a\to b\to c\to a$: **`None`**.

**What `None` means to a build system:** the dependency graph contains a cycle, so **no valid build
order exists** — some target would have to be built before itself. The tool reports "circular
dependency detected". This is not a limitation of the algorithm; it is a correct statement that the
project is unbuildable as specified, and the fix is to break the cycle.

**4.4** *(4 pts)* `is_bipartite` returns **True** for $C_4$ and $T$, **False** for $C_5$.

**Every tree is bipartite** because bipartiteness fails only on odd cycles, and a tree has no cycles
at all. Concretely, 2-colour by depth parity: every edge joins consecutive depths, hence different
parities.

---

## Section 5 — Reflection Model Answers

1. **Prim from six starts.** The *insertion order* varied; the *total* never did, and on this graph
   neither did the edge set. This reflects the MST being an optimum of a well-defined minimisation:
   the value is a property of the graph, while the path the algorithm takes to it is not.

2. **Why everything here is fast.** Trees have **no cycles**, so there is a unique path between any
   two vertices — nothing to choose between. For MSTs, the **cut property** guarantees a locally
   cheapest choice is globally safe, which is what licenses a greedy algorithm. Week 10's Hamilton
   problem has no such property: no local test tells you whether an edge belongs to a Hamiltonian
   cycle, so the search cannot be pruned and stays factorial.

3. **`None` is not a failure.** The algorithm answered the question correctly — the question just has
   no positive answer. A topological order exists **iff** the graph is acyclic; returning `None` on a
   cyclic input is the specification being met, not violated.

---

## Checkoff Summary

| Section | Watch for |
|---|---|
| 1.2 | Rooted leaves ($e,f,g$) not confused with degree-1 vertices |
| 2.1 | All three cases explained, both conditions understood as necessary |
| 2.3 | Full height table; centre identified as $a$ |
| 3.1 | Total 11 with 5 edges |
| 3.2 | **Both** questions answered explicitly |
| 3.3 | Two genuinely distinct MSTs exhibited |
| 3.4 | Subset counts computed, not guessed |
| 4.3 | `None` explained in build-system terms |

---

*MATH 151 · Week 11 · Lab 11 Solutions · Instructor copy — do not distribute*
