# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 8: Dynamic Programming II — Applications

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 8** (released Fri 19 Mar 10:00, due **Fri 26 Mar 17:00**), Lab 8 (**Tue 23 Mar**, 15:00), **Quiz 8** (Mon 15 Mar, 09:00) — which covers Week 7.
**PROJECT 1 is due Friday 26 March, 17:00** — the same day as PS 8. **This is the heaviest week of the
term.** Prioritise the project; the problem set says so explicitly.

---

### Why This Week Exists

Week 7 gave you the technique. This week gives you the thing that does not come from reading: **six
more state designs**, chosen because each teaches something different.

| problem | state | what it teaches |
| --- | --- | --- |
| matrix chain | interval $[i,j]$ | split on the **last** operation |
| optimal BST | interval $[i,j]$ | the cost term accounting for depth |
| longest increasing subsequence | "ending at $i$" | the *suffix* of the decision matters |
| coin change | remaining amount | greedy needs a proof |
| DP on trees | vertex + flag | the recursion order is handed to you |
| bitmask TSP | subset + position | order is irrelevant, membership is not |
| Floyd–Warshall | allowed intermediates | the state nobody guesses |

**None of these is deducible from the problem statement, and all of them are obvious afterwards.**
That asymmetry is what makes DP feel hard, and the only cure is having seen enough.

### Learning Objectives

By the end of Week 8, you should be able to:

1. Recognise interval DP, write the split recurrence, and **fill the table by increasing interval
   length**.
2. Reconstruct a parenthesisation from a split table.
3. Explain why an optimal BST is generally unbalanced, and reconcile that with Week 2.
4. Write LIS both ways, and explain why the fast version's `tails` array is not an answer.
5. Give a coin system where greedy fails, and say what property real currencies have that makes it
   work.
6. Write DP on a tree with an explicit postorder, and say why the same problem is NP-complete on a
   general graph.
7. Encode a subset as a bitmask and reduce $n!$ to $2^n$ — **without claiming the problem is now
   tractable**.
8. State what $d^{(k)}[i][j]$ means and derive Floyd–Warshall's loop order from it.
9. Detect negative cycles from the diagonal, and reconstruct paths correctly.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L25 Interval DP Matrix Chain and Optimal BSTs]] | The interval family, and why balance is the wrong objective here |
| [[L26 Sequences Trees and Bitmasks]] | LIS, coin change, tree DP, bitmask TSP |
| [[L27 Floyd-Warshall and All-Pairs Shortest Paths]] | The state, the loop order, negative cycles, and semirings |
| [[PS 8 Dynamic Programming II]] | 100 points, due Fri 26 Mar 17:00 |
| [[CS102 Week8/assignments/QUIZ 8 Week 8 Monday\|QUIZ 8 Week 8 Monday]] | 20 points, formative — **covers Week 7** |
| [[LAB 8 Implementing Floyd-Warshall]] | Five lines, and four ways to get them wrong |
| [[CS102 Week8/resources/Reading Guide Week 8\|Reading Guide Week 8]] | CLRS §14.2, §14.5, §23.2 |
| `solutions_instructor/` | PS 8 and Lab 8 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. Floyd–Warshall's loop order is not a convention.** `k` must be outermost. Measured over all six
orderings on 200 random graphs each: the two with `k` outside are correct; the other four are wrong on
**70 to 78** of 200 — about a third of the time. Every one of them produces a complete, plausible
distance matrix. The reason is entirely in what $d^{(k)}$ *means*: level $k+1$ reads all of level $k$,
so level $k$ must be finished first.

**2. An optimal BST is generally unbalanced, and Week 2 was not wrong.** With
$p = [0.7, 0.1, 0.1, 0.1]$ the balanced tree costs **2.000** expected comparisons and the optimum
costs **1.500** — balanced is 33% worse. Week 2 knew nothing about the queries and minimised the worst
case; here the distribution is known and the objective is the average. **Different information,
different objective.**

**3. Greedy coin change is correct on every real currency and wrong 42% of the time on
$[1,5,6,9]$.** It fails for **84** of the first 199 targets, smallest at $T=11$ where greedy takes
$9{+}1{+}1$ and the optimum is $5{+}6$. Real currencies are *canonical* by design — a property of the
denominations, not of the algorithm. This is Week 9's opening question, one week early.

### Two Bugs That Produce Correct-Looking Output

**The path that is not a path.** Floyd–Warshall's `nxt` matrix must store `nxt[i][k]`, not `k`. Storing
`k` gives **identical distances** and broken paths — 221 invalid reconstructions of 3,708 (≈6%). A test
that checks distances passes completely.

**The array that is not a subsequence.** Fast LIS's `tails` array has the right length and is generally
**not** an increasing subsequence of the input — measured, **47%** of random arrays. The smallest
counterexample is `[2,3,1]`, whose `tails` is `[1,3]`. Recovering a real LIS needs predecessor
pointers, which is the third time this term that a space optimisation has cost the answer.

### A Measurement That Contradicts the Textbook

On a dense graph, Floyd–Warshall's $\Theta(V^3)$ should beat $V\times$Dijkstra's $O(V^3\log V)$.
Measured, they are **within about 10% even on the complete graph**, trading places run to run —
because Floyd–Warshall's triple loop is interpreted and Dijkstra's work happens inside `heapq`, which
is C.

**This is the sixth instance of that pattern this term**, and by now the reason should be predictable.
Use Floyd–Warshall for what it does — negative edges, free cycle detection, five lines — not for its
exponent.

### Connections

**Back:** The interval recurrence's exchange-style justification is **Week 6**'s cut property. Optimal
BSTs answer the question **Week 2** deferred. Floyd–Warshall's negative-cycle test replaces **Week 5**'s
virtual-source construction. The $(\min,\max)$ semiring computes exactly the minimax quantity **Week
6** obtained from the MST — verified to agree on 250 of 250 graphs. The "ending at $i$" state is
**PS 7 E2**.

**Forward:** **Week 9** abandons tables entirely — greedy makes one choice and never revisits it,
which is faster whenever it works, and the week is about proving that it does. Coin change is its
opening example. **Week 10**'s KMP failure function is a DP over pattern positions. **Week 11**'s
segment trees revisit interval decomposition. **Week 12** returns to TSP as the canonical NP-hard
problem, with Week 6's MST supplying the 2-approximation.

---

*CS 102 · Week 8 · © CSE Department*
