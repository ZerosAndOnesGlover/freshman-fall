# CS 102 · Computer Science II
## Lecture 39: Approximation Algorithms

**Date:** Friday 9 April 2027 · 09:00–09:50 · Week 12

---

## 1. Giving Up the Right Thing

A problem is NP-complete. You still have to ship something. Four things can be relaxed, and the whole
of practical algorithm design is choosing which:

| give up | you get | what it costs |
| --- | --- | --- |
| **speed** | exact answers | works to $n \approx 20$ for TSP |
| **generality** | exact and fast | only on restricted inputs — DAGs, trees, small $W$ |
| **optimality** | fast, with a **proven** ratio | **approximation algorithms** |
| **guarantees** | fast, often excellent | **heuristics** — no bound at all |

**The last two rows look similar and are completely different**, and telling them apart is what this
lecture is for.

> An algorithm is a **$\rho$-approximation** if for **every** input it returns a solution within a
> factor $\rho$ of optimal — and that is **proved**, not observed.

---

## 2. Vertex Cover: 2-Approximation

**Problem.** Smallest set of vertices touching every edge. NP-complete.

The algorithm is almost embarrassing:

```python
def vertex_cover_approx(edges):
    cover = set()
    for u, v in edges:
        if u not in cover and v not in cover:
            cover.add(u); cover.add(v)          # take BOTH endpoints
    return cover
```

**Take both endpoints of any uncovered edge.** It does not even look at the degrees.

### Why it is within 2×

The edges that triggered an addition form a **matching** — no two share a vertex. Any cover must
contain at least one endpoint of each matched edge, so

$$\mathrm{OPT} \ge |M|.$$

Our cover has exactly $2|M|$ vertices. Therefore $|C| = 2|M| \le 2\,\mathrm{OPT}$. $\square$

**Three lines, and the bound is tight** — a single edge forces 2 against an optimum of 1.

*(Verified over 2,000 random graphs against exact vertex cover: worst ratio exactly **2.000**, and **0**
violations of the bound.)*

### The intuitive algorithm has no such bound

Everyone's first idea is greedy: repeatedly take the **highest-degree** vertex. It is more
sophisticated, it looks smarter, and on random graphs it does better:

| algorithm | worst ratio over 2,000 random graphs |
| --- | --- |
| matching-based 2-approximation | **2.000** |
| highest-degree greedy | **1.500** |

*(Verified.)* **The unproven algorithm won the sample.**

Now the instance the proof warned about — a bipartite graph with $k$ left vertices and right groups of
sizes $k/2, k/3, \dots$ arranged so greedy prefers the right side:

| $k$ | optimal | greedy | ratio |
| --- | --- | --- | --- |
| 8 | 8 | 12 | 1.50 |
| 16 | 16 | 34 | 2.12 |
| 32 | 32 | 87 | 2.72 |
| 64 | 64 | 216 | 3.38 |
| 128 | 128 | **517** | **4.04** |

*(Verified.)* The ratio tracks $H_k \approx \ln k$ — **greedy is $\Theta(\log n)$-approximate, and
unboundedly worse than the ugly algorithm.** At $k = 64$ the matching method returns 128 and greedy
returns 216.

> **This is the closing argument of the course.** The intuitive algorithm looked better on every
> instance anyone would generate casually, and is arbitrarily worse on the instance the proof
> predicts. **The three-line algorithm with a theorem is the one you ship**, and the reason is not that
> it performs better — it is that you know what it will do on input you have not seen.

---

## 3. Metric TSP: the MST 2-Approximation

**Problem.** Shortest tour visiting every city. NP-hard.

Assume the **triangle inequality** — $d(a,c) \le d(a,b) + d(b,c)$ — which any distance derived from
actual geometry satisfies. Then:

1. Build a **minimum spanning tree** (Week 6).
2. Walk it in preorder, **shortcutting** past cities already visited.

```python
def tsp_approx(n, D):
    tree = mst(n, D)                     # Week 6's Prim
    tour = preorder_walk(tree)           # each edge twice
    return shortcut(tour)                # skip repeats
```

### Why it is within 2×

Three steps, each one line:

1. **$\mathrm{MST} \le \mathrm{OPT}$.** Delete any edge from an optimal tour and you have a spanning
   path — a spanning tree. So the minimum spanning tree is no heavier than the optimal tour.
2. **The full walk costs $2 \cdot \mathrm{MST}$**, traversing every tree edge twice.
3. **Shortcutting does not increase the cost** — by the triangle inequality, going directly is no
   longer than going via a visited city.

$$\mathrm{tour} \le 2\cdot\mathrm{MST} \le 2\cdot\mathrm{OPT}. \qquad\square$$

*(Verified on 300 metric instances against exact Held–Karp: worst ratio **1.3509**, **0** violations of
the 2× bound. And $\mathrm{MST}/\mathrm{OPT}$ reached at most **0.8286**, consistent with step 1.)*

