# CS 102 · Computer Science II
## Lecture 17: Dijkstra's Algorithm

*“What is the shortest way to travel from Rotterdam to Groningen, in general: from given city to given city. It is the algorithm for the shortest path, which I designed in about twenty minutes.”* — Edsger W. Dijkstra, interview with Philip L. Frana (2001), *Communications of the ACM* 53(8) (2010)

**Date:** Wednesday 24 February 2027 · 09:00–09:50 · Week 5

**Reading:** CLRS §22.3

**Coursework:** 📝 **PS 4** due Fri 26 Feb 17:00 · 📝 **PS 5** released Fri 26 Feb 10:00, due Fri 5 Mar 17:00 · 📊 **Quiz 6** Mon 1 Mar 09:00–09:15 · 📘 **Midterm 1** Mon 1 Mar 18:00–19:15 · 🔬 **Lab 5** Tue 2 Mar 15:00–16:50

---

## 1. BFS With a Different Collection

Lecture 13 gave a traversal skeleton and said that changing the collection changes the algorithm.
Here is the change.

```python
def dijkstra(adj, s):
    n = len(adj)
    dist = [INF] * n; dist[s] = 0
    done = [False] * n
    pq = [(0, s)]                              # priority queue, not a FIFO queue
    while pq:
        d, u = heapq.heappop(pq)               # nearest unfinalised vertex
        if done[u]: continue                   # stale entry - lazy deletion, Week 3 L12
        done[u] = True
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

**That is BFS with `deque` replaced by `heapq`.** Where BFS takes the vertex that has been waiting
longest, Dijkstra takes the vertex that is *nearest*. Everything else — the relaxation, the visited
test, the parent array — is unchanged.

The `if done[u]: continue` line is the lazy-deletion priority queue from Week 3 Lecture 12 §3.
Instead of a `decrease_key`, we push a duplicate entry with the better priority and discard the stale
one when it surfaces. That decision has a consequence in §4 that almost nobody expects.

---

## 2. Why It Works, and What It Needs

Dijkstra is **greedy**: at each step it takes the nearest unfinalised vertex and declares its distance
final, never to be revisited. That is a strong claim, and it needs justification.

> **Theorem.** If all edge weights are non-negative, then when Dijkstra pops $u$, $\mathrm{dist}[u]$
> equals the true shortest distance to $u$.

*Proof.* Suppose not, and let $u$ be the first vertex popped with $\mathrm{dist}[u] > \delta(s,u)$.
Consider a true shortest path $s \rightsquigarrow u$, and let $y$ be the **first vertex on it that is
not yet finalised** — $y$ exists, since $u$ itself is not finalised, and $y \ne s$ since $s$ was
finalised first with the correct value 0. Let $x$ be $y$'s predecessor on that path, so $x$ *is*
finalised and, by the choice of $u$ as the first error, $\mathrm{dist}[x] = \delta(s,x)$.

When $x$ was finalised we relaxed the edge $(x,y)$, so

$$\mathrm{dist}[y] \;\le\; \delta(s,x) + w(x,y) \;=\; \delta(s,y)$$

using optimal substructure for the last equality. Now, $y$ lies on a shortest path to $u$, so
$\delta(s,y) \le \delta(s,u)$ — **and this step is where non-negativity is used**: the rest of the
path from $y$ to $u$ has non-negative length. Combining,

$$\mathrm{dist}[y] \le \delta(s,y) \le \delta(s,u) < \mathrm{dist}[u]$$

So $y$ has a strictly smaller key than $u$ and would have been popped first — contradicting that we
popped $u$. $\square$

**Mark the one line that uses the hypothesis.** $\delta(s,y) \le \delta(s,u)$ says that a prefix of a
shortest path is no longer than the whole. With a negative edge later on, that is false, and the proof
— and the algorithm — collapses.

*(Verified: over 4,071 (graph, source) pairs on random non-negative graphs, Dijkstra agreed with
Bellman-Ford exactly. 0 mismatches.)*

---

## 3. Complexity

Each vertex is finalised once, so each adjacency list is scanned once: $\Theta(E)$ relaxations. Each
successful relaxation pushes, so the heap holds at most $O(E)$ entries and every push and pop costs
$O(\log E)$.

$$O((V + E)\log V)$$

using $\log E \le \log V^2 = 2\log V$. With a **Fibonacci heap** and a true `decrease_key` it is
$O(E + V\log V)$, which is asymptotically better and, as Week 3 Lecture 12 noted, almost always slower
in practice.

Measured, against the alternative of scanning for the minimum ($\Theta(V^2 + E)$), from Week 3:

| $V$ | $E$ | binary heap | linear scan | speedup |
| --- | --- | --- | --- | --- |
| 1,000 | 5,000 | 3.2 ms | 49.5 ms | 15× |
| 5,000 | 25,000 | 14.2 ms | 1,010.6 ms | 71× |
| 20,000 | 100,000 | 113.6 ms | 16,175.2 ms | **142×** |

> **The heap is right for sparse graphs, which is to say almost all of them.** On a **dense** graph
> with $E \approx V^2$, $O((V+E)\log V) = O(V^2\log V)$ is *worse* than the array's $\Theta(V^2)$, and
> the simple version wins. "Use a heap for Dijkstra" is a statement about your graph, not a law.

---

## 4. What Happens With Negative Weights

Everyone is told Dijkstra fails on negative edges. Far fewer people have seen it fail, and the details
are more interesting than the slogan.

### It is not reliably wrong

*(Verified: of 1,632 random graphs containing negative edges but **no** negative cycle, Dijkstra
returned a wrong answer on **38** — just **2.3%**.)*

**A bug that manifests 2.3% of the time is worse than one that manifests always.** Your tests pass,
your code ships, and the failure arrives on someone else's data.

### The textbook counterexample does not break the code you just wrote

The standard three-vertex example is $0 \to 1$ with weight $-1$, $0 \to 2$ with weight $-2$, and
$1 \to 2$ with weight $-2$. True distances are $[0, -1, -3]$; textbook Dijkstra returns $[0, -1, -2]$.

*(Verified: this is the **smallest** counterexample for the textbook algorithm — found by exhaustive
search over all digraphs on $V \le 3$ with weights in $\{-2,-1,1,2\}$.)*

**Run it through the implementation in §1 and it gets the right answer.** The reason is a subtlety in
the lazy-deletion version:

```python
for v, w in adj[u]:
    if d + w < dist[v]:                    # note: no "and not done[v]" here
        dist[v] = d + w                    # ...so a finalised v still gets relabelled
        heapq.heappush(pq, (dist[v], v))
