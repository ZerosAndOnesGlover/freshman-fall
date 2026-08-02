# CS 102 · Quiz 6

**Week 6, Monday, first 15 minutes of lecture · 20 points**
**Covers Week 5** — shortest paths: relaxation, DAGs, Dijkstra, Bellman–Ford. **Not** this week's
material.

Closed book. Every number here is exact.

---

**Q1.** *(3)* Name the algorithm you would use for each, in one word or phrase:

- **(a)** all edges have weight 1;
- **(b)** the graph is a DAG and some weights are negative;
- **(c)** the graph has cycles and some weights are negative.

---

**Q2.** *(4)* For the directed graph

$$0\to1\ (4),\quad 0\to2\ (1),\quad 2\to1\ (2),\quad 1\to3\ (5),\quad 2\to3\ (8),\quad 3\to4\ (3)$$

run Dijkstra from vertex 0. Give the **order in which vertices are finalised**, with the distance at
which each is finalised.

---

**Q3.** *(4)* A directed graph contains the cycle $1 \to 2\ (-2)$, $2 \to 3\ (-2)$, $3 \to 1\ (w)$,
reachable from the source.

- **(a)** For which values of $w$ does Bellman–Ford report a negative cycle?
- **(b)** When it does, what is the correct output of a shortest-path algorithm, and why?

---

**Q4.** *(3)* For the DAG $0\to1\ (3)$, $0\to2\ (2)$, $1\to3\ (4)$, $2\to3\ (1)$, $3\to4\ (2)$,
give the **longest** path length from 0 to 4, and say how you computed it in $\Theta(V+E)$.

---

**Q5.** *(3)* Bellman–Ford runs $V-1$ rounds. On a random graph with $V = 20{,}000$, an implementation
with early termination stopped after **14** rounds.

State what the number of rounds actually measures.

---

**Q6.** *(3)* Dijkstra's correctness proof uses non-negativity in exactly one place.

State the inequality it needs, and what goes wrong without it.

---

*20 points total. Solutions posted after Wednesday's lecture.*

*CS 102 · Week 6 · Quiz 6 · © CSE Department*