### Step 3 is load-bearing

Drop the triangle inequality and the guarantee dies:

*(Verified: on 2,000 **non-metric** instances with random edge weights, the worst ratio was **4.000**
and the 2× bound was **exceeded in 42 cases**.)*

**The algorithm is unchanged; only the input assumption is gone.** And that is not a technicality —
without the triangle inequality, TSP has **no** constant-factor approximation unless P = NP.

> That is the strongest form of the course's recurring lesson. It is not that the bound gets worse
> without the assumption. It is that **no bound of that kind can exist**, and the theorem says so.

### Better is possible

**Christofides' algorithm** (1976) achieves **1.5** by adding a minimum-weight perfect matching on the
odd-degree vertices instead of doubling every edge. It stood as the best known ratio for metric TSP for
**forty-five years**, until a 2020 result improved it by about $10^{-36}$.

---

## 4. Heuristics: Excellent, and Unbounded

**2-opt** repeatedly removes two tour edges and reconnects the other way if that is shorter.

Measured on 200 metric instances, starting from the MST tour:

| method | mean ratio | worst ratio | found the optimum |
| --- | --- | --- | --- |
| MST 2-approximation | 1.1145 | 1.3205 | — |
| **+ 2-opt** | **1.0051** | **1.1290** | **167 of 200** |

*(Verified.)*

**2-opt found the exact optimum in 84% of instances and averaged half a per cent above it.** It is
dramatically better than the algorithm with the theorem.

**And it has no approximation guarantee whatsoever.** There are instances where 2-opt's local optimum
is arbitrarily bad, and no amount of measurement will tell you whether your input is one of them.

| | approximation algorithm | heuristic |
| --- | --- | --- |
| typical quality | often mediocre | often excellent |
| worst case | **proved** | unknown, possibly unbounded |
| tells you | what it will *never* do | what it usually does |

**Ship both.** Run the approximation to get a bound, run the heuristic to get a good answer, and report
the heuristic's result *with* the approximation's guarantee as a sanity check. That is what production
solvers do.

---

## 5. The Landscape of Approximability

Not all NP-complete problems are equally approximable, and this is the genuinely surprising part —
problems that are equivalent for *exact* solution differ enormously for *approximate* solution.

| problem | best known approximation |
| --- | --- |
| **Knapsack** | **any** $1+\varepsilon$ — a PTAS |
| Metric TSP | 1.5 (Christofides) |
| Vertex cover | 2 |
| Set cover | $\ln n$ — and **no better is possible** unless P = NP |
| Max clique | $n^{1-\varepsilon}$ — essentially nothing |
| **General TSP** | **no constant factor possible** unless P = NP |

Knapsack and max clique are both NP-complete. One admits an arbitrarily good approximation; the other
admits essentially none. **NP-completeness says how hard they are to solve exactly, and nothing at all
about how hard they are to approximate.**

The lower bounds here — "no better is possible" — are theorems, from the PCP theorem and the theory of
inapproximability. **They are the reason this is a real subject rather than a collection of tricks**:
they tell you when to stop improving your ratio, just as NP-completeness tells you when to stop looking
for an exact algorithm.

---

## 6. Where the Course Ends

Twelve weeks ago the question was *how do I make this faster*. It is now a more precise set of
questions, and you can answer all of them:

- **Is there a fast algorithm?** — complexity analysis, Weeks 0–11.
- **Is there a fast algorithm *at all*?** — NP-completeness, Lecture 38.
- **If not, what do I give up?** — this lecture.
- **What does my answer guarantee?** — the question the whole course has been building toward.

That last one is the thesis, and it has appeared every week in a different disguise: Dijkstra
guarantees a shortest path *given non-negative weights*; Kruskal guarantees an MST *given the cut
property*; Huffman guarantees an optimal code *given independent symbols and integer bits*; a k-d tree
guarantees the true nearest neighbour *and stops being worth using* past ten dimensions; a convex hull
guarantees the right polygon *given exact arithmetic*.

**Every algorithm in this course is correct under an assumption.** Knowing what your algorithm
guarantees, and what it assumed to guarantee it, is what the subject actually consists of.

---

## 7. What to Do

- Read CLRS Chapter 35 — §35.1 (vertex cover), §35.2 (TSP), §35.3 (set cover), §35.5 (subset-sum and
  the PTAS).
- **Lab 12** implements §3 and §4 and measures both.
- **PROJECT 2 and PS 11 are due Friday.**
- **The FINAL EXAM is this week and is comprehensive.** See
  `resources/FINAL EXAM Revision Guide.md`.
- And when you are done: `resources/Course Retrospective.md`.

---

*CS 102 · Week 12 · Lecture 39 · © CSE Department*
