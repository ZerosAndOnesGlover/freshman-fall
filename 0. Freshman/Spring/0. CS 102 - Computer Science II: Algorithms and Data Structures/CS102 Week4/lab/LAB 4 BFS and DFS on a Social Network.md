# CS 102 · Lab 4
## BFS and DFS on a Social Network

**Date:** Tuesday 23 February 2027 · 15:00–16:50 · Lab section (Week 5) — covers Week 4 (L13–L15)
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab4.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 13 labs to pass the course.** See the syllabus.

---

## Purpose

Every graph you have seen so far was random. Real networks are not random, and the difference changes
what the algorithms do.

This lab builds a synthetic social network with the statistical properties real ones have — a few
very well-connected people, most people with a handful of connections — and then uses BFS to measure
"degrees of separation" on it.

**It ends with a heuristic that gives the wrong answer**, and asks you to notice.

---

## Part A — Build the Network (8 pts)

**A1.** *(5)* Implement `ba_graph(n, m, seed)`, a **preferential-attachment** network:

- Start with $m$ vertices, fully connected.
- Add vertices $m, m+1, \dots, n-1$ one at a time. Each new vertex picks $m$ **distinct** existing
  vertices to connect to, chosen with probability proportional to their current degree.

The standard way to sample proportional to degree is to keep a list `rep` in which each vertex appears
once per incident edge, and choose uniformly from it. **To make everyone's graph identical**, do it
exactly this way:

- Build the starting clique with `for i in range(m): for j in range(i+1, m):`, adding edge $i$–$j$
  and appending `i` then `j` to `rep`.
- For each new vertex `v`, draw `rep[random.randint(0, len(rep) - 1)]` repeatedly, skipping any
  target already chosen, until you have $m$ targets. Keep them **in the order drawn**.
- Add the edges in that order (append `u` to `adj[v]` and `v` to `adj[u]`). Then extend `rep` with
  the $m$ targets in that order, then with `v` repeated $m$ times.

`random.randint` is the one random function CS 101 taught; nothing else from `random` is needed.

Use `random.seed(seed)` at the start so your graph is reproducible.

**A2.** *(3)* Build the network with `n=5000, m=3, seed=42` and report:

- $V$, $E$, mean degree;
- the number of connected components;
- maximum, minimum, and median degree;
- the ten largest degrees.

**Check against the reference table below before continuing.** If your numbers differ, your generator
differs, and every later part will disagree.

---

## Part B — Degrees of Separation (12 pts)

**B1.** *(4)* BFS from vertex 0, visiting neighbours in adjacency-list order. Report its **eccentricity** (the largest distance to any vertex), the
mean distance from vertex 0, and the **size of each BFS level**.

**B2.** *(4)* The level sizes are not symmetric — they grow, peak, and then collapse. Explain both
halves of that shape in two or three sentences.

**B3.** *(4)* Compute the **exact diameter**: run BFS from every vertex and take the largest
eccentricity. Report the diameter, the **radius** (the smallest eccentricity), the mean distance over
all ordered pairs, and the full distribution of eccentricities.

> This is 5,000 BFS runs and takes about **8 seconds** on the reference machine. It is not the slow
> part of this lab.

---

## Part C — The Double-Sweep Heuristic (10 pts)

Computing an exact diameter costs $V$ BFS runs. The standard cheap alternative is the **double
sweep**:

1. BFS from an arbitrary vertex $s$; let $a$ be a farthest vertex from $s$ (the smallest-numbered one
   if several tie).
2. BFS from $a$; let $b$ be a farthest vertex from $a$ (again the smallest-numbered).
3. Report $\mathrm{dist}(a, b)$.

Two BFS runs instead of $V$.

**C1.** *(3)* Implement it. Starting from vertex 0, report $a$, $b$, and the estimate.

**C2.** *(3)* Compare with your exact diameter from B3. **Do they agree?**

**C3.** *(4)* Using your eccentricity distribution from B3, explain the result quantitatively:

- How many vertices have eccentricity equal to the true diameter?
- What does that imply about the chance a double sweep lands on one?
- Is the double sweep's answer an upper bound on the diameter, a lower bound, or neither? **Justify
  this** — do not guess.

