# CS 102 · Problem Set 4
## Graph Representations and Traversal

**Released:** Friday 19 February 2027, 10:00 (after L15) · Week 4
**Due:** Friday 26 February 2027, 17:00 · Week 5 — late penalty from 17:01 (syllabus late policy)
**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4–5 hours

**Submit:** `ps4.py` (all code, runnable end to end) and `ps4.md` (written answers, tables, proofs).
Written answers inside code comments will not be marked.

Graphs are 0-indexed with vertex set $\{0, \dots, V-1\}$. Unless stated otherwise, graphs are
**undirected** and **simple**. Use `collections.deque` for queues.

## What this problem set uses

Weeks 0–4: both representations (L13), BFS, shortest-path trees, components and bipartiteness (L14),
DFS, timestamps, the parenthesis theorem, edge classification and undirected cycle detection (L15).
The forest identity in D2 is stated in the question.

**Not needed and not expected:** weighted shortest paths, topological sort, Floyd–Warshall or
union–find (Weeks 5, 6 and 8). Memory and timing measurements are not asked for: Lecture 13 §4 and
§7 already made them.

> **Midterm 1 (Weeks 0–4) is Monday 1 March 2027, 18:00–19:15** — Week 6, a week after this set is
> due. Everything here is examinable on it.

---

## Part A — Representations (10 points)

**A1.** *(10)* Write `AdjList` and `AdjMatrix` classes, each supporting `add_edge(u, v)`,
`neighbours(u)`, `has_edge(u, v)`, and `V`/`E` properties. Both must accept the same test suite.

---

## Part B — BFS (26 points)

**B1.** *(8)* `bfs(g, s)` returning `dist` and `parent` arrays, with $-1$ and `None` for unreachable
vertices.

**B2.** *(6)* `path(parent, s, v)` reconstructing a shortest path as a vertex list, or `None` if $v$
is unreachable.

Explain in one sentence why storing `parent` is preferable to storing the paths themselves.

**B3.** *(6)* `components(g)` returning a component-id array and the count. Argue in two sentences why
running BFS from every undiscovered vertex is $\Theta(V+E)$ **in total**, not $\Theta(V(V+E))$.

**B4.** *(6)* `bipartite(g)`, returning `(True, colouring)` or `(False, None)`.

Test it on cycles of length 3 through 8 and report the pattern. Then state the theorem your results
suggest, in terms of cycles.

---

## Part C — DFS and Timestamps (34 points)

**C1.** *(8)* `dfs_iter(g, s)` using an explicit stack.

Then: build a path graph of 5,000 vertices and run a **recursive** DFS on it. Report what happens.
Explain why `sys.setrecursionlimit(100000)` is not a satisfactory fix.

**C2.** *(8)* `dfs_timestamps(g)` computing `d`, `f`, and `parent` for a **directed** graph, looping
over all vertices so that a forest is produced.

Verify on at least 200 random digraphs that the $2V$ timestamps are exactly a permutation of
$1 \dots 2V$ and that $d[u] < f[u]$ for every $u$. Report the count.

**C3.** *(10)* **The parenthesis theorem.**

- **(a)** *(3)* State it precisely: for any $u, v$, exactly which three cases are possible?
- **(b)** *(3)* Verify it computationally. For every ordered pair in at least 100 random digraphs,
  confirm exactly one case holds, **and** that interval containment matches the descendant relation
  computed independently by walking the `parent` array. Report pairs checked and failures.
- **(c)** *(2)* Write `is_descendant(u, v)` in $O(1)$ using only `d` and `f`, and say why that is
  useful.

**C4.** *(8)* Classify every edge of a directed graph as tree, back, forward, or cross.

Then verify the theorem **"a digraph is cyclic iff DFS finds a back edge"** by comparing your
back-edge test against a brute-force cycle detector — a digraph has a cycle exactly when some vertex
$u$ is reachable from one of its own successors, which a BFS from each successor settles (Lecture 14) on at least 500 random digraphs.
Report the number that were cyclic and the number of mismatches.

---

## Part D — Undirected Cycle Detection (30 points)

**D1.** *(10)* Implement `has_cycle(g)` for undirected graphs. Show that omitting the parent check
reports a cycle in a **tree**, and give the smallest tree on which this happens.

**D2.** *(20)* It is commonly claimed that the `v != parent` test is "correct only for simple graphs,
because it misses a 2-cycle formed by parallel edges."

**Test this claim.** Search exhaustively over all multigraphs on $V \le 4$ with up to 3 edges —
self-loops and parallel edges included — comparing against an independent ground truth. Then:

> **Building the ground truth.** Use the edge-count characterisation, which needs nothing beyond
> this week's traversals: a graph is **acyclic (a forest) if and only if** $|E| = |V| - c$, where
> $c$ is its number of connected components. Count $c$ with the BFS or DFS you wrote in Part B,
> then compare. Count parallel edges separately and count a self-loop as one edge — getting those
> two conventions right is half the problem.
>
> *(You may recognise this as a job for a disjoint-set structure. It is — union–find arrives in
> Week 6 and is the tool you would reach for in practice. The edge-count identity gives the same
> answer using only what you have now.)*

- **(a)** *(10)* Is the claim true? Report your disagreement count and explain the result.
- **(b)** *(10)* Repeat with adjacency built from `set` instead of `list`. Report the count, give the
  smallest failing case, and say exactly where the fault lies.

> **D2 is the part to spend time on.** You are being asked to check a piece of received wisdom, and
> the answer is not the one the claim states.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 10 | Both representations behind one interface |
| B | 26 | BFS, paths, components, bipartiteness |
| C | 34 | DFS, timestamps, the parenthesis theorem, edge classification |
| D | 30 | Undirected cycles, and checking a claim rather than repeating it |
| **Total** | **100** | |

---

## Reference Numbers

**Your verification counts in C2, C3, C4 and D2 should all be zero mismatches** — except D2(b),
which is meant to find failures. If any other count is not zero, the bug is yours to find and report;
a submission that reports non-zero mismatches without investigating them scores no credit for that
part.

---

## A Note on Part D2

D2 gives you a claim that appears in textbooks and on every algorithms forum, and asks you to check it
by exhaustive search rather than accept it. **A claim you have not tested is a liability**, and the
difference between a competent engineer and a fluent one is largely how quickly such claims get
checked.

---

*CS 102 · Week 4 · Problem Set 4 · © CSE Department*
