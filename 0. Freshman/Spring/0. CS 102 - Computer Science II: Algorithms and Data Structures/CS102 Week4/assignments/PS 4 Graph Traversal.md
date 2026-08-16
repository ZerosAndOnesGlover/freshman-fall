# CS 102 · Problem Set 4
## Graph Representations and Traversal

**Released:** Friday, Week 4 · **Due:** Friday, Week 5, 23:59
**100 points · counts toward the Problem Sets component (35% of the final grade)**

**Submit:** `ps4.py` (all code, runnable end to end) and `ps4.md` (written answers, tables, proofs).
Written answers inside code comments will not be marked.

Graphs are 0-indexed with vertex set $\{0, \dots, V-1\}$. Unless stated otherwise, graphs are
**undirected** and **simple**. Use `collections.deque` for queues.

> **MIDTERM 1 (Weeks 0–4) is in Week 5.** This problem set is due the same week. Start early —
> Parts A and B are the examinable material and are worth doing before the midterm rather than after.

---

## Part A — Representations (16 points)

**A1.** *(6)* Write `AdjList` and `AdjMatrix` classes, each supporting `add_edge(u, v)`,
`neighbours(u)`, `has_edge(u, v)`, and `V`/`E` properties. Both must accept the same test suite.

**A2.** *(4)* Measure the memory of both, recursively (`sys.getsizeof` applied through the nested
lists), for $V \in \{100, 500, 1000, 2000\}$ at $E = 2V$. Tabulate and give the ratio.

State what the ratio does when $V$ doubles, and why.

**A3.** *(6)* Fix $V = 400$ and vary $E$ over $\{400, 2000, 10000, 40000, 79800\}$ — the last is the
complete graph. Tabulate memory for both and find **the density at which the matrix becomes the
smaller representation.**

Then answer:

- The asymptotics say $\Theta(V+E)$ beats $\Theta(V^2)$ for any sparse graph. Your crossover is much
  later than that suggests. **Why?** Your answer must refer to how Python stores a list of small
  integers.
- Would the crossover move if you wrote this in C with a bit-packed matrix? Which way, and roughly how
  far?

---

## Part B — BFS (24 points)

**B1.** *(6)* `bfs(g, s)` returning `dist` and `parent` arrays, with $-1$ and `None` for unreachable
vertices.

**B2.** *(4)* `path(parent, s, v)` reconstructing a shortest path as a vertex list, or `None` if $v$
is unreachable.

Explain in one sentence why storing `parent` is preferable to storing the paths themselves.

**B3.** *(6)* Verify B1 **against an independent reference**: implement Floyd–Warshall for unweighted
graphs and compare BFS distances from **every** source, on at least 100 random graphs of up to 15
vertices. Report graphs tested, source–target pairs compared, and mismatches.

**B4.** *(4)* `components(g)` returning a component-id array and the count. Argue in two sentences why
running BFS from every undiscovered vertex is $\Theta(V+E)$ **in total**, not $\Theta(V(V+E))$.

**B5.** *(4)* `bipartite(g)`, returning `(True, colouring)` or `(False, None)`.

Test it on cycles of length 3 through 8 and report the pattern. Then state the theorem your results
suggest, in terms of cycles.

---

## Part C — DFS and Timestamps (26 points)

**C1.** *(5)* `dfs_iter(g, s)` using an explicit stack.

Then: build a path graph of 5,000 vertices and run a **recursive** DFS on it. Report what happens.
Explain why `sys.setrecursionlimit(100000)` is not a satisfactory fix.

**C2.** *(7)* `dfs_timestamps(g)` computing `d`, `f`, and `parent` for a **directed** graph, looping
over all vertices so that a forest is produced.

Verify on at least 200 random digraphs that the $2V$ timestamps are exactly a permutation of
$1 \dots 2V$ and that $d[u] < f[u]$ for every $u$. Report the count.

**C3.** *(8)* **The parenthesis theorem.**

- **(a)** *(3)* State it precisely: for any $u, v$, exactly which three cases are possible?
- **(b)** *(3)* Verify it computationally. For every ordered pair in at least 100 random digraphs,
  confirm exactly one case holds, **and** that interval containment matches the descendant relation
  computed independently by walking the `parent` array. Report pairs checked and failures.
- **(c)** *(2)* Write `is_descendant(u, v)` in $O(1)$ using only `d` and `f`, and say why that is
  useful.

**C4.** *(6)* Classify every edge of a directed graph as tree, back, forward, or cross.

Then verify the theorem **"a digraph is cyclic iff DFS finds a back edge"** by comparing your
back-edge test against an independently written cycle detector on at least 500 random digraphs.
Report the number that were cyclic and the number of mismatches.

---

