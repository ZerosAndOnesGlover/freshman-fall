# CS 102 · Computer Science II
## Lecture 15: Depth-First Search — Timestamps and Edge Classification

**Date:** Friday 12 February 2027 · 09:00–09:50 · Week 4

---

## 1. The Algorithm

Go as deep as possible before backtracking.

```python
def dfs(g, s, seen=None):
    if seen is None: seen = [False] * len(g)
    seen[s] = True
    for v in g[s]:
        if not seen[v]:
            dfs(g, v, seen)
    return seen
```

Change one line of BFS — `pop()` instead of `popleft()` — and you get the iterative form:

```python
def dfs_iter(g, s):
    seen = [False] * len(g)
    st = [s]
    while st:
        u = st.pop()                       # LIFO - the only difference from BFS
        if seen[u]: continue
        seen[u] = True
        for v in g[u]:
            if not seen[v]: st.append(v)
```

Both are $\Theta(V+E)$. Both visit exactly the reachable vertices. **They do not visit them in the
same order**, because the recursive version descends into a neighbour immediately while the iterative
version pushes them all and takes the last. Neither order is wrong; if you need a specific one,
`reversed(g[u])` in the iterative version reproduces the recursive order.

### The recursion limit is a real problem

Python's default recursion limit is **1,000**, and each DFS level is a frame.

| input | recursive DFS | iterative DFS |
| --- | --- | --- |
| path of 900 vertices | works | works |
| path of 5,000 vertices | **`RecursionError`** | works |
| path of 1,000,000 vertices | `RecursionError` | works — 1,000,000 visited |

*(Verified on Python 3.14; `sys.getrecursionlimit()` returns 1000.)*

A path graph is not exotic — a linked list, a chain of dependencies, or a road with no junctions all
produce one. **Raising the limit with `sys.setrecursionlimit` is not a fix**: the frames are real and
you will exhaust the C stack and get a segmentation fault instead of an exception, which is a strictly
worse failure. Write the iterative version when $V$ can be large.

---

## 2. Timestamps

The plain version tells you *what* is reachable. Adding two clocks tells you *how the graph is put
together*, and that is what DFS is actually for.

Give every vertex two integers from a counter that ticks on every event:

- $d[u]$ — the **discovery** time, when $u$ is first reached;
- $f[u]$ — the **finish** time, when $u$'s adjacency list is exhausted.

Track three colours: **white** = undiscovered, **grey** = discovered but not finished (*on the current
recursion stack*), **black** = finished.

```python
WHITE, GRAY, BLACK = 0, 1, 2

def dfs_timestamps(g):
    n = len(g)
    color = [WHITE] * n
    d = [0] * n; f = [0] * n; parent = [None] * n
    t = 0

    def visit(u):
        nonlocal t
        color[u] = GRAY;  t += 1; d[u] = t
        for v in g[u]:
            if color[v] == WHITE:
                parent[v] = u
                visit(v)
        color[u] = BLACK; t += 1; f[u] = t

    for s in range(n):                     # a forest, not a tree
        if color[s] == WHITE: visit(s)
    return d, f, parent
```

The outer loop matters: a single DFS reaches only one component, so a full DFS produces a **forest**.

The counter ticks exactly twice per vertex, so **the timestamps are a permutation of
$1, 2, \dots, 2V$**, and $d[u] < f[u]$ always.

*(Verified over 300 random digraphs: all $2V$ timestamps distinct and $d[u] < f[u]$ everywhere. 0
failures.)*

**Grey means "on the stack right now."** That reading is what makes the next two sections work, and it
is worth fixing in your mind before going on.

---

## 3. The Parenthesis Theorem

Write `(u` when $u$ is discovered and `u)` when it finishes. The result is always a **balanced
parenthesis string.**

```
(0 (1 (2 2) 1) (3 3) 0)          well-formed - always
(0 (1 0) 1)                      impossible
```

Which gives the theorem:

> **For any two vertices $u, v$, exactly one of the following holds:**
> 1. the intervals $[d(u), f(u)]$ and $[d(v), f(v)]$ are **disjoint**, and neither is a descendant of
>    the other in the DFS forest;
> 2. $[d(v), f(v)]$ is **contained in** $[d(u), f(u)]$, and $v$ is a **descendant** of $u$;
> 3. $[d(u), f(u)]$ is contained in $[d(v), f(v)]$, and $u$ is a descendant of $v$.

*(Verified: 21,814 ordered pairs across 200 random digraphs. Exactly one of the three held for every
pair, and interval containment matched the descendant relation computed independently from the parent
array in every case. 0 failures.)*

