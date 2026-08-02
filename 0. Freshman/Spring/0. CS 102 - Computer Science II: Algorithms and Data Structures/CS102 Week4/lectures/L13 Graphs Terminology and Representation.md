# CS 102 · Computer Science II
## Lecture 13: Graphs — Terminology and Representation

---

## 1. Why Graphs Are Different

Everything so far has been a *container*. A BST, an AVL tree, a heap — each holds items and answers
questions about the items. The structure was in service of storage.

**A graph is not a container. It is a relation.** The items matter less than the connections between
them, and almost every interesting question is about the connections: is there a path? how short?
which parts are separable?

That change of subject is why graphs occupy a third of this course. It is also why the algorithms
look different — you will not be asked to insert into a graph efficiently. You will be asked what the
graph's shape implies.

The list of things that are graphs is unreasonably long: road networks, the web, social networks,
call graphs, dependency graphs, state machines, circuits, molecules, scheduling constraints, and the
type relationships in the language you are writing in. **When a problem resists, ask what its graph
is.** That heuristic will serve you for the rest of the degree.

---

## 2. Terminology

A **graph** $G = (V, E)$ is a set of **vertices** $V$ and a set of **edges** $E$, each edge joining
two vertices. Throughout this course $|V| = V$ and $|E| = E$ where no confusion arises — an abuse of
notation that CLRS also commits, because writing $O(|V| + |E|)$ everywhere is unbearable.

| term | meaning |
| --- | --- |
| **undirected** | edges have no direction; $\{u,v\}$ is the same edge as $\{v,u\}$ |
| **directed** (digraph) | edges are ordered pairs $(u,v)$; the edge points from $u$ to $v$ |
| **weighted** | each edge carries a number — a distance, cost, or capacity |
| **adjacent** / **neighbours** | $u$ and $v$ are adjacent if $\{u,v\} \in E$ |
| **degree** $\deg(u)$ | the number of edges at $u$; in a digraph, **in-degree** and **out-degree** |
| **path** | a sequence of vertices, each adjacent to the next |
| **simple path** | a path with no repeated vertex |
| **cycle** | a path from a vertex back to itself |
| **connected** | (undirected) every vertex is reachable from every other |
| **component** | a maximal connected piece |
| **tree** | connected and acyclic — equivalently, connected with $E = V - 1$ |
| **DAG** | directed acyclic graph |

### Two facts to have immediately

**The handshake lemma.** $\sum_{u \in V} \deg(u) = 2E$, because every edge contributes 1 to the
degree of each endpoint. An immediate corollary: **the number of odd-degree vertices is even.**

**Sparse against dense.** $E$ ranges from 0 to $\binom{V}{2} \approx V^2/2$. A graph is called
**sparse** when $E = O(V)$ and **dense** when $E = \Theta(V^2)$.

That distinction decides almost every representation and algorithm choice in the next three weeks,
and the important empirical fact is that **real graphs are overwhelmingly sparse.** Road networks
have a bounded number of roads per junction. Social networks have people with a few hundred friends
out of billions. The dense case is the exception, and when you meet one it is usually small.

---

## 3. The Two Representations

### Adjacency matrix

A $V \times V$ array with $M[u][v] = 1$ when the edge exists.

```python
M = [[0]*V for _ in range(V)]
for u, v in edges:
    M[u][v] = M[v][u] = 1          # symmetric if undirected
```

- **Space** $\Theta(V^2)$, *regardless of how many edges there are.*
- **"Is $u$ adjacent to $v$?"** in $O(1)$.
- **Iterate over $u$'s neighbours** in $\Theta(V)$ — you must scan the whole row, including the zeros.

### Adjacency list

An array of $V$ lists, where `g[u]` holds $u$'s neighbours.

```python
g = [[] for _ in range(V)]
for u, v in edges:
    g[u].append(v); g[v].append(u)
```

- **Space** $\Theta(V + E)$.
- **"Is $u$ adjacent to $v$?"** in $O(\deg(u))$ — you must search the list.
- **Iterate over $u$'s neighbours** in $\Theta(\deg(u))$, which is optimal.

