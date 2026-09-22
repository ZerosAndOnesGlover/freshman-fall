# CS 102 · Computer Science II
## Lecture 18: Bellman–Ford, Negative Cycles, and Choosing an Algorithm

**Date:** Friday 26 February 2027 · 09:00–09:50 · Week 5

---

## 1. Giving Up on Being Clever

Dijkstra needs an order — nearest first — and that order is only trustworthy when weights are
non-negative. Bellman–Ford abandons the search for a good order entirely.

```python
def bellman_ford(V, edges, s):
    d = [INF] * V; d[s] = 0; parent = [None] * V
    for _ in range(V - 1):                        # V-1 rounds
        for u, v, w in edges:                     # every edge, every round
            if d[u] != INF and d[u] + w < d[v]:
                d[v] = d[u] + w; parent[v] = u
    for u, v, w in edges:                         # one more round: did anything improve?
        if d[u] != INF and d[u] + w < d[v]:
            return None                           # negative cycle reachable from s
    return d, parent
```

Relax every edge, $V-1$ times. No priority queue, no ordering, no cleverness. **$O(VE)$.**

### Why $V-1$ rounds suffice

A shortest path in a $V$-vertex graph is simple — it has no repeated vertex, since removing a
non-negative cycle never lengthens a path and a negative cycle means there is no shortest path at all.
So it uses **at most $V-1$ edges**.

Now induct on rounds:

> **After round $i$, `d[v]` is correct for every vertex whose shortest path uses at most $i$ edges.**

Round 1 relaxes every edge, so in particular the first edge of every shortest path — correct for paths
of 1 edge. If it holds after round $i$, then round $i+1$ relaxes the $(i{+}1)$-th edge of every
shortest path, whose prefix is already correct by hypothesis and by optimal substructure. Since no
shortest path exceeds $V-1$ edges, $V-1$ rounds finish the job. $\square$

This is exactly the path-relaxation property of Lecture 16 §2, obtained by brute force: **relax
everything enough times and every shortest path gets relaxed in order, whatever order you actually
used.**

### It is a dynamic program

Write $D_i[v]$ for the shortest distance to $v$ using at most $i$ edges:

$$D_i[v] \;=\; \min\Big(D_{i-1}[v],\ \min_{(u,v)\in E}\big(D_{i-1}[u] + w(u,v)\big)\Big)$$

That is a recurrence over subproblems indexed by *edge count*, and the code above is its bottom-up
evaluation with the rows overwritten in place. **Bellman–Ford is the first dynamic program in this
course**, three weeks before Week 7 names the technique. Keep it in mind — Week 7 opens by pointing
back at it.

---

## 2. The Bound Is About Edge Order, Not the Graph

$V-1$ is tight, and the reason is not what most people assume.

Take a path graph $0 \to 1 \to \dots \to (V-1)$, every weight 1, and present the edges to the inner
loop in **reverse** order. Each round advances the frontier by exactly one hop:

| $V$ | rounds used | $V-1$ |
| --- | --- | --- |
| 5 | 4 | 4 |
| 10 | 9 | 9 |
| 20 | 19 | 19 |
| 50 | **49** | 49 |

Now present **the same graph's** edges in forward order:

| $V$ | rounds used |
| --- | --- |
| 5 | 2 |
| 50 | **2** |

*(Verified. The second round does no work; it is the one that detects that nothing changed.)*

**Same graph, same weights — 49 rounds or 2, depending only on the order the edge list happens to be
in.** The $O(VE)$ bound is a worst case over edge orderings, not a property of the graph, and an
algorithm whose cost varies by 25× on an invisible detail of your input file is worth knowing about.

---

## 3. Early Termination, and Why the Bound Overstates the Cost

Add three lines:

```python
for _ in range(V - 1):
    changed = False
    for u, v, w in edges:
        if d[u] != INF and d[u] + w < d[v]:
            d[v] = d[u] + w; changed = True
    if not changed: break                          # nothing improved: we are done
```

If a full round changes nothing, no later round can either, so we stop. This does not improve the
worst case. It transforms the typical case.

*(Verified on random graphs of average degree 6:)*

| $V$ | rounds actually used | $V-1$ | $\log_2 V$ |
| --- | --- | --- | --- |
| 1,000 | **11** | 999 | 10.0 |
| 5,000 | **12** | 4,999 | 12.3 |
| 20,000 | **14** | 19,999 | 14.3 |

**The rounds track $\log_2 V$, not $V$.** The number of rounds needed is the maximum number of *edges*
on any shortest path — the graph's hop-diameter — and on a random graph that is $\Theta(\log V)$. So
the early-exit version runs in $O(E\log V)$ here, the same as Dijkstra.

The wall clock confirms it, and the size of the effect is the point:

| $V$ | $E$ | Dijkstra | Bellman–Ford, early exit | Bellman–Ford, no early exit |
| --- | --- | --- | --- | --- |
| 1,000 | 2,999 | 0.8 ms | 3.1 ms | **310.7 ms** |
| 3,000 | 8,998 | 3.3 ms | 8.9 ms | **2,615.9 ms** |

**Three lines of code turn a 793× penalty into a 3× one**, and the 3× is a constant factor from
scanning an edge list rather than a heap. On a road network — hop-diameter in the hundreds — the gap
would be smaller but the conclusion is the same.

> This is the reverse of Week 3's lesson and worth holding alongside it. There, an algorithm with
> better asymptotics lost in practice. Here, an algorithm with worse asymptotics is *nearly as fast in
> practice* because its worst case almost never occurs. **Neither direction is safe to assume.**

---

## 4. Negative Cycles

Run one extra round. If anything still improves, some shortest path would have used $\ge V$ edges,
which for a simple path is impossible — so a negative cycle is reachable from $s$.

*(Verified: on 600 random digraphs, 152 of which contained a negative cycle reachable from the source,
the extra-round test agreed with brute-force enumeration of all cycles. 0 mismatches.)*

```
0 -> 1 (1),  1 -> 2 (-1),  2 -> 3 (-1),  3 -> 1 (-1)     cycle weight -3   detected
0 -> 1 (1),  1 -> 2 (-1),  2 -> 3 ( 1),  3 -> 1 ( 1)     cycle weight +1   not detected
```

Three points that are examined:

**Only cycles reachable from $s$ are detected.** A negative cycle in a part of the graph you cannot
get to does not affect any distance from $s$, and this algorithm will not report it. To find *all* of
them, add a virtual source with a 0-weight edge to every vertex.

**"Detected" is not "located."** To extract the cycle, note any vertex $v$ that still improved, walk
`parent` back $V$ times to land inside the cycle, then walk round until you return.

**A negative cycle means the question has no answer.** Reporting `None` is correct behaviour, not a
failure. Compare Dijkstra, which returns a plausible-looking wrong number.

### Where negative weights actually come from

Students reasonably ask when a road has negative length. The honest answer is that it does not, and
negative weights arise when the weights are not distances:

- **Currency arbitrage.** Edge $u \to v$ weighted $-\log(\text{rate})$; a path's weight sums to
  $-\log$ of the product of rates, so **a negative cycle is a sequence of trades that ends with more
  money than it started with.** Detecting negative cycles *is* detecting arbitrage.
- **Profit and loss.** Costs positive, rebates negative.
- **Difference constraints.** A system of inequalities $x_j - x_i \le c$ becomes a shortest-path
  problem, and it is feasible exactly when there is no negative cycle. CLRS §22.4.

---

## 5. Choosing

| situation | algorithm | cost | notes |
| --- | --- | --- | --- |
| all weights equal | **BFS** | $\Theta(V+E)$ | no priority queue at all |
| DAG, any weights | **topological order** | $\Theta(V+E)$ | also gives longest paths |
| non-negative, sparse | **Dijkstra + heap** | $O((V+E)\log V)$ | the default |
| non-negative, dense | **Dijkstra + array** | $\Theta(V^2)$ | beats the heap when $E \approx V^2$ |
| negative edges | **Bellman–Ford** | $O(VE)$, often $O(E\log V)$ | add the early exit |
| need to *detect* negative cycles | **Bellman–Ford** | $O(VE)$ | the extra round |
| all pairs, dense | **Floyd–Warshall** | $\Theta(V^3)$ | Week 8 |

**Do not reach for the general algorithm by default.** Each row exploits an assumption, and a correct
choice is worth more than a clever implementation of the wrong one. That judgement is Section D of the
midterm and it is the recurring question of this course.

### The three-line summary

- **BFS counts edges. Dijkstra sums non-negative weights. Bellman–Ford sums anything.**
- **Dijkstra is greedy** — one pass, decisions never revisited, correct because of an ordering
  argument.
- **Bellman–Ford is dynamic programming** — subproblems indexed by edge count, no order needed,
  correct because it eventually tries everything.

Those two are the paradigms of Weeks 7 and 9, and you have now met both before either is named. The
comparison is worth carrying: **greedy needs a proof that the order is safe; DP needs no such proof
and pays for it in time.**

---

## 6. What to Do

- Read CLRS §22.1 (Bellman–Ford) and §22.4 (difference constraints — short, and the best motivation
  for negative weights you will find).
- **PS 5** implements Bellman–Ford with the early exit, measures the rounds actually used, and
  extracts a negative cycle rather than merely reporting one.
- **MIDTERM 1** is this week. This lecture is not on it.
- **Week 6** keeps the greedy paradigm but changes the objective: minimum spanning trees, where the
  cut property plays the role that non-negativity plays here.

---

*CS 102 · Week 5 · Lecture 18 · © CSE Department*
