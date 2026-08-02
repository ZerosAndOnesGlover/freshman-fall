# MATH 151 — Discrete Mathematics for Computer Science
## Lecture 11.1 (L33) — Trees and Their Properties
### Monday, Week 11

---

## 1. The Definition, and Why It Is Restrictive

> **Definition.** A **tree** is a connected graph with no cycles.

Week 10 showed that graphs in general are hard: isomorphism has no known efficient algorithm,
Hamiltonicity is NP-complete. **Trees are where almost all of that difficulty disappears.** Removing
cycles removes choice, and removing choice is what makes algorithms fast.

A **forest** is a graph with no cycles — that is, a disjoint union of trees.

### The running example

$$V=\{a,b,c,d,e,f,g\},\qquad E=\{ab,\ ac,\ bd,\ be,\ cf,\ cg\}$$

7 vertices, 6 edges, connected, acyclic. Every claim below is checked against it.

---

## 2. Five Equivalent Characterisations

> **Theorem.** For a graph $G$ with $n$ vertices, the following are **equivalent**:
>
> 1. $G$ is a tree (connected, acyclic)
> 2. $G$ is connected with exactly $n-1$ edges
> 3. $G$ is acyclic with exactly $n-1$ edges
> 4. There is a **unique** path between every pair of vertices
> 5. $G$ is connected, and removing any edge disconnects it

**Verified:** the running example is connected with $6 = 7-1$ edges ✓

Each characterisation is the useful one somewhere:

- **(2)** is how you check "is this a tree?" in one line — count edges after confirming connectivity.
- **(4)** is why trees are used for routing and for file systems: there is never ambiguity about how
  to get from one place to another.
- **(5)** says **every edge of a tree is a bridge**. Trees are maximally fragile — they are exactly
  the connected graphs with no redundancy whatever.

### Proof that (1) ⟹ (2), by induction on $n$

**Base:** $n=1$. One vertex, no edges $= n-1$ ✓

**Step:** let $T$ be a tree on $n\ge2$ vertices. A finite tree has a **leaf** (a vertex of degree 1)
— if every vertex had degree $\ge2$ you could walk forever without repeating an edge, and in a finite
graph that forces a cycle. Remove a leaf $v$ and its single edge: the result is still connected and
acyclic, so by the induction hypothesis it has $(n-1)-1$ edges. Adding $v$ back gives $n-1$. ∎

*The "a finite tree has a leaf" step is the one to dwell on. It is used again in Wednesday's proof
and in nearly every tree induction you will ever write.*

---

## 3. Counting Consequences

$$\sum_{v\in V}\deg(v)=2\lvert E\rvert = 2(n-1)$$

**Verified:** the running example has degrees $2,3,3,1,1,1,1$, summing to $12 = 2\times6$ ✓

**Every tree with $n\ge2$ vertices has at least two leaves.** If it had at most one, the degree sum
would be at least $1 + 2(n-1) = 2n-1 > 2n-2$ — too many. The running example has four leaves:
$d, e, f, g$.

---

## 4. Rooted Trees

Choosing a **root** imposes direction: every other vertex has a unique parent (its neighbour on the
unique path to the root).

| Term | Meaning |
|---|---|
| Root | The distinguished vertex |
| Parent / child | Neighbour towards / away from the root |
| Leaf | No children |
| Internal | Has at least one child |
| Depth of $v$ | Length of the path from the root |
| Height | Maximum depth |
| Subtree at $v$ | $v$ and all its descendants |

**Verified** for the running example rooted at $a$:

| Vertex | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ |
|---|---|---|---|---|---|---|---|
| Depth | 0 | 1 | 1 | 2 | 2 | 2 | 2 |

**Height 2**, leaves $d,e,f,g$, internal vertices $a,b,c$.

**The same tree rooted elsewhere has a different height.** Rooting is a choice imposed on the tree,
not a property of it.

---

## 5. Binary Trees and the Height Bound

A **binary tree** gives each node at most two children. It is **full** if every internal node has
exactly two, and **perfect** if additionally all leaves are at the same depth.

> **Theorem.** A binary tree of height $h$ has at most $2^{h+1}-1$ nodes, and at least $h+1$.

**Verified:**

| Height $h$ | Max nodes $2^{h+1}-1$ | Min nodes $h+1$ |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 3 | 2 |
| 2 | 7 | 3 |
| 3 | 15 | 4 |
| 4 | 31 | 5 |

Inverting the upper bound: a binary tree with $n$ nodes has height **at least**
$\lceil\log_2(n+1)\rceil - 1$.

**Verified minimum heights:** $n=7 \to 2$; $n=8 \to 3$; $n=15 \to 3$; $n=16 \to 4$;
$n=100 \to \mathbf{6}$.

**This is the theorem behind every balanced search tree.** A binary search tree on $n$ items *can*
have height $n-1$ — a degenerate path, giving $\Theta(n)$ lookups. The bound says height
$\Theta(\log n)$ is *possible*; AVL and red–black trees are the machinery that forces it. The gap
between $\log_2(10^6)\approx20$ and $10^6$ comparisons is the whole reason those data structures
exist.

---

## 6. Trees in Computer Science

| Application | Structure |
|---|---|
| File system | Directory tree — unique path is the absolute path |
| Binary search tree | Ordered tree; $\Theta(\log n)$ search when balanced |
| Heap | Complete binary tree with an ordering invariant |
| Parse tree | Grammatical structure of source code |
| Decision tree | Classification; depth is the number of questions asked |
| Huffman code | Optimal prefix-free encoding |
| Git | Commit DAG; each tree object is a directory snapshot |
| Spanning tree | Loop-free routing over a physical network |

**The unique-path property is what most of these rely on.** A file system has exactly one absolute
path per file; a prefix-free code has exactly one decoding.

---

## 7. Summary

| | |
|---|---|
| Tree | Connected and acyclic |
| Edge count | Exactly $n-1$ |
| Path between any two vertices | **Unique** |
| Every edge | Is a bridge — no redundancy |
| Leaves | At least 2, when $n\ge2$ |
| Degree sum | $2(n-1)$ |
| Rooted | Depth, height, parent, child — imposed, not intrinsic |
| Binary tree, height $h$ | At most $2^{h+1}-1$ nodes |
| Binary tree, $n$ nodes | Height at least $\lceil\log_2(n+1)\rceil-1$ |

---

## 8. End-of-Lecture Exercises

1. A tree has 15 vertices. How many edges? What is the sum of its degrees?

2. A tree has 10 vertices, of which 6 are leaves. If the remaining vertices all have the same degree, what is it?

3. Draw all non-isomorphic trees on 5 vertices. *(There are three.)*

4. Root the running example at $d$ instead of $a$. Give the new depths and height, and say why they differ.

5. What is the minimum possible height of a binary tree with 1000 nodes? With $10^6$?

6. **(Stretch.)** Prove that a graph is a tree if and only if it is connected and every edge is a bridge. *(Both directions.)*

---

## Reading

- **Rosen, 8e §11.1** — Introduction to trees
- **Epp, 5e §10.5** — Trees: definitions and properties
- **Levin, 3e §4.3** — Trees

*Next: Lecture 11.2 — Spanning Trees and Minimum Spanning Trees*