### The comparison

| | matrix | list |
| --- | --- | --- |
| space | $\Theta(V^2)$ | $\Theta(V+E)$ |
| edge query | $O(1)$ | $O(\deg u)$ |
| iterate neighbours | $\Theta(V)$ | $\Theta(\deg u)$ |
| add edge | $O(1)$ | $O(1)$ |
| BFS / DFS over the whole graph | $\Theta(V^2)$ | $\Theta(V+E)$ |

**The last row is the one that matters this week**, and it is the reason the adjacency list is the
default. A traversal must look at every vertex's neighbours; with a matrix that is $V$ scans of length
$V$ whatever the graph looks like. On a sparse graph with $E = 3V$, the list does $\Theta(V)$ work and
the matrix does $\Theta(V^2)$ — at $V = 10^6$ that is the difference between a second and a fortnight.

---

## 4. Measured, and a Surprise

Space actually used, measured recursively with `sys.getsizeof` on this machine:

| $V$ | $E$ | matrix | list | ratio |
| --- | --- | --- | --- | --- |
| 100 | 200 | 86,576 B | 13,772 B | 6.3× |
| 500 | 1,000 | 2,032,272 B | 88,220 B | 23.0× |
| 1,000 | 2,000 | 8,064,912 B | 199,164 B | 40.5× |
| 2,000 | 4,000 | 32,128,240 B | 420,080 B | **76.5×** |

**The ratio doubles when $V$ doubles**, which is $\Theta(V^2)$ against $\Theta(V+E)$ appearing exactly
as advertised.

Now the surprise. Fix $V = 400$ and vary the density:

| $E$ | density | matrix | list | ratio |
| --- | --- | --- | --- | --- |
| 400 | 0.005 | 1,305,712 B | 52,040 B | 25.1× |
| 2,000 | 0.025 | 1,305,712 B | 116,348 B | 11.2× |
| 10,000 | 0.125 | 1,305,712 B | 411,328 B | 3.2× |
| 40,000 | 0.501 | 1,305,712 B | 1,520,720 B | **0.86×** |
| 79,800 | 1.000 | 1,305,712 B | 2,910,448 B | **0.45×** |

**The crossover is at about 50% density**, not the 1–2% that the asymptotics might suggest. In a
complete graph the adjacency list uses **more than twice** the matrix's memory.

The reason is a Python fact rather than a graph fact: a `list` of small integers stores *pointers to
integer objects*, so each neighbour entry costs 8 bytes of pointer plus a share of a 28-byte `int`
object, while the matrix — also a list of lists — pays the same overhead but stores $V^2$ entries
regardless. **In C, where a matrix could be a bit array at one bit per pair, the crossover would sit
somewhere else entirely.**

Two lessons, and the second is the transferable one:

1. **Use adjacency lists.** Real graphs are sparse, and at the densities that occur in practice the
   list wins by one to two orders of magnitude.
2. **A space bound in $\Theta$ notation does not tell you the crossover point.** $\Theta(V+E)$ beats
   $\Theta(V^2)$ eventually and for all sparse graphs, but *where* the two cross depends on the
   constant factors of your language and machine. Week 2 found the same thing with `SortedList`,
   Week 3 with heap sort. **This is now a pattern, and you should expect it.**

---

## 5. Variants You Will Meet

**Weighted graphs.** Store `(neighbour, weight)` pairs: `g[u] = [(v, w), ...]`. Weeks 5 and 6 use this
form throughout.

**Directed graphs.** Append in one direction only. Note that a digraph has *two* natural adjacency
lists — successors and predecessors — and some algorithms need both. Building the reverse graph costs
$\Theta(V+E)$ and is worth doing when you need it more than once.

**Implicit graphs.** Sometimes the graph is never built at all. A puzzle's states are its vertices and
its legal moves are its edges; there may be $10^{20}$ of them, and you generate neighbours on demand.
**Every algorithm this week works unchanged on an implicit graph**, provided you can enumerate a
vertex's neighbours — which is why BFS is the standard tool for shortest solution sequences.