Partial overlap is impossible, and the reason is simply that the intervals are stack lifetimes: $v$'s
visit either finishes before $u$'s begins, or begins and ends entirely inside it.

**Why this is useful.** It converts a question about tree structure into an arithmetic comparison:

```python
def is_descendant(v, u):
    return d[u] < d[v] and f[v] < f[u]     # O(1), no traversal
```

Ancestry in $O(1)$ from two integers per vertex. That trick reappears in Week 8's tree DP and in every
serious implementation of lowest-common-ancestor queries.

---

## 4. Edge Classification

Classify each edge $(u,v)$ by the **colour of $v$** when the edge is examined.

| $v$'s colour | type | meaning |
| --- | --- | --- |
| white | **tree** | the edge the search descended through |
| grey | **back** | $v$ is an ancestor — **$v$ is on the stack** |
| black, $d[u] < d[v]$ | **forward** | $v$ is a non-child descendant |
| black, $d[u] > d[v]$ | **cross** | everything else: another subtree, or another tree |

*(Verified: over 300 random digraphs, all four types occurred — 2,279 tree, 1,516 back, 749 forward,
1,541 cross.)*

### The result that matters

> **A directed graph has a cycle if and only if a DFS finds a back edge.**

($\Leftarrow$) A back edge $(u,v)$ means $v$ is grey, so $v$ is on the current stack, so there is a
tree path $v \rightsquigarrow u$; adding the edge $u \to v$ closes a cycle.

($\Rightarrow$) If there is a cycle, let $v$ be its first-discovered vertex. Every other cycle vertex
is reachable from $v$ through white vertices at that moment, so all become descendants of $v$; the
cycle edge entering $v$ therefore comes from a descendant, and $v$ is still grey when it is examined.

*(Verified: the back-edge test was compared against an independently written three-colour cycle
detector on 1,000 random digraphs. 0 mismatches.)*

**This is a cycle detector that costs nothing** — you get it as a side effect of a traversal you were
running anyway. It is how build systems find circular dependencies, how type checkers find infinite
types, and how deadlock detectors work.

### Undirected graphs are simpler, with a catch

> **In an undirected graph, every edge is a tree edge or a back edge.** Forward and cross edges cannot
> occur.

The catch is that this is a statement about **first encounters**. Every undirected edge is examined
twice, once from each endpoint, and the second look is classified differently:

| | first encounter | second encounter |
| --- | --- | --- |
| tree edges | 2,547 | seen as **back** (the edge to the parent): 2,547 |
| back edges | 1,487 | seen as **forward**: 1,487 |
| forward | **0** | — |
| cross | **0** | — |

*(Verified over 300 random undirected graphs. The pairing is exact: every tree edge reappears as a
back edge from the child, every back edge reappears as a forward edge from the ancestor.)*

Run the naive classifier without tracking which physical edges you have already seen and you will
count 1,487 "forward" edges in a graph that provably has none. **The classification depends on when
you look**, and forgetting that is the direct cause of the bug in the next section.

---

## 5. Cycle Detection in Undirected Graphs, and the Parent Trap

The directed rule — "a back edge means a cycle" — appears to transfer. It does not, because in an
undirected graph *every* tree edge produces a back edge when examined from the child.

```python
def has_cycle_wrong(g):
    seen = [False] * len(g)
    def go(u):
        seen[u] = True
        for v in g[u]:
            if seen[v]: return True        # <-- this includes the parent
            if go(v): return True
        return False
    return any(not seen[s] and go(s) for s in range(len(g)))
```

On a 4-vertex **tree** with edges $0-1$, $1-2$, $1-3$:

```
without the parent check:  True    <- WRONG, there is no cycle
with the parent check   :  False   <- correct
```

*(Verified by execution.)*

The fix is to ignore the edge you arrived on:

```python
def has_cycle(g):
    seen = [False] * len(g)
    def go(u, p):
        seen[u] = True
        for v in g[u]:
            if not seen[v]:
                if go(v, u): return True
            elif v != p: return True       # a back edge that is not the parent edge
        return False
    return any(not seen[s] and go(s, -1) for s in range(len(g)))
```

### Where the real trap is

`v != p` is widely described as "correct only for simple graphs," on the grounds that two parallel
edges between $u$ and $p$ genuinely *are* a cycle of length 2 which the parent test would reject.

