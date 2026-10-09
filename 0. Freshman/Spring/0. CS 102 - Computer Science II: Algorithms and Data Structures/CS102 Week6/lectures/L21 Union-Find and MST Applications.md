# CS 102 · Computer Science II
## Lecture 21: Union-Find, and What MSTs Are For

*“The applications of knowledge, especially mathematics, reveal the unity of all knowledge. In a new situation almost anything and everything you ever learned might be applicable, and the artificial divisions seem to vanish.”* — Richard Hamming, *Methods of Mathematics Applied to Calculus, Probability, and Statistics* (1985)

**Date:** Friday 5 March 2027 · 09:00–09:50 · Week 6

**Reading:** CLRS §19.1–19.3 (§19.4: the statement of the bound only)

**Coursework:** 📝 **PS 5** due today 17:00 · 📝 **PS 6** released today 10:00, due Fri 12 Mar 17:00 · 📊 **Quiz 7** Mon 8 Mar 09:00–09:15 · 📋 **Project 1** released Mon 8 Mar 09:00, due Fri 26 Mar 17:00 · 🔬 **Lab 6** Tue 9 Mar 15:00–16:50

---

## 1. The Problem

Kruskal needs one question answered $E$ times: **are these two vertices already connected?** And it
needs to record $V-1$ merges.

That is the **disjoint-set union** ADT — also called union-find:

| operation | meaning |
| --- | --- |
| `make_set(x)` | $x$ starts alone |
| `find(x)` | return a canonical representative of $x$'s set |
| `union(a, b)` | merge the two sets |

`find(a) == find(b)` tests connectivity. The representative is arbitrary but must be *consistent*:
two elements are in the same set exactly when their `find` results agree.

The obvious implementation is a forest: each element points at a parent, and `find` walks to the root.

```python
def find(x):
    while p[x] != x: x = p[x]
    return x

def union(a, b):
    p[find(a)] = find(b)
```

**This is correct and it is catastrophically slow**, because nothing stops the trees becoming paths.

---

## 2. Two Optimisations

### Union by rank

Keep an upper bound on each tree's height and **attach the shorter tree under the taller**.

```python
def union(a, b):
    a, b = find(a), find(b)
    if a == b: return False
    if r[a] < r[b]: a, b = b, a          # a is the taller
    p[b] = a
    if r[a] == r[b]: r[a] += 1           # only a tie increases the rank
    return True
```

Alone, this bounds every tree's height at $\log_2 n$: a tree of rank $k$ has at least $2^k$ elements,
because rank only increases when two equal ranks merge.

### Path compression

On the way back from a `find`, point every node visited **directly at the root**.

```python
def find(x):
    root = x
    while p[root] != root: root = p[root]
    while p[x] != root: p[x], x = root, p[x]      # second pass: reattach
    return root
```

It costs nothing extra asymptotically — you already walked the path — and it means the next `find` on
any of those nodes is $O(1)$.

### Measured

Steps taken following parent pointers, over $n$ random unions followed by one `find` per element:

| $n$ | neither | union by rank | path compression | **both** |
| --- | --- | --- | --- | --- |
| 1,000 | 81,403 | 3,479 | 4,240 | **2,450** |
| 5,000 | 1,978,844 | 18,040 | 22,987 | **12,243** |
| 20,000 | 30,823,531 | 72,486 | 99,855 | **49,232** |
| 100,000 | 779,553,223 | 379,496 | 542,521 | **246,855** |

*(Verified by instrumented execution.)*

**The naive column is quadratic** — 100× the input gives roughly $10^4$× the work. Either optimisation
alone brings it to near-linear; together they are **3,158× faster than neither** at $n = 100{,}000$,
and the gap widens with $n$.

### The adversarial case

Random input is kind. Build a deliberate chain — union in an order that always attaches the current
root beneath a new element — and then `find` every node:

| $n$ | naive | both optimisations |
| --- | --- | --- |
| 1,000 | 499,500 | **999** |
| 5,000 | 12,497,500 | **4,999** |
| 20,000 | 199,990,000 | **19,999** |

*(Verified. The naive figures are exactly $n(n-1)/2$ — the sum of the path lengths in a chain — and the
optimised ones are exactly $n-1$.)*

**Every `find` costs one step**, because the first `find` flattened the tree for everyone after it.
This is amortisation in its purest form: one expensive operation pays for all the cheap ones that
follow.

---

## 3. The Bound

With both optimisations, $m$ operations on $n$ elements cost

$$O(m\,\alpha(n))$$

where $\alpha$ is the **inverse Ackermann function**. Measured, in steps per operation:

| $n$ | steps/op | $\log_2 n$ |
| --- | --- | --- |
| $10^3$ | 1.225 | 10.0 |
| $10^4$ | 1.222 | 13.3 |
| $10^5$ | 1.234 | 16.6 |
| $10^6$ | 1.235 | 19.9 |

**Flat at about 1.23 across three orders of magnitude**, while $\log_2 n$ doubles. That is what
"effectively constant" looks like when you measure it.

### How small is $\alpha$?

$\alpha(n)$ is the least $k$ such that $A_k(1) \ge n$, where $A_k$ is the Ackermann hierarchy:

| $k$ | $A_k(1)$ |
| --- | --- |
| 0 | 2 |
| 1 | 3 |
| 2 | 5 |
| 3 | **13** |
| 4 | $2^{2^{2^{16}}} - 3$ |

