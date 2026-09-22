# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 5: Graphs II — Shortest Paths

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 5** (released Fri 26 Feb 10:00, due **Fri 5 Mar 17:00**), Lab 5 (**Tue 2 Mar**, 15:00), **Quiz 5** (Mon 22 Feb, 09:00) — which covers Week 4.
**MIDTERM 1 is next Monday, 1 March 2027, 18:00–19:15**, 75 minutes, covering Weeks 0–4. Nothing in
Week 5 is on it.

---

### Why This Week Exists

BFS finds the path with the fewest edges. Put weights on the edges and that stops being the question
anybody wants answered — the route through the fewest junctions is not the fastest route.

This week answers the weighted question three times, under three different assumptions:

| assumption on weights | algorithm | cost |
| --- | --- | --- |
| all equal | **BFS** (Week 4) | $\Theta(V+E)$ |
| graph is a **DAG**, any weights | **topological order** | $\Theta(V+E)$ |
| all **non-negative** | **Dijkstra** | $O((V+E)\log V)$ |
| **anything**, no negative cycle | **Bellman–Ford** | $O(VE)$ |

**Read that as a ladder of assumptions.** Each row buys speed by assuming more, and the engineering
question — which rung does my problem sit on — is worth more than any individual implementation.
Guessing too low is the subject of half this week's assessment.

Underneath all four is one operation. `relax(u, v, w)` asks whether the route to $v$ through $u$ beats
what we had. Every algorithm here is a scheme for relaxing the edges of every shortest path *in order*;
they differ only in how they guarantee it.

### Learning Objectives

By the end of Week 5, you should be able to:

1. State the relaxation invariants and the path-relaxation property, and explain how each algorithm
   guarantees the latter.
2. Prove that subpaths of shortest paths are shortest paths, and say why that is what makes the week
   possible.
3. Distinguish **negative edges** (Dijkstra breaks; the problem is fine) from **negative cycles** (the
   problem itself is ill-posed).
4. Produce a topological order two ways, and use it for shortest **and longest** paths on a DAG in
   $\Theta(V+E)$.
5. Implement Dijkstra with a heap, and **identify the one step of its correctness proof that requires
   non-negative weights**.
6. Implement Bellman–Ford with early termination, detect a negative cycle, and **extract** it.
7. Say what the $V-1$ round bound is a worst case *over*.
8. Find strongly connected components, and explain why the condensation of any digraph is a DAG.
9. Choose the right algorithm for a stated problem and justify it from the assumptions available.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L16 Weighted Shortest Paths Relaxation and DAGs]] | Relaxation, optimal substructure, topological order, DAG paths, SCC |
| [[L17 Dijkstras Algorithm]] | The algorithm, the proof, and exactly how it fails |
| [[L18 Bellman-Ford Negative Cycles and Choosing an Algorithm]] | Bellman–Ford as a DP, negative cycles, and the selection table |
| [[PS 5 Shortest Paths]] | 100 points, due Fri 5 Mar 17:00 |
| [[CS102 Week5/assignments/QUIZ 5 Week 5 Monday\|QUIZ 5 Week 5 Monday]] | 20 points, formative — **covers Week 4** |
| [[LAB 5 Route Planning on a Road Network]] | Dijkstra, A\*, and the cost-model change that breaks it |
| [[CS102 Week5/resources/Reading Guide Week 5\|Reading Guide Week 5]] | CLRS §20.4–20.5, §22.1–22.4 |
| `solutions_instructor/` | PS 5 and Lab 5 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. Dijkstra does not fail loudly on negative weights — it fails 2.3% of the time.** Over 1,632
random graphs with negative edges but no negative cycle, it returned a wrong answer on **38**. A fault
that appears on one input in forty passes a small test suite comfortably. Only the correctness
argument tells you the precondition, which is why PS 5 C3 asks you to name the single inequality that
needs it.

**2. The $O(VE)$ bound on Bellman–Ford is a worst case over *edge orderings*, and ordinary input is
nowhere near it.** With a three-line early exit, random graphs of up to 20,000 vertices converged in
**11 to 14 rounds** where $V-1$ is 19,999 — the rounds track the graph's hop-diameter, $\Theta(\log V)$,
not $V$. Those three lines turn a 793× penalty against Dijkstra into a 3× one.

**3. A DAG is the only case where the fastest algorithm also has the weakest restriction on weights.**
$\Theta(V+E)$ *and* negative weights allowed — because a DAG has no cycles, hence no negative cycles,
and because the ordering comes from the graph's structure rather than from the weights. It also gives
longest paths for free, by negation, which is worth contrasting with the fact that longest simple path
on a general graph is NP-complete.

### Two Things That Are Not What They Look Like

**The standard counterexample does not break the code you will write.** Everyone is shown
$0\to1\ (-1)$, $0\to2\ (-2)$, $1\to2\ (-2)$ as the graph where Dijkstra fails. It does break the
textbook algorithm — but the lazy-deletion implementation everyone actually writes gets it **right**,
because it still relabels finalised vertices and only refuses to re-expand them. Breaking that version
needs **four** vertices, not three, and PS 5 C makes you find one.

**A\* can be silently, badly wrong after a change that touches no code.** On Lab 5's road network A\*
expands 7.3× fewer vertices than Dijkstra and returns identical distances on all 200 test queries.
Reinterpret the same edge weights as travel times with motorways 2.5× faster — same graph, same
coordinates, same heuristic — and it returns a suboptimal route on **101 of 200** queries, worst case
**74.9% too long**. A heuristic is a claim about the cost function, not about the graph.

### A Note on the Measurements

**Verification counts are deterministic and should all be zero mismatches**: 4,071 (graph, source)
pairs for Dijkstra against Bellman–Ford, 500 DAGs for DAG-SSSP, 600 digraphs for negative-cycle
detection, 400 for Kosaraju against transitive closure. Lab 5's network figures are deterministic too.

**Timings are not**, and Bellman–Ford's are especially input-dependent — see idea 2 above.

### Connections

**Back:** Dijkstra is **Week 4**'s BFS with **Week 3**'s priority queue substituted for the FIFO
queue, and the lazy-deletion trick is Week 3 Lecture 12 §3 verbatim. Topological order and SCC are
**Week 4**'s DFS finish times, which is why the Week 4 reading guide deferred CLRS §20.4–20.5 to now.
Optimal substructure is the same property that made divide-and-conquer work in **Week 0**.

**Forward:** **Week 6** keeps the greedy paradigm and changes the objective — the cut property plays
exactly the role that non-negativity plays here, and Prim's algorithm is Dijkstra with one line
changed. **Week 7** names dynamic programming and opens by pointing back at Bellman–Ford, which is a
DP over subproblems indexed by edge count. **Week 8**'s Floyd–Warshall does all pairs in
$\Theta(V^3)$. **Week 9**'s exchange arguments generalise Dijkstra's greedy proof. **Week 12** explains
why longest simple path, unlike shortest, is NP-complete.

---

*CS 102 · Week 5 · © CSE Department*