**Self-loops and multi-edges.** An edge from a vertex to itself, or two edges between the same pair.
Most of this course assumes **simple** graphs — neither is present.

Note that the choice above already commits you: `g[u]` built as a `list` can hold a repeated
neighbour, while a `set` cannot. **Adjacency built from sets makes edge queries $O(1)$ and makes
multigraphs inexpressible**, and if your input has parallel edges the loss happens at construction
time, silently. Lecture 15 §5 has the measurement, and it is not the failure most textbooks warn
about.

---

## 6. The Skeleton for the Rest of the Term

Here is the whole of this week, and much of the next two, in one piece of pseudocode:

```
put the source into a COLLECTION
while the COLLECTION is not empty:
    take a vertex u out of the COLLECTION
    if u has been visited: continue
    mark u visited
    for each neighbour v of u:
        put v into the COLLECTION
```

**Change the collection and you change the algorithm.**

| collection | algorithm | finds |
| --- | --- | --- |
| **queue** (FIFO) | **BFS** — Lecture 14 | fewest *edges* |
| **stack** (LIFO) | **DFS** — Lecture 15 | structure: cycles, components, ordering |
| **priority queue** | **Dijkstra** — Week 5 | least total *weight* |

That priority queue is the one you built last week. **One skeleton, three data structures, three
different meanings of "next"** — and the reason Week 3 came before Week 4 rather than after.

It is worth being precise about what changes. All three visit every reachable vertex, all three do
$\Theta(V+E)$ work up to the collection's own cost, and all three build a tree of "how I first got
here." They differ only in *the order the collection hands vertices back*, and that order is what
makes one of them compute shortest paths and another one detect cycles.

---

## 7. A Caution About $O(V+E)$

BFS and DFS are $\Theta(V+E)$, and that is a genuine bound on the number of operations. It is not a
promise about time.

Measured, BFS best of 5, on two families of sparse graph:

| | **random**, avg degree 6 | | **grid**, the $k\times k$ lattice | |
| --- | --- | --- | --- | --- |
| $V$ | BFS | ns per $(V+E)$ | BFS | ns per $(V+E)$ |
| $\approx 10^4$ | 3.2 ms | **80.6** | 2.3 ms | **78.4** |
| $\approx 5\times10^4$ | 46.8 ms | 234.2 | 12.8 ms | 85.0 |
| $\approx 2\times10^5$ | 258.2 ms | 322.8 | 55.9 ms | 92.9 |
| $\approx 10^6$ | 1597.4 ms | **399.4** | 356.1 ms | **118.8** |

Read the two ns columns together. They **start at the same place** — about 80 nanoseconds per unit of
$(V+E)$ — and then diverge: the random graph degrades by **5.0×**, the grid by **1.5×**.

The algorithm has not stopped being linear. The *cost of one step* has changed, and only for one of
the graphs. A traversal of a random graph jumps to an unpredictable memory location at every edge; on
a grid numbered $ik+j$, a vertex's neighbours are at $\pm 1$ and $\pm k$, so most of them are already
in cache.

**Same code, same asymptotics, same $V$ and $E$ — 3.4× the time, because of the shape of the graph.**

Two consequences:

1. This is Week 3's locality argument again. $\Theta(V+E)$ is an honest count of *operations*; what an
   operation costs is a separate question that the notation deliberately does not address.
2. **Graph benchmarks are structure-dependent to a degree that makes many of them useless.** A
   published figure means little without the graph family, and "we tested on random graphs" and "we
   tested on road networks" describe measurements that can differ by a factor of several. When you see
   a graph-algorithm benchmark, ask what the graph was — and when you publish one, say.

---

## 8. What to Do

- Read CLRS §20.1 (representations) — short, and the exercises are worth doing.
- **PS 4** is released Friday and implements both representations before either traversal.
- **Quiz 4 covers Week 3** — heaps, the linear build, priority queues. Not graphs.
- **MIDTERM 1 is announced this week**, covering Weeks 0–4, and sits in Week 5. The syllabus has the
  format; the revision guide is in `resources/`.

---

*CS 102 · Week 4 · Lecture 13 · © CSE Department*