*(The small values verified by direct computation.)*

$A_4(1)$ is a power tower vastly exceeding the number of atoms in the observable universe. **So
$\alpha(n) \le 4$ for any $n$ you could store**, and in practice the bound is a constant.

But be precise about what has been proved: **$\alpha$ is not constant — it grows, unboundedly, just
extraordinarily slowly.** And $O(m\,\alpha(n))$ is **tight**; Tarjan proved a matching lower bound for
this class of algorithms, so this is not merely the best analysis anyone has managed.

> **Connection to Week 3.** The linear-time `BUILD-HEAP` proof worked because the expensive operations
> were rare and a series converged. This is the same shape of argument in a harder setting: no
> individual `find` is $O(1)$ — the first one on a long chain is $\Theta(n)$ — but the *total* over any
> sequence is near-linear, because each expensive call flattens the structure and cannot be repeated.
> **An amortised bound is a statement about sequences, not about calls.**

---

## 4. Union-Find Beyond Kruskal

The structure is more broadly useful than the algorithm that motivated it:

- **Connected components** in a graph given as a stream of edges, with no traversal.
- **Dynamic connectivity** under edge insertion — with the significant caveat that union-find handles
  insertions only; **deletion is much harder** and needs quite different machinery.
- **Cycle detection** while building a graph: an edge whose endpoints already share a root closes a
  cycle.
- **Image segmentation and percolation**, where regions merge as a threshold moves.
- **Type unification** in a compiler — the classic Hindley–Milner inference algorithm is union-find
  over type variables.

The one thing it does **not** do is tell you *how* two elements are connected. It answers "same
component?" and nothing else. If you need a path, you need a traversal.

---

## 5. What MSTs Are For

### Infrastructure

The original problem: connect $n$ locations with minimum total cable, pipe, or road. Borůvka's 1926
paper was about electrifying Moravia. Lab 6 is this, on a campus.

### Bottleneck: the minimax property

From Lecture 19 §5, the MST path between any two vertices minimises the **maximum** edge on the route.
So **the heaviest edge in the MST is the smallest possible "worst link"** of any spanning structure —
which is the answer to "what is the shortest cable reel that could possibly suffice?"

### Clustering

This is the application worth knowing, because it is not obvious.

> **To split $n$ points into $k$ clusters, build the MST and delete the $k-1$ heaviest edges.**

The result is exactly **single-linkage agglomerative clustering**, obtained in $O(E\log E)$ instead of
by running the clustering algorithm. And it is *optimal* for a precise objective: it maximises the
minimum distance between different clusters.

Measured on Lab 6's campus — 400 buildings in 5 well-separated groups:

| $k$ | cluster sizes | smallest deleted edge |
| --- | --- | --- |
| 2 | 320, 80 | 27.476 |
| 3 | 240, 80, 80 | 26.522 |
| 4 | 160, 80, 80, 80 | 25.311 |
| **5** | **80, 80, 80, 80, 80** | **23.725** |
| 6 | 80, 80, 80, 80, 79, 1 | **5.227** |

*(Verified. At $k=5$ the recovered clusters match the planted ones exactly — 100% agreement by
pair-counting.)*

**Look at the last column.** The four heaviest MST edges are 23.7 to 27.5; the fifth is **5.227** — a
4.5× drop. **The MST's edge weights tell you how many clusters there are**, without being told. That
gap is the elbow, and looking for it is the standard way to choose $k$.

### The failure mode

Single-linkage **chains**: two well-separated clusters joined by a thin bridge of points are merged,
because the algorithm only ever looks at the single shortest link between groups.

*(Verified: on the same 400 buildings with the clusters made to overlap — standard deviation 10 rather
than 3 — $k=5$ gives cluster sizes 237, 159, 2, 1, 1 and only **67.1%** agreement with the planted
groups, against 100% when separated. The algorithm peels off individual outliers instead of finding
groups.)*

**Both results come from the same property.** Sensitivity to the single shortest link is what makes
the method optimal for the minimum-separation objective, and what makes it fragile when a few points
bridge a gap. Lab 6 Part D has you produce both.

### And approximation

A minimum spanning tree gives a **2-approximation to the travelling salesman problem** on a metric
graph: walk the MST twice and shortcut repeats. Week 12 proves the factor of 2.

---

## 6. Where This Leaves the Graph Weeks

Three weeks, one skeleton. A traversal removes a vertex from a collection and adds its neighbours:

| collection | algorithm | optimises |
| --- | --- | --- |
| queue | BFS | fewest edges |
| stack | DFS | structure, ordering |
| priority queue, key = distance from **source** | Dijkstra | least total weight of a path |
| priority queue, key = distance from **tree** | Prim | least total weight of a tree |

**Prim and Dijkstra differ in one expression.** Being able to say which and why is the single best test
of whether the last three weeks have landed.

**Week 7 changes subject** to dynamic programming, and the bridge is already built: Bellman–Ford is a
DP, and Week 7 opens by saying so.

---

## 7. What to Do

- Read CLRS §19.1–19.3 (disjoint sets) and §21.2. §19.4's proof of the $\alpha$ bound is hard and is
  **not examinable**; read its statement.
- **PS 6** implements all four union-find variants and measures them; **Lab 6** builds the clustering.
- **Lab 6** is the campus cable layout, including the clustering and its failure mode.
- **Quiz 6 covers Week 5.**

---

*CS 102 · Week 6 · Lecture 21 · © CSE Department*