> **C3 is the assessed part of this lab.** The heuristic is genuinely useful and genuinely wrong here,
> and being able to say precisely which kind of wrong is the skill.

---

## Part D — BFS Against DFS (10 pts)

**D1.** *(4)* Run Lecture 15's `dfs_iter` from vertex 0 — push every unseen neighbour, pop LIFO — with
each stack entry carrying a depth one more than the vertex that pushed it, and record each vertex's
depth when it is first popped. That is its depth in the DFS tree.
Report the maximum DFS depth alongside the BFS eccentricity from B1.

**D2.** *(3)* You should find the DFS depth is larger by roughly three orders of magnitude. Explain
why, and state which of the two trees — if either — has any claim to being optimal.

**D3.** *(3)* Now try a **recursive** DFS on the same network. Report what happens.

Then answer: the network's *diameter* is 7, so no two people are more than 7 steps apart. **Why does a
recursive traversal of it exceed a recursion limit of 1,000?** One sentence, and be precise about
which quantity bounds the stack depth.

---

## Submission

- `lab4.py` — runnable end to end, producing every table.
- `RESULTS.md` — all tables and answers. **Include your machine and Python version**, as in Lab 0.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 8 | A correct, reproducible generator |
| B | 12 | BFS, level structure, exact diameter |
| C | 10 | The heuristic, and what kind of wrong it is |
| D | 10 | BFS against DFS, and the recursion limit |
| **Total** | **40** | |

---

## Reference Numbers

`n=5000, m=3, seed=42`, Python 3.14 on x86-64 Linux. **These are deterministic** — if your generator
matches the specification, every number below should match exactly.

**A2 — the network**

| quantity | value |
| --- | --- |
| $V$ | 5,000 |
| $E$ | 14,994 |
| mean degree | 6.00 |
| components | **1** |
| max degree | 192 |
| min degree | 3 |
| ten largest degrees | 192, 181, 166, 162, 151, 124, 120, 111, 111, 109 |
| vertices of degree 3 | 2,024 |

**B1 — BFS from vertex 0**

| level | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| vertices | 1 | 181 | 1,682 | 2,858 | 278 |

Eccentricity of vertex 0: **4**. Mean distance from vertex 0: **2.647**.

**B3 — exact**

| quantity | value |
| --- | --- |
| diameter | **7** |
| radius | 4 |
| mean distance, all ordered pairs | 4.0236 |
| eccentricity distribution | 4: 8 vertices, 5: 1,541, 6: 3,415, **7: 36** |

**C1 — double sweep from vertex 0**

$a = 549$ (eccentricity 6), $b = 2988$, estimate **6**.

**D1, D3 — DFS**

| quantity | value |
| --- | --- |
| BFS eccentricity from vertex 0 | 4 |
| **iterative DFS tree depth from vertex 0** | **3,274** |
| ratio | 818× |
| recursive DFS on this network | **`RecursionError`** |

The DFS depth is deterministic given the generator, because it depends on the order neighbours appear
in each adjacency list. If yours differs, check that you append in the order the specification
describes.

---

## A Note on What This Lab Is Really Testing

Vertex 0 is one of the three founding vertices, so it is a hub: its mean distance to everyone is
**2.647** while the network-wide mean is **4.0236**. Starting a measurement there gives an
unrepresentative answer, and the double sweep starts there.

The heuristic then returns 6 against a true diameter of 7. **It is not badly wrong — it is wrong by
one, in a predictable direction, for a reason you can quantify**: only 36 of 5,000 vertices achieve
eccentricity 7, so a procedure that examines two of them is unlikely to find one.

That is the shape of a good heuristic, and knowing its failure direction is what makes it safe to use.
An engineer who reports "the diameter is 6" has made an error. One who reports "the diameter is at
least 6, and this method can only understate it" has reported a fact.

**Part C3 asks for the second sentence.** Weeks 9 and 12 return to this repeatedly — greedy algorithms
and approximation algorithms are both, in the end, about knowing which way your answer is wrong.

---

*CS 102 · Week 4 · Lab 4 · © CSE Department*