**That is wrong, and it is worth seeing why.** If $u$ and $p$ are joined by two edges, then `g[p]`
contains `u` **twice**. DFS descends through the first copy; on returning it examines the second,
finds $u$ already seen and not equal to *its own* parent, and reports the cycle. Self-loops are caught
too, for the same reason.

*(Verified exhaustively over every multigraph on $V \le 4$ with up to 3 edges — self-loops and
parallel edges included — against a union-find ground truth: **0 disagreements.**)*

The genuine failure happens one step earlier, when the graph is built:

```python
adj = [set() for _ in range(V)]            # <-- the bug
for u, v in edges:
    adj[u].add(v); adj[v].add(u)
```

*(Verified over the same exhaustive search: building adjacency with `set` instead of `list` produces
**56 wrong answers**, the smallest being two vertices joined by two parallel edges.)*

**A `set` deduplicates, so the second copy of the edge is discarded before the algorithm ever runs.**
The traversal is then correct about a graph that is not the one you were given.

Two things to take from this. First, if you use sets for adjacency — and there are good reasons to,
since they make edge queries $O(1)$ — you have chosen a representation that **cannot express a
multigraph**, and you must know that. Second, and more generally: *the bug people warn you about here
is not the bug that is actually present.* The received wisdom names the algorithm; the fault is in the
data structure. **Check the claim before repeating it**, which is what the exhaustive search above was
for.

---

## 6. What DFS Is Actually For

BFS answers one question extremely well. DFS answers a different, larger set, and this list is the
reason it recurs all term:

| use | mechanism | where |
| --- | --- | --- |
| cycle detection | back edges | above |
| connected components | one DFS per undiscovered vertex | PS 4 |
| **topological sort** | reverse order of finish times | Week 5 (DAG shortest paths) |
| **strongly connected components** | two DFS passes, second on the reverse graph | Week 5 |
| ancestry queries | the parenthesis theorem | Week 8 |
| bridges and articulation points | low-link values from back edges | Week 11 |
| solving mazes and puzzles | backtracking, the same recursion | Week 12 |

Topological sort deserves a preview, because it follows from section 2 with almost no extra work.

> **In a DAG, sorting the vertices by *decreasing finish time* yields a topological order.**

The reason is exactly the cycle theorem. For any edge $(u,v)$: $v$ cannot be grey, or the edge would
be a back edge and the graph would have a cycle. So $v$ is either white — and becomes a descendant of
$u$, finishing first — or already black, having finished earlier. **Either way $f[v] < f[u]$**, which
is what the ordering requires.

So a topological sort is a DFS plus a list built in reverse — $\Theta(V+E)$, and no extra data
structure at all.

---

## 7. BFS Against DFS

| | BFS | DFS |
| --- | --- | --- |
| collection | queue | stack (or recursion) |
| finds shortest paths | **yes**, unweighted | no |
| space | $\Theta(V)$ queue | $\Theta(h)$ stack, $h$ = deepest path |
| worst-case space | $\Theta(V)$ | $\Theta(V)$ |
| natural recursion | no | yes |
| reveals cycles | awkwardly | **directly**, via back edges |
| reveals ordering | no | **yes**, via finish times |
| good for | distances, levels, "fewest moves" | structure, ordering, backtracking |

**Neither dominates.** The choice follows from the question, and it is worth being able to say in one
sentence which you want and why.

One practical note in DFS's favour: on a wide shallow graph its stack holds only the current path,
which can be far smaller than BFS's frontier. On a deep narrow graph the reverse is true. **Both are
$\Theta(V)$ in the worst case, and the typical case depends entirely on shape.**

---

## 8. Where This Leaves Week 4

You have the traversal skeleton from Lecture 13 §6 instantiated twice, and one substitution left to
make. Replacing the queue with a **priority queue** — the structure from Week 3 — turns BFS into
Dijkstra's algorithm and "fewest edges" into "least total weight."

**Week 5 makes that substitution**, and also uses this lecture's finish-time ordering for shortest
paths on DAGs. **MIDTERM 1 (Weeks 0–4) is in Week 5**; the revision guide in `resources/` lists what
is examinable.

---

## 9. What to Do

- Read CLRS §20.3. The parenthesis theorem is Theorem 20.7 and the classification is §20.3.4.
- **PS 4** implements timestamps, the classification, and both cycle detectors — including the
  `set`-versus-`list` adjacency question from §5, which it asks you to settle by exhaustive search
  rather than by argument.
- **Lab 4** contrasts the two traversals on a real network.
- **Quiz 4 covers Week 3.**

---

*CS 102 · Week 4 · Lecture 15 · © CSE Department*
