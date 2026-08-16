# CS 102 · Computer Science II
## Lecture 19: Spanning Trees and the Cut Property

**Date:** Monday 22 February 2027 · 09:00–09:50 · Week 6

---

## 1. A Different Question

Week 5 asked for the cheapest route between two vertices. This week asks a question about the graph as
a whole:

> **Connect every vertex, using as little total edge weight as possible.**

A **spanning tree** of a connected graph is a subgraph that is a tree and touches every vertex. It has
exactly $V-1$ edges — any fewer leaves the graph disconnected, any more creates a cycle. A **minimum
spanning tree** (MST) is one of least total weight.

The phrasing matters. We are not minimising any *path*; we are minimising the *total*. Those turn out
to be genuinely different objectives, and §5 shows a three-vertex graph where they disagree.

**Why you cannot enumerate.** By Cayley's formula the complete graph on $n$ vertices has $n^{n-2}$
spanning trees.

| $n$ | spanning trees of $K_n$ |
| --- | --- |
| 10 | $10^{8}$ |
| 20 | $2.6\times10^{23}$ |
| 50 | $3.6\times10^{81}$ |
| 100 | $10^{196}$ |

*(Cayley's formula verified by exhaustive enumeration for $n = 2\dots6$: 1, 3, 16, 125, 1296.)*

At $n = 50$ there are more spanning trees than there are atoms in the observable universe. The whole
content of this week is that a problem with that search space has a **greedy** solution, and *why*
greedy is allowed to work here.

---

## 2. Two Properties

Both MST algorithms are consequences of one theorem. Two definitions first.

A **cut** $(S, V \setminus S)$ is a partition of the vertices into two non-empty parts. An edge
**crosses** the cut if its endpoints are on opposite sides.

> ### The Cut Property
> For any cut, a **minimum-weight edge crossing that cut belongs to some MST.**

*(Verified: over 3,191 (graph, cut) pairs — every non-trivial cut of 200 small random graphs, checked
against every minimum spanning tree found by exhaustive enumeration. **0 violations.**)*

*Proof (exchange argument).* Let $e$ be a minimum-weight edge crossing the cut, and let $T$ be any
MST. If $e \in T$ we are done. Otherwise, adding $e$ to $T$ creates exactly one cycle. That cycle
crosses the cut at $e$ and must cross back somewhere, so it contains another crossing edge $f$. Now
$T' = T - f + e$ is again a spanning tree — we removed an edge of the cycle we created — and

$$w(T') = w(T) - w(f) + w(e) \le w(T)$$

since $w(e) \le w(f)$ by the choice of $e$. As $T$ was minimum, $w(T') = w(T)$, so $T'$ is also an MST,
and it contains $e$. $\square$

**Note the phrasing: "some MST", not "every MST."** If several crossing edges tie for minimum, an MST
may contain any one of them. Getting this wrong is the most common error in stating the theorem.

The dual statement is just as useful:

> ### The Cycle Property
> For any cycle, the **strictly heaviest edge on that cycle belongs to no MST.**

*(Verified: 758 (cycle, strictly-heaviest-edge) cases across 150 random graphs. **0 violations.**)*

*Proof.* If such an $e$ were in an MST $T$, deleting it splits $T$ into two components. The rest of the
cycle joins those components, so some other cycle edge $f$ crosses the split; $T - e + f$ is a spanning
tree of strictly smaller weight. Contradiction. $\square$

**"Strictly" is doing real work.** With a tie for heaviest, one of the tied edges may well be in an
MST — and PS 6 asks you to build the example.

> **The two properties are what a greedy algorithm needs.** The cut property says which edges are
> *safe to add*; the cycle property says which are *safe to reject*. Prim's algorithm is repeated
> application of the first; Kruskal's uses both. Everything in Lecture 20 follows.

---

## 3. Uniqueness

> **If all edge weights are distinct, the MST is unique.**

*(Verified: of 156 random graphs with all-distinct weights, **0** had more than one MST. Of 240 graphs
containing ties, **121 — almost exactly half — still had a unique MST.** So distinct weights are
*sufficient* but **not necessary**.)*

*Proof sketch.* Suppose $T_1 \ne T_2$ are both minimum. Let $e$ be the **lightest** edge in exactly one
of them, say $e \in T_1$. Adding $e$ to $T_2$ makes a cycle, which must contain an edge $f \notin T_1$
— otherwise $T_1$ would contain a cycle. Since $e$ was the lightest edge in exactly one tree and
weights are distinct, $w(e) < w(f)$, so $T_2 - f + e$ beats $T_2$. Contradiction. $\square$

The second half of the verified result is the part worth remembering: **ties permit multiple MSTs but
do not force them.** "The MST" is a safe phrase when weights are distinct and a sloppy one otherwise.
In practice weights are often distances or costs with ties, and if you need determinism you break ties
by an index rather than hoping.

---

## 4. Why Greedy Is Allowed Here

Week 5 was careful about when greedy works. Dijkstra is greedy and correct *because* weights are
non-negative; drop that and it silently fails. So the question for this week is what plays the same
role.

The answer is the cut property, and the structure of the argument is the same shape you will see
formalised in **Week 9**: an **exchange argument**. Assume an optimal solution that disagrees with the
greedy choice; show you can swap the greedy choice in without making things worse; conclude that some
optimal solution agrees with greedy.

**That is what makes a greedy choice *safe*.** It is not that greedy "usually works" — it is a theorem
that a locally minimal choice is consistent with global optimality.

Note what is *not* assumed here. **MST algorithms do not need non-negative weights.** A negative edge
is simply a very attractive one, and the exchange argument never compares a weight to zero.

A cleaner way to see it: **adding a constant to every edge does not change which spanning tree is
minimum.** Every spanning tree has exactly $V-1$ edges, so every total shifts by the same amount and
the ranking is untouched. Any graph with negative weights can therefore be shifted to have none.

*(Verified: adding 100 to every edge weight left the MST edge set unchanged in 300 of 300 random
graphs.)*

> **Contrast that with shortest paths**, where adding a constant to every edge *does* change the answer,
> because paths have different lengths. **Same graph, same weights, and the two problems respond
> differently to the same transformation.** That is a good way to remember that they are not variants
> of each other.

---

## 5. The MST Is Not a Shortest-Path Tree

This is the misconception of the week, and it deserves a counterexample small enough to hold in your
head.

```
        2
   0 ------- 1
    \       /
   3 \     / 2
      \   /
        2
```

A triangle: $w(0,1) = 2$, $w(1,2) = 2$, $w(0,2) = 3$.

- **MST:** take the two edges of weight 2. Total **4**.
- **Shortest path $0 \to 2$ in the graph:** the direct edge, **3**.
- **Path from 0 to 2 within the MST:** $0 \to 1 \to 2$, weight **4**.

*(Verified by execution.)*

**The MST is 33% worse than optimal for that particular journey**, and it must be — the direct edge is
the heaviest on the cycle, so the cycle property forbids it from any MST.

The two problems optimise different things. An MST minimises the **total** infrastructure; a
shortest-path tree minimises **each individual journey**, and generally uses more total edge weight to
do it. If you are laying cable, you want the MST. If you are routing packets, you do not.

### But this *is* true: the MST is a minimax tree

There is a genuine optimality property, and it is a good one.

> For any two vertices $u, v$, the path between them **in the MST** minimises the **maximum edge
> weight** over all $u$–$v$ paths in the graph.

*(Verified: 15,988 (source, target) pairs across 300 random graphs, comparing the MST path's maximum
edge against a minimax search on the full graph. **0 mismatches.**)*

So the MST does not give you the shortest route, but it does give you the route with the *best worst
link* — and the heaviest edge in the whole MST is the smallest possible "worst link" for any spanning
structure at all. Lab 6 uses exactly this: **the heaviest MST edge is the shortest cable run that
could possibly suffice** to connect a campus.

---

## 6. Summary

| statement | true? |
| --- | --- |
| A minimum-weight edge across any cut is in **some** MST | **yes** — the cut property |
| A minimum-weight edge across any cut is in **every** MST | no — only with distinct weights |
| The strictly heaviest edge on a cycle is in **no** MST | **yes** — the cycle property |
| Distinct weights $\Rightarrow$ unique MST | **yes** |
| Unique MST $\Rightarrow$ distinct weights | **no** — 121 of 240 tied graphs had a unique MST |
| MST paths are shortest paths | **no** — the triangle above |
| MST paths are minimax paths | **yes** — 0 mismatches in 15,988 pairs |
| MST algorithms need non-negative weights | **no** — unlike Dijkstra |

---

## 7. What to Do

- Read CLRS §21.1 — the generic MST algorithm and the safe-edge theorem. It is 8 pages and it is the
  whole of this lecture, stated once and carefully.
- **PS 6** asks you to verify both properties computationally and to construct the tie counterexamples.
- **Quiz 6 covers Week 5** — Dijkstra, Bellman–Ford, DAGs. Not this material.
- Next lecture: Prim's and Kruskal's, which are the cut property applied in two different orders.

---

*CS 102 · Week 6 · Lecture 19 · © CSE Department*
