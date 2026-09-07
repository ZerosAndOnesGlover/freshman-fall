# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 4: Graphs I — Representations and Traversals

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 4** (released Friday, due Friday of Week 5), Lab 4, **Quiz 4 —
which covers Week 3**.
**MIDTERM 1 is announced this week** and sits in Week 5, covering Weeks 0–4. See
[[CS102 Week4/resources/MIDTERM 1 Revision Guide|MIDTERM 1 Revision Guide]].

---

### Why This Week Exists

Everything so far has been a *container*. A BST, an AVL tree, a heap — each holds items and answers
questions about the items.

**A graph is a relation.** The items matter less than the connections between them, and every
interesting question is about the connections. That change of subject is why graphs occupy a third of
this course, and why the algorithms look different: nobody will ask you to insert into a graph
efficiently.

The week's organising idea is a single piece of pseudocode:

```
put the source into a COLLECTION
while the COLLECTION is not empty:
    take a vertex u out, skip it if visited, mark it visited
    put all of u's neighbours in
```

**Change the collection and you change the algorithm.** A queue gives BFS and fewest edges; a stack
gives DFS and structure; a priority queue — the thing you built in Week 3 — gives Dijkstra and least
total weight. One skeleton, three data structures, three meanings of "next". That is the reason heaps
came before graphs rather than after.

### Learning Objectives

By the end of Week 4, you should be able to:

1. Use graph terminology precisely, and state the handshake lemma and its corollary.
2. Choose between adjacency matrix and adjacency list for a stated graph and workload, **citing the
   measured crossover rather than the asymptotics**.
3. Implement BFS and prove it computes shortest paths, via queue monotonicity.
4. Say exactly where that proof uses the assumption that all edges have equal weight.
5. Implement DFS both recursively and iteratively, and say when the recursive form fails and why
   raising the recursion limit is not a fix.
6. Compute discovery and finish times, and use the parenthesis theorem to answer ancestry queries in
   $O(1)$.
7. Classify edges as tree, back, forward, or cross, and prove that a digraph is cyclic **iff** DFS
   finds a back edge.
8. Explain why undirected DFS produces only tree and back edges, and why a naive classifier appears to
   contradict this.
9. Find connected components and test bipartiteness, and state the odd-cycle theorem.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L13 Graphs Terminology and Representation]] | Terminology, both representations measured, the traversal skeleton |
| [[L14 Breadth-First Search]] | BFS, the shortest-path proof, components, bipartiteness |
| [[L15 Depth-First Search Timestamps and Edge Classification]] | DFS, timestamps, parenthesis theorem, edge types, cycles |
| [[PS 4 Graph Traversal]] | 100 points, due Friday of Week 5 |
| [[CS102 Week4/assignments/QUIZ 4 Week 4 Monday\|QUIZ 4 Week 4 Monday]] | 20 points, formative — **covers Week 3** |
| [[LAB 4 BFS and DFS on a Social Network]] | Degrees of separation, and a heuristic that gets it wrong |
| [[CS102 Week4/resources/Reading Guide Week 4\|Reading Guide Week 4]] | CLRS §20.1–20.3, with the misreadings to avoid |
| [[CS102 Week4/resources/MIDTERM 1 Revision Guide\|MIDTERM 1 Revision Guide]] | Format, examinable material, the eight reproducible proofs |
| `solutions_instructor/` | PS 4 and Lab 4 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. DFS does not find shortest paths.** On a 7-cycle, BFS gives vertex 6 a distance of 1 — it is
adjacent to the source — while DFS places it at tree depth **6**. Both traversals visit the same
vertices; only one of the trees means anything metric. Lab 4 makes the point at scale: on the social
network, BFS's eccentricity from vertex 0 is **4** and the DFS tree depth is **3,226**.

**2. Grey means "on the stack right now", not "visited".** Black means visited and finished. The whole
back-edge test rests on that distinction, and conflating the two is the standard way to produce a
cycle detector that does not work.

**3. $\Theta(V+E)$ is a count of operations, not a promise about time.** Measured, BFS costs about 80 ns
per unit of $(V+E)$ at $V = 10^4$ on both random and grid graphs. By $V = 10^6$ the random graph has
degraded to 399 ns and the grid only to 119 — **3.4× apart on inputs with the same $V$ and $E$**. The
notation says nothing about memory locality, which means a graph benchmark without its graph family
is close to meaningless.

### A Claim This Week Asks You to Disbelieve

It is widely stated that the `v != parent` test in undirected cycle detection "fails on multigraphs,
because it misses the 2-cycle formed by parallel edges."

**It does not.** A parallel edge appears *twice* in a list-based adjacency structure, so the second
copy is found and the cycle is reported. Verified exhaustively over every multigraph on $V \le 4$ with
up to 3 edges, against a union-find ground truth: **0 disagreements.**

The real fault is one step earlier. Build adjacency from `set` instead of `list` and the duplicate is
discarded before the algorithm runs — **56 wrong answers** in the same search, the smallest being two
vertices joined by two edges. **The received wisdom names the algorithm; the bug is in the data
structure.** PS 4 D4 makes you settle it by search rather than by argument.

### A Note on the Measurements

**Counts are deterministic** — memory figures, edge-type counts, verification totals, and every number
in Lab 4. If yours differ, your construction differs, and the discrepancy is worth finding before you
continue.

**Timings are not**, and this week they are less transferable than usual: the same code differs by
3.4× between two graph families of identical size. When you report a graph timing, report the graph.

### Connections

**Back:** The traversal skeleton's third instantiation is **Week 3**'s priority queue. The locality
argument in Lecture 13 §7 is Week 3's `sift_down` stride problem in a new setting, and the
representation crossover is the third time this term — after `SortedList` in **Week 2** and heap sort
in **Week 3** — that asymptotics have failed to predict which implementation wins at a given size.
The handshake lemma and graph terminology are **MATH 151**.

**Forward:** **Week 5** replaces the queue with a priority queue and gets Dijkstra, and uses this
week's finish-time ordering for topological sort, DAG shortest paths, and strongly connected
components. **Week 6** builds minimum spanning trees on the same traversal machinery. **Week 8**'s
tree DP uses the parenthesis theorem for ancestry. **Week 11** extends the back-edge idea to bridges
and articulation points. **Week 12** returns to bipartiteness as 2-colouring — the one graph-colouring
problem that is not NP-complete.

---

*CS 102 · Week 4 · © CSE Department*