```

The textbook algorithm never relaxes into a finalised vertex. The lazy version has no such test — it
happily *relabels* `dist[v]` after $v$ is done; it only refuses to **re-expand** $v$. So a late
correction still lands in the answer array, provided nothing downstream depended on it.

To break the lazy version the correction must need to **propagate further**:

```
0 -> 1  weight  1
0 -> 2  weight  2
2 -> 1  weight -2
1 -> 3  weight  1
```

| | dist |
| --- | --- |
| Dijkstra, lazy (§1) | `[0, 0, 2, 2]` |
| Dijkstra, textbook | `[0, 1, 2, 2]` |
| **correct** | `[0, 0, 2, 1]` |

*(Verified. The true route to 3 is $0 \to 2 \to 1 \to 3 = 2 - 2 + 1 = 1$. Vertex 1 is finalised at
cost 1 and relaxes $1 \to 3$ to give `dist[3] = 2`; the later correction of `dist[1]` to 0 arrives
after 1 has been expanded, so it never reaches 3.)*

*(Verified by exhaustive search: the smallest failing case for the lazy version needs **4** vertices,
where the textbook version fails at **3**.)*

**The lazy implementation is strictly more forgiving than the algorithm in the textbook** — which
means it is strictly better at hiding the bug. It is still wrong, and it is wrong in a way that
depends on graph structure rather than on anything you can see in the code.

> The lesson is not about negative weights. It is that **two implementations described by the same
> pseudocode can have different failure sets**, and that testing one tells you less than you think
> about the other.

---

## 5. Variants

**Early exit for a single target.** If you only want $\mathrm{dist}(s,t)$, stop when $t$ is popped —
it is final at that moment. On the road network in Lab 5 this alone is a large saving, because the
search stops as soon as it reaches the destination rather than covering the map.

**A\*.** Push with priority $g(u) + h(u)$, where $g$ is the distance so far and $h$ is a *guess* at the
remaining distance. If $h$ never overestimates — if it is **admissible** — A\* returns the true
shortest path while expanding far fewer vertices. Setting $h = 0$ recovers Dijkstra exactly.

Measured on Lab 5's road network, 10 source–target pairs:

| | vertices expanded |
| --- | --- |
| Dijkstra with early exit | 18,550 |
| **A\* with a straight-line heuristic** | **2,530** |

**7.3× fewer expansions, with identical distances on all 200 test queries.** Lab 5 builds this, and
then breaks it: change the cost model from distance to *travel time* and the straight-line heuristic
stops being admissible, at which point A\* becomes 74.9% wrong on some queries. The fix is
principled and the lab makes you find it.

**Bidirectional search.** Run Dijkstra from both ends and stop when the frontiers meet. Roughly
square-roots the explored area. The stopping condition is subtler than it looks and is a classic
source of off-by-one bugs.

**Multiple sources.** Push all of them with distance 0. The result is, for every vertex, the distance
to the *nearest* source — one run, not $k$.

---

## 6. What to Do

- Read CLRS §22.3. The proof there is the one in §2, stated more carefully.
- **PS 5** implements Dijkstra, verifies it against Bellman-Ford, and asks you to find the
  4-vertex counterexample from §4 yourself.
- **Lab 5** is route planning: Dijkstra, then A\*, then the cost-model change that breaks it.
- Next lecture: Bellman-Ford, which drops the non-negativity assumption and pays $O(VE)$ for it —
  except that in practice it usually does not.

---

*CS 102 · Week 5 · Lecture 17 · © CSE Department*
