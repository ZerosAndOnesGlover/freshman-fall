# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 6: Graphs III — Minimum Spanning Trees

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 6** (released Friday, due Friday of Week 7), Lab 6, **Quiz 6 —
which covers Week 5**.

---

### Why This Week Exists

Week 5 asked for the cheapest route between two vertices. This week asks about the graph as a whole:
**connect every vertex, using as little total edge weight as possible.**

The complete graph on 50 vertices has $3.6\times10^{81}$ spanning trees — more than there are atoms in
the observable universe. **A greedy algorithm finds the best one**, and the whole content of the week
is the theorem that says greedy is allowed to work here:

> **The cut property.** For any partition of the vertices into two parts, a minimum-weight edge
> crossing that partition belongs to **some** minimum spanning tree.

Prim's algorithm and Kruskal's are the same theorem applied to two different choices of cut. They are
not competing ideas; they are one idea with two schedules.

### Learning Objectives

By the end of Week 6, you should be able to:

1. State the cut and cycle properties precisely, **including why "some" and "strictly" are
   load-bearing**, and prove the cut property by an exchange argument.
2. Say why distinct weights give a unique MST, and why the converse fails.
3. Implement Kruskal with union-find and Prim in both the heap and $\Theta(V^2)$ forms.
4. **Identify the one expression that separates Prim from Dijkstra**, and explain what it changes.
5. Explain why MST algorithms — unlike Dijkstra — need no assumption about the sign of the weights.
6. Implement union-find with union by rank and path compression, and construct the input that defeats
   the naive version.
7. State what $\alpha(n)$ is, why it is at most 4 in practice, and why it is nonetheless not constant.
8. Use an MST for bottleneck analysis and for single-linkage clustering — **and describe the failure
   mode of the latter.**
9. Reconcile a complexity comparison with a measurement that contradicts it.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L19 Spanning Trees and the Cut Property]] | The two properties, uniqueness, why greedy is safe, and what an MST is *not* |
| [[L20 Prim and Kruskal]] | Both algorithms, both proofs, and where the time actually goes |
| [[L21 Union-Find and MST Applications]] | Union-find measured, $\alpha(n)$, clustering, bottleneck |
| [[PS 6 Minimum Spanning Trees]] | 100 points, due Friday of Week 7 |
| [[CS102 Week6/assignments/QUIZ 6 Week 6 Monday\|QUIZ 6 Week 6 Monday]] | 20 points, formative — **covers Week 5** |
| [[LAB 6 Network Cable Layout]] | Campus fibre, the bottleneck, clustering, and breaking it |
| [[CS102 Week6/resources/Reading Guide Week 6\|Reading Guide Week 6]] | CLRS Ch. 21 and §19.1–19.3 |
| `solutions_instructor/` | PS 6 and Lab 6 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. The MST is not a shortest-path tree.** On a triangle with weights 2, 2, 3, the shortest route from
0 to 2 is the direct edge of weight 3 — but that edge is the heaviest on the cycle, so the cycle
property forbids it from *any* MST, and the MST path costs 4. The two problems optimise different
things. What the MST *does* guarantee is the **minimax** property: the MST path between any two
vertices minimises the maximum edge on the route, verified over 15,988 pairs with 0 mismatches.

**2. Prim is Dijkstra with one expression changed.** Dijkstra pushes the distance from the *source*;
Prim pushes the weight of the *single edge*. Dijkstra accumulates, Prim does not — and that is exactly
the difference between "how far have I come" and "what does the next connection cost". Being able to
say this in one sentence is the best single test of whether the three graph weeks have landed.

**3. $\alpha(n)$ is at most 4 for any storable input, and is not a constant.** Both halves matter.
Measured with both optimisations, the steps per operation are **1.225, 1.222, 1.234, 1.235** at
$n = 10^3$ through $10^6$ while $\log_2 n$ doubles — flat, as advertised. But $\alpha$ does grow, just
extraordinarily slowly, and the $O(m\,\alpha(n))$ bound is **tight** rather than merely the best
anyone has proved.

### Two Measurements That Contradict the Textbook

Both are real, both are explained, and neither means the analysis is wrong.

**"Kruskal for sparse, Prim for dense" failed every test.** On explicit edge lists in CPython, Kruskal
won at every size measured — including $V = 2{,}000$ with $E = 400{,}000$, where it was **3.4×**
faster. Kruskal's dominant cost is `sorted()`, which is C; Prim's inner loop is interpreted bytecode
per edge. **The advice becomes right again when the graph is implicit** — Lab 6's dense Prim beats
Kruskal by 2.9× precisely because it never builds the 79,800-edge list at all.

**"Kruskal's cost is dominated by the sort" is asymptotically true and measurably false.** The
union-find phase costs about **1.8× the sort**, stably from $E = 5{,}000$ to $E = 300{,}000$. The
complexity comparison is between $\log E$ and $\alpha(V)$ and is correct; it compares *operation
counts*, and says nothing about one phase running in C and the other in interpreted Python. The ratio
is flat rather than shrinking, which is the evidence that $\log E$ has not begun to matter. **This is
the fifth instance of that pattern this term**, and PS 6 D3 asks you to state it in general.

### A Note on the Measurements

**Counts are deterministic** — the union-find step counts, the verification totals, and every number in
Lab 6. The adversarial union-find figures are *exact*: $n(n-1)/2$ naive against $n-1$ optimised.

**Timings are not**, and this week they are unusually language-dependent. Both textbook-contradicting
results above would likely reverse in C.

### Connections

**Back:** Prim is **Week 5**'s Dijkstra with one expression changed, and uses **Week 3**'s heap with the
same lazy-deletion trick. The cut property's proof is an exchange argument, the same shape as
Dijkstra's correctness argument. Union-find's amortised bound has the structure of **Week 3**'s
linear-time `BUILD-HEAP` proof — expensive operations are rare, and each one pays for the cheap ones
after it. The clustering application uses **Week 2**'s sorting.

**Forward:** **Week 7** changes subject to dynamic programming, and the bridge is Bellman–Ford, which
was already a DP. **Week 9** formalises the exchange argument as the standard proof technique for
greedy algorithms — this week's cut property is the worked example. **Week 11** returns to geometric
graphs for closest-pair and $k$-d trees. **Week 12** uses the MST to build a 2-approximation for the
travelling salesman problem, and explains why an exact solution is out of reach.

---

*CS 102 · Week 6 · © CSE Department*
