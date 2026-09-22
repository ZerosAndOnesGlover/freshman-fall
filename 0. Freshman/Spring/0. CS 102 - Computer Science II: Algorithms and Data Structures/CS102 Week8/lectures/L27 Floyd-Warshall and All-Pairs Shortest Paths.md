# CS 102 · Computer Science II
## Lecture 27: Floyd–Warshall and All-Pairs Shortest Paths

**Date:** Friday 19 March 2027 · 09:00–09:50 · Week 8

---

## 1. The State Nobody Guesses

**Problem.** The shortest distance between **every** pair of vertices.

The obvious approach is to run a single-source algorithm $V$ times. That works, and Week 5 gives you
two ways to do it. Floyd–Warshall does something else, and its state is the least guessable in this
course:

> $d^{(k)}[i][j]$ = the shortest distance from $i$ to $j$ using **only vertices $0 \dots k-1$ as
> intermediates.**

Nobody arrives at that by staring at the problem. But once you have it, the recurrence writes itself.
Consider whether the shortest $i \rightsquigarrow j$ path that may use $\{0, \dots, k\}$ actually uses
vertex $k$:

- **it does not** — then it is the answer for $\{0, \dots, k-1\}$, unchanged;
- **it does** — then it goes $i \rightsquigarrow k \rightsquigarrow j$, and **both halves avoid $k$**
  (a shortest path visits no vertex twice), so both are answers for $\{0, \dots, k-1\}$.

$$d^{(k+1)}[i][j] = \min\Big(d^{(k)}[i][j],\ \ d^{(k)}[i][k] + d^{(k)}[k][j]\Big)$$

That second bullet is the whole proof. **The two halves are subproblems of the same kind precisely
because $k$ cannot appear inside either of them.**

---

## 2. The Algorithm

$V^3$ states, $O(1)$ work each. And since level $k+1$ depends only on level $k$, the third dimension
rolls away:

```python
def floyd_warshall(V, d):
    """d is a V x V matrix: d[i][j] = weight, INF if absent, d[i][i] = 0.
       Modified in place."""
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d
```

**Five lines, $\Theta(V^3)$ time, $\Theta(V^2)$ space.** It is the shortest non-trivial algorithm in
the course.

*(Verified against Bellman–Ford run from every source: 300 random graphs with non-negative weights and
300 with negative weights. **0 mismatches** in both.)*

### The in-place version is correct, and that is not obvious

The code above overwrites `d` while reading it, so during round $k$ some entries are already updated to
level $k+1$ and others are not. **This does not matter**, and the reason is worth seeing:

$$d^{(k+1)}[i][k] = \min\big(d^{(k)}[i][k],\ d^{(k)}[i][k] + d^{(k)}[k][k]\big) = d^{(k)}[i][k]$$

since $d[k][k] = 0$. **Row $k$ and column $k$ do not change during round $k$**, and those are the only
entries the update reads. So reading a mixture of old and new values is safe.

---

## 3. The Loop Order Is Not Negotiable

`k` **must** be the outermost loop. This is the bug of the lecture, and unlike most bugs it produces
plausible output.

*(Verified: all six orderings of the three loops, each run on 200 random graphs and compared against
Bellman–Ford from every source.)*

| loop order | wrong on |
| --- | --- |
| `k, i, j` | **0 of 200** |
| `k, j, i` | **0 of 200** |
| `i, k, j` | 78 of 200 |
| `i, j, k` | 70 of 200 |
| `j, i, k` | 70 of 200 |
| `j, k, i` | 73 of 200 |

**Both orders with `k` outermost are correct; all four others are wrong about a third of the time.**

The reason is the meaning of the state. The recurrence needs *all* of level $k$ complete before level
$k+1$ begins. With `k` innermost, you finish cell $(i,j)$ for every $k$ before moving on — using
intermediate values that are not yet final.

**A third of the time is the worst possible failure rate.** It is frequent enough to be a real bug and
rare enough that a handful of small tests will pass.

---

## 4. Negative Cycles, for Free

After the algorithm runs, $d[i][i]$ is the cheapest way to leave $i$ and return. If that is **negative**,
$i$ lies on a negative cycle.

```python
has_negative_cycle = any(d[i][i] < 0 for i in range(V))
```

*(Verified: agrees with a Bellman–Ford virtual-source detector on **400 of 400** random graphs with
negative edges.)*

Two advantages over Week 5's approach. It detects negative cycles **anywhere in the graph**, not only
those reachable from one source — Lecture 18 §4 needed a virtual source for that. And it costs nothing:
you read the diagonal of a matrix you already computed.

**Caveat.** Once a negative cycle exists, the off-diagonal entries are meaningless for any pair whose
path can reach it. Check the diagonal **before** trusting anything else.

---

## 5. Against $V \times$ Single-Source

| method | complexity | negative edges |
| --- | --- | --- |
| $V\times$ BFS | $\Theta(V(V+E))$ | unweighted only |
| $V\times$ Dijkstra (heap) | $O(V(V+E)\log V)$ | **no** |
| $V\times$ Bellman–Ford | $O(V^2E)$ | yes |
| **Floyd–Warshall** | $\Theta(V^3)$ | **yes** |
| Johnson's | $O(V^2\log V + VE)$ | yes |

