# CS 102 · Lab 8 — Solutions and Checkoff Notes
## Implementing Floyd–Warshall

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**This is Project 1 week minus one.** Students will be behind on the project. The lab is short —
Floyd–Warshall is five lines — so it is reasonable to let them leave early if Parts A–C are done and
checked off, and several will use the time for the project. That is a good outcome; say so rather
than letting them feel they are cutting a corner.

**Part D's timing runs take a couple of minutes at $V = 400$.** Have students launch those first and
do Part B while they run.

The one thing to insist on: **A2 must be verified against an independent reference before anything
else.** Every subsequent part compares against their own implementation.

---

## Part A — The Algorithm (10)

### A1 (4), A2 (4) — deterministic: 0 mismatches

300 non-negative and 300 negative-edge graphs against Bellman–Ford from every source.

*The common error is initialising `d[i][i]` to `INF` rather than 0. It produces a matrix that is
correct except on the diagonal — and then the Part C2 negative-cycle test never fires. Check the
diagonal is zero before they move on.*

### A3 (2) — deterministic

```
          0     1     2     3
  0       0     3    -1     4
  1       3     0    -4     1
  2       7     4     0     5
  3       2    -1    -5     0
```

Worth pointing out at checkoff: $d[1][2] = -4$ via $1 \to 3 \to 2 = 1 + (-5)$, which beats the
direct edge of weight 4 — and $d[0][2] = -1$ rather than 8, for the same reason. **The negative edge
is doing real work here**, which is why this graph was chosen.

---

## Part B — The Loop Order (12)

### B1 (5), B2 (4) — deterministic

| loop order | wrong on 200 |
| --- | --- |
| `k,i,j` | **0** |
| `k,j,i` | **0** |
| `i,k,j` | 78 |
| `i,j,k` | 70 |
| `j,i,k` | 70 |
| `j,k,i` | 73 |

*Accept ±5 on the wrong counts if their graph generator differs; the pattern — exactly two correct,
the other four wrong on 35–40% — must hold. **A student reporting more than two correct orderings has
a bug in their test**, most likely comparing against their own `k,i,j` version rather than an
independent reference.*

### B3 (3) — the assessed question

**(a) (2)** `k,i,j` and `k,j,i`. What they share: **`k` is outermost.**

**(b) (1)** $d^{(k)}[i][j]$ is the shortest $i\rightsquigarrow j$ distance using only vertices
$\{0,\dots,k-1\}$ as intermediates. The recurrence computes level $k+1$ from **level-$k$ values for
every pair**, so the whole of level $k$ must be finished first. With `k` inner, cell $(i,j)$ is driven
through all $k$ before its neighbours have been touched, so it reads values that are not yet the
level-$k$ answers.

The inner two loops may be in either order because, within round $k$, row $k$ and column $k$ do not
change — so the updates cannot interfere with each other.

*The mark is for an explanation in terms of the **meaning** of $d^{(k)}$. "The values aren't ready yet"
is the right instinct without the content; give it only if they say what the values are supposed to be.*

---

## Part C — Paths and Negative Cycles (10)

### C1 (5) — deterministic

| stored on improvement | invalid reconstructions |
| --- | --- |
| `nxt[i][j] = nxt[i][k]` | **0 of 4,210** |
| `nxt[i][j] = k` | **221 of 3,708** (≈6%) |

**The point to draw out**: the distances are *identical* in both cases. Only the paths differ, so any
test that checks distances passes completely. This is why the handout insists on validating the path
as a walk with the right total weight.

*3 for a correct `nxt` with the path validation, 2 for reporting both variants. A student who only
implemented the correct one and asserted the other is wrong scores 3 of 5 — the question said try
both.*

### C2 (5)

**(a) (3)** Diagonal test agreed with an independent detector on **400 of 400**.

**(b) (2)** Floyd–Warshall computes distances between *all* pairs, so a negative cycle anywhere makes
some $d[i][i]$ negative regardless of reachability from any particular source. Bellman–Ford from $s$
only ever relaxes vertices reachable from $s$, which is why Week 5 Lecture 18 §4 needed a virtual
source with 0-weight edges to everything.

Once a negative cycle exists, **the off-diagonal entries are meaningless** for any pair whose route can
reach it — there is no shortest path. Check the diagonal first.

---

## Part D — Is It Actually Faster? (8)

### D1 (4) — machine-dependent, ordering is not

| $V$ | density | $E$ | Floyd–Warshall | $V\times$Dijkstra |
| --- | --- | --- | --- | --- |
| 200 | 0.5 | 20,000 | 317 ms | **193 ms** |
| 200 | 1.0 | 39,800 | **304 ms** | 328 ms |
| 300 | 1.0 | 89,700 | **1,079 ms** | 1,080 ms |
| 400 | 1.0 | 159,600 | 2,703 ms | **2,579 ms** |

They trade places. **Neither wins decisively even on the complete graph.**

### D2 (4)

**(a) (2)** Floyd–Warshall's inner loop is **interpreted Python bytecode**, executed $V^3$ times.
Dijkstra's per-vertex work happens inside `heapq`, which is a **C extension**. The $\log V$ that
Floyd–Warshall saves asymptotically is smaller, over this range, than the constant-factor gap between
interpreted and compiled inner loops.

**(b) (2)** Any three of:

- it **handles negative edges**, which Dijkstra silently does not;
- it **detects negative cycles for free** from the diagonal;
- it is **five lines** — far less to get wrong, and no priority queue;
- it works **directly on an adjacency matrix**, which may be the representation you already have;
- it **vectorises** — under `numpy` or in C the $\Theta(V^3)$ advantage is real;
- its performance is **completely predictable**, independent of graph structure.

*2 for a correct mechanism in (a). "Python is slow" alone is 0 — the question asks where each inner
loop executes. For (b), reject "it's faster on dense graphs", which their own D1 table refutes.*

---

## Checkoff Checklist

1. `d[i][i] = 0` initially, and A3's matrix matches.
2. A2 compares against an **independent** reference, not their own variant.
3. Exactly **two** of six loop orderings are reported correct.
4. C1 reports **both** `nxt` variants, with path validation as a walk.
5. D2(b) gives three reasons, none of them speed.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 10 |
| B | 12 |
| C | 10 |
| D | 8 |
| **Total** | **40** |

Labs are pass/fail for progression: **10 of the 12 required labs (0–11).**

---

## Note for the Week 9 Lecture

This is the last DP lab, and the last time this term a *correctness* question has an answer you can
get by looking at the code. Week 9's greedy algorithms are all short, all obviously terminating, and
several of them are wrong on inputs nobody thinks to try — coin change on $[1,5,6,9]$ being the
example already on the table.

**Parts B and C here are the rehearsal.** In both, the implementation runs, produces well-formed
output, and is wrong; in both, the only defence was knowing what a quantity was supposed to *mean*.
Open Week 9 by pointing at the loop-order table and saying that greedy correctness is the same
situation with no table to inspect — which is why the week is about proofs rather than code.

---

*CS 102 · Week 8 · Lab 8 Solutions · © CSE Department*
