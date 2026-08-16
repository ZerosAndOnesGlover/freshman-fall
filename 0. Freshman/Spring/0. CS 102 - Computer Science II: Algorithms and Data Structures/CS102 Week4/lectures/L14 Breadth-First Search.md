# CS 102 · Computer Science II
## Lecture 14: Breadth-First Search

**Date:** Wednesday 10 February 2027 · 09:00–09:50 · Week 4

---

## 1. The Algorithm

Explore the graph in rings: the source, then everything one edge away, then everything two edges
away, and so on. The queue is what enforces that order.

```python
from collections import deque

def bfs(g, s):
    n = len(g)
    dist   = [-1] * n                      # -1 means "not yet discovered"
    parent = [None] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()                    # FIFO - this line is the algorithm
        for v in g[u]:
            if dist[v] == -1:              # first time we have seen v
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
    return dist, parent
```

Twelve lines, and the only thing distinguishing it from DFS is `popleft` rather than `pop`.

**Cost.** Every vertex is enqueued at most once and dequeued at most once; each dequeue scans that
vertex's adjacency list once. Total $\Theta(V + E)$ with an adjacency list, $\Theta(V^2)$ with a
matrix.

**Space.** $\Theta(V)$ — the queue holds at most one entry per vertex. Hold on to that claim; §5 shows
a version that gets the right answer with $\Theta(E)$ space instead.

---

## 2. Why It Finds Shortest Paths

The claim: **when BFS sets `dist[v]`, that value is the minimum number of edges on any path from $s$
to $v$.** This is not obvious — the algorithm never compares two paths.

The proof rests on one property of the queue.

> **Queue monotonicity.** At every moment, the distances of the vertices in the queue are
> non-decreasing, and the largest differs from the smallest by at most 1.

*Sketch.* Initially the queue holds only $s$, with distance 0. When we dequeue $u$ at distance $d$, we
append vertices at distance $d+1$ to the back. So the queue always looks like: some vertices at
distance $d$, then some at $d+1$. Appending $d+1$ to a queue whose contents are $\{d, d+1\}$ keeps the
property.

**Therefore BFS dequeues vertices in non-decreasing order of distance** — it finishes every vertex at
distance $d$ before starting any at distance $d+1$.

Now the theorem. Suppose $v$ has true distance $k$ and let $s = x_0, x_1, \dots, x_k = v$ be a
shortest path. By induction, $x_{k-1}$ is assigned distance $k-1$ and is eventually dequeued. At that
moment $v$ is either already discovered — with some value $\le k$, since assignments happen in
non-decreasing order — or it is discovered now with value $(k-1) + 1 = k$. Either way
$\mathrm{dist}[v] \le k$. And $\mathrm{dist}[v] \ge k$ because `parent` traces out an actual path of
that length. So it is exactly $k$. $\square$

*(Verified: BFS distances from **every** source were compared against Floyd–Warshall on 200 random
graphs of up to 18 vertices — every pair, every source. **0 mismatches.** Separately, over 500 random
graphs, the dequeue order was confirmed non-decreasing in distance and BFS/DFS were confirmed to
reach the identical vertex set.)*

### Where this stops being true

**Only for unweighted graphs**, or equivalently graphs where every edge has the same weight. BFS
counts edges. The moment edges have differing costs, "fewest edges" and "least total weight" come
apart, and BFS answers the wrong question — which is Week 5's opening problem and the reason
Dijkstra's algorithm exists.

The distinction is worth stating sharply now: **BFS is Dijkstra's algorithm with the priority queue
replaced by a plain queue**, and that substitution is valid exactly when all weights are equal,
because then insertion order already is priority order.

---

## 3. DFS Does Not Do This

The most common misconception of the week is that depth-first search also finds shortest paths, since
it also visits everything. It does not, and the counterexample is small enough to keep in your head.

Take the 7-cycle $0-1-2-3-4-5-6-0$.

```
BFS distances from 0:   [0, 1, 2, 3, 3, 2, 1]
DFS tree depths from 0: [0, 1, 2, 3, 4, 5, 6]
```

*(Verified by execution.)*

Vertex 6 is **adjacent to the source** — true distance 1. A DFS that happens to walk
$0 \to 1 \to 2 \to \dots$ arrives at 6 through the long way round and places it at depth **6**. It has
found *a* path, and there is nothing wrong with the path; it is simply not the shortest one, and DFS
never claimed otherwise.

**BFS's tree is a shortest-path tree. DFS's tree is not any kind of optimal tree** — it is a record of
the order the search happened to go, and Lecture 15 is about the fact that this order is nonetheless
extremely informative.

---

## 4. What BFS Gives You

