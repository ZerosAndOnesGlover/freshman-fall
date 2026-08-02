# CS 102 · Reading Guide, Week 4
## Graphs — Representations and Traversal

---

## Required

**CLRS, 4th ed. — §20.1, §20.2, §20.3** (Elementary Graph Algorithms).

About 30 pages, and unusually well written. §20.3 is the densest thing you have been asked to read
this term and repays a second pass.

Skip §20.4 (topological sort) and §20.5 (strongly connected components) **for now** — they are Week 5.
Lecture 15 §6 previews topological sort because it follows from §20.3 with no new machinery, but the
reading can wait.

Also useful:

- **Sedgewick & Wayne §4.1–4.2** — the best diagrams of BFS and DFS anywhere, and a genuinely good
  discussion of graph-processing API design.
- **Skiena §5** — the practitioner's view, with war stories about which representation to pick.

---

## A Note on CLRS's Notation

CLRS writes $O(V + E)$ where it means $O(|V| + |E|)$, and so does this course. It also writes
$G = (V, E)$ and then uses $V$ as a number. This is universal in the literature and worth getting used
to rather than fighting.

More importantly: **CLRS's `BFS` and `DFS` use vertex attributes** (`u.color`, `u.d`, `u.π`) where the
lectures use parallel arrays (`color[u]`, `d[u]`, `parent[u]`). These are the same thing. Arrays are
faster in Python and make the $\Theta(V)$ space obvious; attributes read better in pseudocode.

---

## How to Read Chapter 20

**§20.1 (representations, 5 pages).** Short. The two-page comparison is the whole content. Note
Exercise 20.1-7 — the square of the adjacency matrix counts paths of length 2 — which is a genuinely
surprising fact and a plausible exam question.

**§20.2 (BFS, 9 pages).** The algorithm is a page; the rest is the proof that it computes shortest
paths, and **the proof is the reason to read it.** Follow the chain: Lemma 20.1 (distances satisfy a
triangle inequality), Lemma 20.2 ($d$ is an upper bound on the true distance), Lemma 20.3 (the queue
holds at most two distinct distances), Theorem 20.5 (therefore $d$ is exact).

**Lemma 20.3 is the load-bearing one** and is the "queue monotonicity" property of Lecture 14 §2.
Everything else follows from it.

**§20.3 (DFS, 12 pages).** The chapter's centre of gravity.

- §20.3.1: the algorithm and the timestamps.
- §20.3.2: **the parenthesis theorem (Theorem 20.7) and the white-path theorem (Theorem 20.9).** Read
  both twice. The white-path theorem — *$v$ is a descendant of $u$ iff at time $d[u]$ there is a path
  $u \rightsquigarrow v$ consisting entirely of white vertices* — is not in the lectures and is the
  cleanest tool for reasoning about DFS forests. It is worth the extra effort.
- §20.3.3: the $\Theta(V+E)$ analysis.
- §20.3.4: edge classification, and Theorem 20.10 — in an undirected graph every edge is a tree edge
  or a back edge.

---

## Guiding Questions

Answer these as you read. They are not submitted, and three are on MIDTERM 1.

1. §20.1: the adjacency matrix costs $\Theta(V^2)$ *whatever* $E$ is. Name a graph on 10,000 vertices
   where that is clearly the right choice anyway, and say what makes it right.

2. §20.2, Lemma 20.3: why can the queue never hold three distinct distance values? What in the code
   prevents it?

3. §20.2: BFS computes shortest paths in unweighted graphs. **Exactly where does the argument use the
   fact that all edges have the same weight?** Find the specific line — this is Week 5's starting
   point.

4. §20.3, Theorem 20.7: the theorem forbids partially overlapping intervals. Explain why that is
   obvious once you think of $[d(u), f(u)]$ as a stack lifetime.

5. §20.3.4: in a directed graph, which of the four edge types can point from a vertex to one **not**
   yet discovered? Which can point backwards in time?

6. Theorem 20.10 says undirected graphs have only tree and back edges. Lecture 15 §4 reports counting
   1,487 forward edges in undirected graphs. **Reconcile these.** (The reconciliation is the point of
   PS 4 D1–D2.)

7. Compare the collection in BFS, DFS, and the priority queue of Week 3. What single property of the
   collection determines which algorithm you get?

---

## Common Misreadings

**"DFS finds shortest paths too."** It does not. On a 7-cycle, DFS can place a vertex adjacent to the
source at depth 6. BFS is the algorithm with the shortest-path guarantee; DFS has a different and
larger set of uses.

**"BFS is $\Theta(V+E)$, so it takes time proportional to $V+E$."** It performs $\Theta(V+E)$
*operations*. Measured, the time per operation grows 5× between $V = 10^4$ and $V = 10^6$ on random
graphs and only 1.5× on grids — see Lecture 13 §7. The bound is correct; it is a count, not a clock.

**"Grey means visited."** Grey means **on the current recursion stack**. Black means visited and
finished. The distinction is the entire content of the back-edge test, and conflating the two is the
most common source of a broken cycle detector.

**"The adjacency matrix wastes memory, so never use it."** At densities above about 50% in Python it
uses *less* memory than an adjacency list, and it gives $O(1)$ edge queries that a list cannot. Use
lists because real graphs are sparse, not because the matrix is bad.

**"`v != parent` fails on multigraphs."** This is stated confidently in many places and is **false** —
a parallel edge appears twice in a list-based adjacency structure and is found. What fails is building
adjacency from `set`, which discards the duplicate before the algorithm runs. PS 4 D4 makes you settle
this by exhaustive search.

---

## If You Have Extra Time

**The white-path theorem** (§20.3.2). Genuinely elegant, and the right tool for most DFS proofs.

**Exercise 20.1-7.** If $A$ is an adjacency matrix, what does $A^2$ count? Then $A^k$? This is the
doorway to spectral graph theory and to the matrix formulation of all-pairs shortest paths in Week 8.

**Problem 20-1 (classifying edges by BFS).** BFS also induces an edge classification, and it is
different from DFS's. Working out which types can occur is a good test of whether you have understood
both.

**Bidirectional search.** To find the distance between two specific vertices, run BFS from both ends
and stop when the frontiers meet. On a graph with branching factor $b$ and distance $d$, this explores
$O(b^{d/2})$ rather than $O(b^{d})$ vertices — a square-root saving that is enormous in practice. It
is how route planners were built before contraction hierarchies, and Lab 4's network is a good place
to try it.

---

*CS 102 · Week 4 · Reading Guide · © CSE Department*
