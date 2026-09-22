# CS 102 · Lab 8
## Implementing Floyd–Warshall

**Date:** Tuesday 23 March 2027 · 15:00–16:50 · Lab section (Week 9) — covers Week 8 (L25–L27)
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab8.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 13 labs to pass the course.** See the syllabus.

---

## Purpose

Floyd–Warshall is five lines. That makes it a good lab, because the whole session can be spent on the
things the five lines do not tell you: **which loop goes outside**, **why the in-place version is
safe**, **how to get the paths out**, and **whether it is actually faster than the alternative**.

Three of those four have a wrong answer that produces plausible output.

---

## Part A — The Algorithm (10 pts)

**A1.** *(4)* `floyd_warshall(V, d)` operating in place on a $V\times V$ matrix with `INF` for absent
edges and 0 on the diagonal.

**A2.** *(4)* Verify against Bellman–Ford run from **every** source, on at least 150 random graphs
including some with **negative** edges (but no negative cycles). Report graphs tested and mismatches.

**A3.** *(2)* Print the full distance matrix for this graph, using `.` for unreachable:

$$0\to1\ (3),\quad 0\to2\ (8),\quad 1\to3\ (1),\quad 2\to1\ (4),\quad 3\to0\ (2),\quad 3\to2\ (-5)$$

---

## Part B — The Loop Order (12 pts)

**B1.** *(5)* Write a version parameterised by which of `i`, `j`, `k` is the outer, middle, and inner
loop, so all **six** orderings can be run.

**B2.** *(4)* Test all six against a correct reference on at least 150 random graphs. Report a table
of six rows: the ordering and how many graphs it got wrong.

**B3.** *(3)* Two of the six are correct.

- **(a)** *(2)* Which two, and what do they have in common?
- **(b)** *(1)* Explain the failure in terms of what $d^{(k)}[i][j]$ **means** — not in terms of the
  code.

---

## Part C — Paths and Negative Cycles (10 pts)

**C1.** *(5)* Add a `nxt` matrix so you can reconstruct an actual shortest path, and a `path(i, j)`
function returning the vertex sequence or `None`.

Verify on at least 100 graphs that **every** reconstructed path is a real walk in the graph, starts
and ends correctly, and has total weight equal to the computed distance. Report failures.

> There are two plausible things to store in `nxt`. **One of them is wrong.** Try both and report the
> failure count for each — the distances are correct either way, so only the path check finds it.

**C2.** *(5)* **Negative-cycle detection.** After the algorithm, report whether any $d[i][i] < 0$.

- **(a)** *(3)* Verify against an independent detector on at least 200 graphs with negative edges.
- **(b)** *(2)* Floyd–Warshall detects negative cycles **anywhere**; Week 5's Bellman–Ford detected
  only those reachable from the source. Explain why, and say what the off-diagonal entries mean once a
  negative cycle exists.

---

## Part D — Is It Actually Faster? (8 pts)

The textbook claim: on a dense graph, Floyd–Warshall's $\Theta(V^3)$ beats $V\times$Dijkstra's
$O(V^3\log V)$.

**D1.** *(4)* Time both at $V \in \{200, 300\}$ and densities $\{0.5, 1.0\}$, confirming they agree.
Report a table.

**D2.** *(4)* You should find the two are within roughly 10% of each other even on the complete graph.

- **(a)** *(2)* **Why?** Your answer must refer to where each algorithm's inner loop actually executes.
- **(b)** *(2)* Given that, state **three** reasons you would still choose Floyd–Warshall for a
  problem, none of which is speed.

---

## Submission

- `lab8.py` — runnable end to end, producing every table.
- `RESULTS.md` — all tables and answers. **Include your machine and Python version.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 10 | A correct implementation, verified independently |
| B | 12 | The loop order and what it means |
| C | 10 | Path reconstruction and negative cycles |
| D | 8 | Measuring, and choosing for the right reason |
| **Total** | **40** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Counts are deterministic; timings are not.**

**A2** — 300 non-negative graphs and 300 with negative edges: **0 mismatches** in both.

**A3 — the distance matrix** (the graph has negative edges but no negative cycle):

```
          0     1     2     3
  0       0     3    -1     4
  1       3     0    -4     1
  2       7     4     0     5
  3       2    -1    -5     0
```

Every vertex is reachable from every other, so no `.` appears. The diagonal is all zero — no negative
cycle. Note $d[1][2] = -4$: the route $1 \to 3 \to 2$ costs $1 + (-5)$, which beats the direct edge.

**B2 — the six orderings**, 200 random graphs each:

| loop order | wrong on |
| --- | --- |
| `k, i, j` | **0** |
| `k, j, i` | **0** |
| `i, k, j` | 78 |
| `i, j, k` | 70 |
| `j, i, k` | 70 |
| `j, k, i` | 73 |

**C1 — the two candidates for `nxt`:**

| stored on improvement | invalid path reconstructions |
| --- | --- |
| `nxt[i][j] = nxt[i][k]` | **0 of 4,210** |
| `nxt[i][j] = k` | **221 of 3,708** (≈6%) |

**C2** — the diagonal test agreed with an independent Bellman–Ford detector on **400 of 400** graphs.

**D1:**

| $V$ | density | $E$ | Floyd–Warshall | $V\times$Dijkstra |
| --- | --- | --- | --- | --- |
| 200 | 0.5 | 20,000 | 317 ms | **193 ms** |
| 200 | 1.0 | 39,800 | **304 ms** | 328 ms |
| 300 | 1.0 | 89,700 | **1,079 ms** | 1,080 ms |
| 400 | 1.0 | 159,600 | 2,703 ms | **2,579 ms** |

---

## A Note on What This Lab Is Really Testing

Every part of this lab has a version that runs, produces numbers, and is wrong.

- **Four of six loop orderings** give correct-looking distance matrices that are wrong about a third of
  the time.
- **One of two `nxt` conventions** gives **correct distances** and broken paths — so a test that checks
  distances passes completely.
- **The textbook's speed claim** is not reproducible in Python, and a student who reports the expected
  result without measuring will be reporting something they did not observe.

None of these is caught by "does it run" or by one small example. **B3(b) and D2(a) are the assessed
questions**, and both ask for a reason rather than a number: what the state means, and where the inner
loop executes. Those are the two questions that separate someone who has implemented an algorithm from
someone who understands it.

Part D also has a positive lesson worth taking. Floyd–Warshall is not faster here, and it is still the
right choice for many problems — five lines, negative edges handled, negative cycles free, and it
vectorises. **"Which is faster" is rarely the only question, and it is often not the important one.**

---

*CS 102 · Week 8 · Lab 8 · © CSE Department*