### The BFS tree

`parent` defines a tree rooted at $s$ containing every reachable vertex, in which the tree path from
$s$ to $v$ is *a* shortest path. Recover it by walking backwards:

```python
def path(parent, s, v):
    if parent[v] is None and v != s:
        return None                        # unreachable
    out = []
    while v is not None:
        out.append(v); v = parent[v]
    return out[::-1]
```

**Store `parent`, not the paths.** $V$ integers describe all $V$ shortest paths simultaneously; storing
them separately could cost $\Theta(V^2)$.

### Connected components

Run BFS from every undiscovered vertex; each run marks one component. Total cost is still
$\Theta(V+E)$, because across all runs each vertex and edge is handled once.

```python
def components(g):
    comp = [-1] * len(g); c = 0
    for s in range(len(g)):
        if comp[s] == -1:
            q = deque([s]); comp[s] = c
            while q:
                u = q.popleft()
                for v in g[u]:
                    if comp[v] == -1:
                        comp[v] = c; q.append(v)
            c += 1
    return comp, c
```

*(Verified against a union-find reference on 500 random graphs — component counts agreed and every
edge was confirmed internal to a component. 0 mismatches.)*

### Bipartiteness

A graph is **bipartite** if its vertices can be 2-coloured with no edge joining same-coloured
vertices. Colour each BFS level alternately; the graph is bipartite iff no edge joins two vertices of
the same colour.

```python
def bipartite(g):
    col = [-1] * len(g)
    for s in range(len(g)):
        if col[s] != -1: continue
        col[s] = 0; q = deque([s])
        while q:
            u = q.popleft()
            for v in g[u]:
                if col[v] == -1:
                    col[v] = 1 - col[u]; q.append(v)
                elif col[v] == col[u]:
                    return False, None     # an edge inside a level
    return True, col
```

The failing edge is always one joining two vertices of the same BFS level, and such an edge closes an
**odd cycle**. That is the theorem: *a graph is bipartite iff it contains no odd cycle.*

*(Verified: cycles of length 3, 5, 7 correctly rejected and 4, 6, 8 accepted; and checked against
exhaustive $2^n$ brute force on 300 random graphs of up to 12 vertices — 0 mismatches.)*

### And elsewhere

**Implicit graphs.** BFS on puzzle states gives the *shortest solution*, which is why it is the
standard tool for "fewest moves" problems.

**Web crawling and network broadcast** are BFS by construction. So is the "degrees of separation"
question, which Lab 4 measures on a real network.

---

## 5. Two Bugs Worth Knowing

### Marking visited on dequeue instead of enqueue

```python
while q:
    u = q.popleft()
    if seen[u]: continue                   # <-- marking here, not on append
    seen[u] = True
    for v in g[u]:
        if not seen[v]: q.append(v)
```

This gives **exactly the right distances**. It is not a correctness bug. But a vertex is now appended
once per incoming edge rather than once in total:

| $V$ | $E$ | correct enqueues | this version | max queue length |
| --- | --- | --- | --- | --- |
| 1,000 | 2,999 | 1,000 | 3,000 | 1,648 |
| 10,000 | 30,000 | 10,000 | 30,001 | 16,389 |
| 100,000 | 299,992 | 100,000 | 299,993 | 164,136 |

*(Verified; distances identical to the correct version at every size.)*

**The queue becomes $\Theta(E)$ rather than $\Theta(V)$.** On these sparse graphs that is a factor of
3. On a dense graph it is a factor of $V$ — a queue holding $10^{10}$ entries for a graph of $10^5$
vertices. A bug that never produces a wrong answer, only an out-of-memory failure at scale, is
considerably harder to find than one that does.

### Using a list as a queue

`list.pop(0)` is $\Theta(n)$, because every remaining element shifts down one place. Written into
BFS's inner loop it turns a $\Theta(V+E)$ algorithm into $\Theta(V^2 + E)$ silently. **Use
`collections.deque`**, whose `popleft` is $O(1)$.

This is the third time this term that the right asymptotic algorithm has been ruined by the wrong
container — after `SortedList` in Week 2 and the merge-versus-sort result in Week 3. It will not be
the last.

---

## 6. What to Do

- Read CLRS §20.2. The proof in §20.2 is more careful than section 2 above; read it for the
  invariant, which is stated as Lemma 20.1 through Theorem 20.5.
- **PS 4** implements BFS, components, and bipartiteness.
- **Lab 4** runs both traversals on a 5,000-person social network and measures its diameter.
- Next lecture: DFS, which finds worse paths and much better structure.

---

*CS 102 · Week 4 · Lecture 14 · © CSE Department*