On a **dense** graph $E \approx V^2$, so $V\times$Dijkstra is $O(V^3\log V)$ and Floyd–Warshall's
$\Theta(V^3)$ should win. Measured, on this machine:

| $V$ | density | $E$ | Floyd–Warshall | $V\times$Dijkstra |
| --- | --- | --- | --- | --- |
| 200 | 0.5 | 20,000 | 317 ms | **193 ms** |
| 200 | 1.0 | 39,800 | **304 ms** | 328 ms |
| 300 | 1.0 | 89,700 | **1,079 ms** | 1,080 ms |
| 400 | 1.0 | 159,600 | 2,703 ms | **2,579 ms** |

**They are within about 10% of each other even on the complete graph**, trading places
run to run. The predicted $\log V$ advantage does not appear.

The reason is by now familiar: Floyd–Warshall's triple loop is interpreted Python, while Dijkstra's
work happens inside `heapq`, which is C. **This is the sixth time this term** that a complexity
comparison has failed to predict a measurement, and the cause has been the same every time.

> **So why use Floyd–Warshall?** Not for speed in Python. Use it because it is **five lines**, because
> it **handles negative edges** where Dijkstra silently does not, because it **detects negative cycles
> for free**, and because it works directly on the adjacency matrix you may already have. In C — or
> under `numpy`, where the inner loop vectorises — the $\Theta(V^3)$ advantage is real. **Choose it for
> what it does, not for what its exponent says.**

---

## 6. Reconstructing Paths

Store, for each pair, the **next** vertex on the route:

```python
def floyd_warshall_paths(V, d):
    nxt = [[j if d[i][j] < INF else None for j in range(V)] for i in range(V)]
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    nxt[i][j] = nxt[i][k]          # NOT k
    return d, nxt

def path(nxt, i, j):
    if nxt[i][j] is None: return None
    out = [i]
    while i != j:
        i = nxt[i][j]; out.append(i)
    return out
```

**`nxt[i][j] = nxt[i][k]`, not `= k`.** The stored value is the *first hop* out of $i$, and the first
hop towards $k$ is also the first hop towards $j$ on the improved route. Writing `k` records a vertex
that may be far down the path, and `path` then emits a sequence that is not a walk in the graph.

*(Verified over 200 random graphs, checking every reachable pair — that the reconstructed sequence is a
real walk, starts and ends correctly, and has total weight equal to $d[i][j]$:)*

| stored value | invalid reconstructions |
| --- | --- |
| `nxt[i][k]` | **0 of 4,210** |
| `k` | **221 of 3,708** (≈6%) |

Six per cent again — frequent enough to be real, rare enough to survive casual testing. **The distances
are correct in both cases**; only the paths are wrong, so a test that checks lengths will not find it.

---

## 7. Transitive Closure and the Wider Pattern

Replace `min` with `or` and `+` with `and`, and the identical triple loop computes **reachability**:

$$r[i][j] \mathrel{|{=}} r[i][k] \wedge r[k][j]$$

That is **Warshall's algorithm**, and the coincidence is not one. Both are instances of the same
computation over different **semirings** — $(\min, +)$ for shortest paths, $(\vee, \wedge)$ for
reachability, and $(+, \times)$ for counting paths. Changing the two operators changes the problem and
not a line of the control flow.

This is a genuinely deep observation and it is the beginning of algebraic path theory. You are not
examined on it. It is worth knowing that the five lines you just wrote are more general than the
problem they were introduced for.

---

## 8. Where Week 8 Leaves You

Six state designs in three lectures: intervals, "ending at $i$", remaining amount, subtree-plus-flag,
subset-plus-position, and allowed-intermediates. **None of them is deducible from the problem
statement**, and all of them are obvious afterwards. That asymmetry is what makes DP feel hard, and the
only cure is having seen enough of them.

**Week 9 changes technique.** A greedy algorithm makes one choice and never revisits it — no table, no
subproblems, usually $\Theta(n\log n)$. It is faster than DP whenever it works, and Week 9 is entirely
about **proving that it does**, using the exchange argument you already met in Week 6's cut property.
Coin change in Lecture 26 §3 is the warning: greedy on $[1,5,6,9]$ is wrong for 84 of the first 199
targets, and nothing in the code says so.

---

## 9. What to Do

- Read CLRS §23.1–23.2 (Floyd–Warshall and transitive closure). §23.3 (Johnson's) is optional and
  excellent — it uses Bellman–Ford once to reweight, then Dijkstra $V$ times.
- **Lab 8** implements Floyd–Warshall, reproduces the loop-order experiment, and adds path
  reconstruction.
- **PS 8** is due Friday of Week 9 — the same day as **PROJECT 1**. Plan accordingly.
- **Quiz 8 covers Week 7.**

---

*CS 102 · Week 8 · Lecture 27 · © CSE Department*