## Part D — Undirected Cycle Detection (18 points)

**D1.** *(4)* Show by direct experiment that classifying undirected edges by colour appears to produce
forward edges. Run the classifier on at least 200 random undirected graphs, counting each edge from
**both** endpoints, and report the four counts.

You should find `forward` equal to `back`. Explain why, in one sentence.

**D2.** *(4)* Now classify each **physical edge on its first encounter only**. Report the four counts
again and state the theorem your numbers support.

**D3.** *(4)* Implement `has_cycle(g)` for undirected graphs. Show that omitting the parent check
reports a cycle in a **tree**, and give the smallest tree on which this happens.

**D4.** *(6)* It is commonly claimed that the `v != parent` test is "correct only for simple graphs,
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

- **(a)** *(3)* Is the claim true? Report your disagreement count and explain the result.
- **(b)** *(3)* Repeat with adjacency built from `set` instead of `list`. Report the count, give the
  smallest failing case, and say exactly where the fault lies.

> **D4 is the part to spend time on.** You are being asked to check a piece of received wisdom, and
> the answer is not the one the claim states.

---

## Part E — Reading the Cost Model (16 points)

**E1.** *(6)* Time BFS on random graphs of average degree 6 for
$V \in \{10^4, 5\times10^4, 2\times10^5, 10^6\}$, best of 5. Report milliseconds **and nanoseconds per
$(V+E)$**.

**E2.** *(4)* BFS is $\Theta(V+E)$. Your ns-per-$(V+E)$ column is not constant. **Is the bound wrong?**
Answer in three sentences or fewer.

**E3.** *(6)* Repeat E1 on a **grid graph** — the $k \times k$ lattice, with vertex $(i,j)$ numbered
$ik+j$ — at comparable sizes. Compare the two ns-per-$(V+E)$ columns and explain the difference.

What does this imply about published graph-algorithm benchmarks?

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 16 | Both representations; the real crossover |
| B | 24 | BFS, verified against an independent reference |
| C | 26 | DFS, timestamps, the parenthesis theorem, edge classification |
| D | 18 | Undirected cycles, and checking a claim rather than repeating it |
| E | 16 | $\Theta(V+E)$ as a count of operations, not a promise about time |
| **Total** | **100** | |

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14, x86-64 Linux). **Counts are
deterministic; timings are not.**

Memory, $E = 2V$ (A2):

| $V$ | matrix | list | ratio |
| --- | --- | --- | --- |
| 100 | 86,576 B | 13,772 B | 6.3 |
| 500 | 2,032,272 B | 88,220 B | 23.0 |
| 1,000 | 8,064,912 B | 199,164 B | 40.5 |
| 2,000 | 32,128,240 B | 420,080 B | 76.5 |

Crossover at $V = 400$ (A3): the matrix is 1,305,712 B at every density; the list passes it between
$E = 10{,}000$ (411,328 B, density 0.125) and $E = 40{,}000$ (1,520,720 B, density 0.501).

Undirected edge classification, 300 random graphs (D1, D2):

| | first encounter | counting both directions |
| --- | --- | --- |
| tree | 2,547 | 2,547 |
| back | 1,487 | 1,487 + 2,547 |
| forward | **0** | 1,487 |
| cross | **0** | 0 |

BFS timing (E1, E3), best of 5:

| $V$ | random: BFS | ns per $(V+E)$ | grid: BFS | ns per $(V+E)$ |
| --- | --- | --- | --- | --- |
| $\approx 10^4$ | 3.2 ms | 80.6 | 2.3 ms | 78.4 |
| $\approx 5\times10^4$ | 46.8 ms | 234.2 | 12.8 ms | 85.0 |
| $\approx 2\times10^5$ | 258.2 ms | 322.8 | 55.9 ms | 92.9 |
| $\approx 10^6$ | 1597.4 ms | 399.4 | 356.1 ms | 118.8 |

The two columns start together and diverge by a factor of 3.4. **That divergence is E3's whole
question.**

**Your verification counts in B3, C2, C3, C4 and D4 should all be zero mismatches.** If any is not,
the bug is yours to find and report — a submission that reports non-zero mismatches without
investigating them scores no credit for that part.

---

## A Note on Parts D4 and E2

Both ask you to disbelieve something.

D4 gives you a claim that appears in textbooks and on every algorithms forum, and asks you to check it
by exhaustive search rather than accept it. E2 gives you a bound you proved in lecture and a
measurement that appears to contradict it, and asks you to reconcile them without abandoning either.

These are the same skill. **A claim you have not tested and a measurement you have not explained are
both liabilities**, and the difference between a competent engineer and a fluent one is largely how
quickly each gets resolved.

---

*CS 102 · Week 4 · Problem Set 4 · © CSE Department*
