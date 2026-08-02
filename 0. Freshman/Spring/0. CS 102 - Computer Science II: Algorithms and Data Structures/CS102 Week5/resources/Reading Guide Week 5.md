# CS 102 · Reading Guide, Week 5
## Shortest Paths

---

## Required

**CLRS, 4th ed. — §20.4, §20.5** (topological sort, strongly connected components)
**CLRS, 4th ed. — Chapter 22, §22.1–22.3** (Bellman–Ford, DAG shortest paths, Dijkstra)
**CLRS, 4th ed. — §22.4** (difference constraints) — short, and the best answer to "when is a weight
ever negative?"

Skip §22.5 (proofs of the relaxation properties) on a first pass. Come back to it once the algorithms
are familiar; it collects the lemmas the other three sections use.

Also useful:

- **Sedgewick & Wayne §4.4** — weighted digraphs and shortest paths, with the clearest diagrams of
  Dijkstra's frontier anywhere.
- **Skiena §8** — good on which algorithm to pick, which is Part E of the problem set.

**This is a heavy reading week and MIDTERM 1 is in it.** If you must triage: read §22.1's introduction
(relaxation) and §22.3 (Dijkstra) properly, skim §22.2, and come back to §20.5 after the exam.

---

## Read §22.1's Preamble First

Chapter 22 opens with several pages before the first algorithm — optimal substructure, negative
weights, cycles, the representation of shortest-path trees, and relaxation. **This preamble is the
chapter.** All three algorithms are the same `RELAX` procedure in different orders, and if you read
the preamble properly the algorithms take twenty minutes each.

The specific thing to extract is the **path-relaxation property**: if the edges of a shortest path are
relaxed *in order*, with anything at all interleaved, the final distance is correct. Every algorithm
in the chapter is a different scheme for guaranteeing that.

---

## How to Read It

**§20.4 (topological sort, 4 pages).** Very short. CLRS gives only the DFS finish-time method; Kahn's
in-degree algorithm is Exercise 20.4-5 and is worth doing, because it is the one that detects cycles
usefully and does not recurse.

**§20.5 (SCC, 8 pages).** Kosaraju's algorithm, in three lines, with a page and a half of proof. Read
the algorithm and the **statement** of Lemma 20.13 and Theorem 20.16; the full proof is worth a second
pass but not a first one. **The idea to take away is the condensation** — contract each SCC and any
digraph becomes a DAG.

**§22.1 (Bellman–Ford, 4 pages).** Note that CLRS presents it before Dijkstra, which is the right
order: it is simpler and it needs no assumptions. The proof of Theorem 22.4 is the induction on edge
counts from Lecture 18 §1.

**§22.2 (DAG shortest paths, 3 pages).** The shortest section in the chapter and the easiest
algorithm in it.

**§22.3 (Dijkstra, 8 pages).** The proof of Theorem 22.6 is the one in Lecture 17 §2. **Find the step
that uses non-negativity** — it is one inequality, and PS 5 C4 asks you to name it.

**§22.4 (difference constraints, 6 pages).** A system of inequalities $x_j - x_i \le b_k$ is a
shortest-path problem in disguise, and it is feasible exactly when a constraint graph has no negative
cycle. Read it; it is the answer to the question everybody asks about negative weights.

---

## Guiding Questions

Three of these are on MIDTERM 2.

1. §22.1: state the path-relaxation property. Then explain, in one sentence each, how DAG-SSSP,
   Dijkstra, and Bellman–Ford each guarantee it.

2. §22.3, Theorem 22.6: identify the **single inequality** that requires non-negative weights. What
   is the concrete counterexample if it fails?

3. §22.2: DAG shortest paths allows negative weights and is the fastest algorithm in the chapter.
   Why is that not a contradiction of the general difficulty of negative weights?

4. Longest path on a DAG is easy; longest **simple** path on a general graph is NP-complete (Week 12).
   Exactly what breaks when you drop acyclicity?

5. §22.1: Bellman–Ford runs $V-1$ rounds. What property of the *graph* actually determines the number
   of rounds needed? (Measure it — PS 5 D2.)

6. §20.5: why does the second DFS in Kosaraju's algorithm run on the **transpose**? What would go
   wrong on the original graph?

7. Dijkstra with a binary heap is $O((V+E)\log V)$ and with an array is $\Theta(V^2)$. For which
   graphs is the array *better*? Give the crossover in terms of $E$ and $V$.

---

## Common Misreadings

**"Dijkstra fails on negative weights, so it will crash or loop."** It does neither. It returns a
plausible wrong number, on about 2.3% of random negative-weight graphs — and the standard three-vertex
counterexample does not even break the lazy-deletion implementation most people write. See PS 5 C.

**"Negative edges and negative cycles are the same problem."** They are not. Negative *edges* leave
shortest paths well defined and are handled by Bellman–Ford. Negative *cycles* mean no shortest path
exists, and no algorithm can return one.

**"Bellman–Ford is $O(VE)$, so it is hopeless."** With the three-line early exit it uses a number of
rounds equal to the graph's hop-diameter — measured at **11–14 rounds** on random graphs where $V-1$
is up to 19,999. The bound is a worst case that ordinary input does not approach.

**"The $V-1$ bound is a property of the graph."** It is a worst case over **edge orderings**. The same
path graph converges in 49 rounds or 2, depending only on the order the edges appear in your list.

**"A\* is faster than Dijkstra."** A\* is Dijkstra with a modified priority. It is faster *when the
heuristic is informative*, correct *only when the heuristic is admissible*, and reduces to Dijkstra
exactly when $h \equiv 0$. Lab 5 shows it silently returning routes 75% too long when the cost model
changes underneath an unchanged heuristic.

**"Topological order is unique."** Almost never. A DAG typically has many valid orders, and the DFS
and Kahn methods usually produce different ones. Both are correct.

---

## If You Have Extra Time

**Johnson's algorithm** (CLRS §22.3 exercises and §23). All-pairs shortest paths on a *sparse* graph
with negative edges, in $O(V^2\log V + VE)$ — beating Floyd–Warshall's $\Theta(V^3)$. It works by
running Bellman–Ford once to compute a **reweighting** that makes every edge non-negative without
changing which paths are shortest, then running Dijkstra $V$ times. It is the most elegant use of both
algorithms together and it makes Week 8's Floyd–Warshall look like the blunt instrument it is.

**Bidirectional Dijkstra.** Search from both ends. The stopping condition is *not* "the frontiers
touch" — that is the classic bug — and working out the correct one is a genuinely good exercise.

**Contraction hierarchies.** How real route planners answer continental queries in microseconds. A\*
is the last algorithm in this lecture that a production planner would recognise; the modern ones
preprocess. Skiena and the OSRM documentation are good entry points.

---

*CS 102 · Week 5 · Reading Guide · © CSE Department*
