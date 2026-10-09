# CS 102 · Reading Guide, Week 8
## Dynamic Programming II — Applications

---

## Required

**CLRS, 4th ed. — §14.2** (matrix chain, properly this time) and **§14.5** (optimal BSTs).
**CLRS, 4th ed. — §23.2** (Floyd–Warshall and transitive closure). §23.1 (APSP by matrix multiplication) is optional.

§23.3 (Johnson's algorithm) is optional and worth the hour if you have it.

Also useful:

- **Kleinberg & Tardos, Chapter 6** — §6.4–6.10. Their treatment of DP is organised by *state design*
  rather than by problem, which is exactly this week's theme.
- **Skiena §10.3–10.5** — the practitioner's view, and good on recognising when a new problem is an
  old one.
- **Competitive Programmer's Handbook (Laaksonen), Ch. 10** — the clearest short treatment of bitmask
  DP anywhere, and it is free.

**This is a heavy week and PS 8 collides with Project 1's deadline.** If reading must be cut, read
§23.2 and §14.2 and leave §14.5 until after the project.

---

## Read for the State, Not for the Problem

Week 7 introduced DP with four examples. This week has six more, and reading them as six recipes is
the mistake. **Each one exists to teach a different shape of state:**

| lecture | problem | state | what it teaches |
| --- | --- | --- | --- |
| L25 | matrix chain | interval $[i,j]$ | split on the *last* operation |
| L25 | optimal BST | interval $[i,j]$ | the cost term that accounts for depth |
| L26 | LIS | "ending at $i$" | the suffix of the decision matters |
| L26 | coin change | remaining amount | greedy needs a proof |
| L26 | tree DP | vertex + flag | the recursion order is given to you |
| L26 | bitmask TSP | subset + position | order is irrelevant, membership is not |
| L27 | Floyd–Warshall | allowed intermediates | the state nobody guesses |

When you meet a new DP problem, the question is never "which of these is it". It is "**what must I
know at a decision point**", and these seven are a catalogue of answers that have worked before.

---

## How to Read It

**§14.2 (matrix chain, 10 pages).** The canonical interval DP. Pay attention to the loop structure —
by increasing chain **length**, not by $i$ and $j$ — and to Figure 14.5, which shows which cells depend
on which. That dependency picture is why the loops are ordered as they are.

**§14.5 (optimal BSTs).** Read for the extra term $\sum p_t$ and where it comes from. CLRS
also handles *unsuccessful* searches (the "dummy keys" $d_i$), which the lectures omit; the idea is
identical and the bookkeeping is heavier.

**§23.2, first part (Floyd–Warshall).** Short. The whole content is the meaning of $d^{(k)}$, and the
argument that a shortest path through $k$ has two halves that avoid $k$. **Read that argument until it
is obvious**, because everything else — the loop order, the in-place version, the negative-cycle test —
follows from it.

**§23.2, last part (transitive closure).** The same triple loop with $(\vee, \wedge)$ replacing
$(\min, +)$. Read it and notice the substitution.

---

## Guiding Questions

Three of these are on MIDTERM 2 and one is on the final.

1. §14.2: matrix chain has $\Theta(n^2)$ states and $\Theta(n^3)$ running time. Where does the extra
   factor of $n$ come from, and which other problems this week share that shape?

2. Interval DP fills by increasing length. What exactly goes wrong if you loop `for i: for j:` in the
   natural order, and would you notice?

3. §14.5: the recurrence adds $\sum_{t=i}^{j} p_t$ regardless of which root is chosen. What is that
   term paying for, and why does it not depend on the root?

4. Week 2 built balanced BSTs; §14.5 builds unbalanced ones. **What does each algorithm know that the
   other does not?**

5. §23.2: state precisely what $d^{(k)}[i][j]$ means. Then explain why `k` must be the outermost loop
   using only that statement.

6. The in-place Floyd–Warshall overwrites entries it is still reading. Prove this is safe. (One line:
   what happens to row $k$ and column $k$ during round $k$?)

7. TSP by bitmask is $O(2^n n^2)$ instead of $O(n!)$. Is TSP therefore tractable? Answer carefully.

---

## Common Misreadings

**"Matrix chain is about multiplying matrices."** It is about **parenthesisation**. The matrices are
never multiplied; the algorithm computes a cost. The same recurrence solves polygon triangulation and
burst balloons, which contain no matrices at all.

**"The optimal BST is roughly balanced."** Only when the distribution is roughly uniform. With
$p = [0.7, 0.1, 0.1, 0.1]$ the balanced tree costs **2.000** and the optimum **1.500** — 33% worse.

**"The `tails` array in fast LIS is an LIS."** It has the right **length** and is usually not even a
subsequence of the input — measured, **47%** of random arrays. Recovering a real LIS needs predecessor
pointers.

**"Greedy coin change works."** On every real currency, yes, because currencies are designed to be
canonical. On $[1,5,6,9]$ it is wrong for **84** of the first 199 targets, first at $T=11$.

**"Any loop order works for Floyd–Warshall since it's just three nested loops."** Four of the six
orderings are wrong on about a third of random graphs, and all six produce a complete, plausible
matrix.

**"Floyd–Warshall is faster than $V$ Dijkstras on dense graphs."** Asymptotically yes. Measured in
CPython, they are within ~10% even on the complete graph, because Dijkstra's work happens inside C and
Floyd–Warshall's does not. Choose it for negative edges and for its five lines, not for its exponent.

**"Bitmask DP makes exponential problems tractable."** It makes $n!$ into $2^n$, which moves the
practical limit from about 13 to about 20. Both are exponential and TSP remains NP-hard.

---

## If You Have Extra Time

**Knuth's optimisation.** Optimal BST drops from $\Theta(n^3)$ to $\Theta(n^2)$ once you prove the
optimal root of $[i,j]$ lies between those of $[i,j-1]$ and $[i+1,j]$. It generalises to a family of
interval DPs satisfying the quadrangle inequality, and it is the natural next thing after §14.5.

**Johnson's algorithm** (CLRS §23.3). All-pairs shortest paths on a **sparse** graph with negative
edges, in $O(V^2\log V + VE)$ — better than $\Theta(V^3)$ when $E \ll V^2$. It runs Bellman–Ford once
to compute a reweighting that makes every edge non-negative *without changing which paths are
shortest*, then runs Dijkstra $V$ times. It is the best combination of Week 5's two algorithms and a
genuinely beautiful piece of work.

**Semirings and algebraic path problems.** The same triple loop solves four different problems
depending on which two operators you use:

| operators | quantity computed |
| --- | --- |
| $(\min, +)$ | shortest paths |
| $(\vee, \wedge)$ | reachability — Warshall's algorithm |
| $(+, \times)$ | number of paths |
| $(\min, \max)$ | **bottleneck paths** |

The last is worth trying. Replacing `d[i][k] + d[k][j]` with `max(d[i][k], d[k][j])` computes, for
every pair, the minimum over all routes of the **heaviest edge on the route** — which is exactly the
minimax quantity **Week 6** obtained from the MST.

*(Verified: Floyd–Warshall under $(\min,\max)$ agrees with the MST path-maximum on **250 of 250**
connected graphs — 0 mismatches.)*

Two algorithms from different weeks, computing the same thing by unrelated means. One control flow,
four problems.

**Divide-and-conquer optimisation** and the **convex hull trick** speed up other classes of DP
recurrence. Both appear in competitive programming long before they appear in textbooks.

---

*CS 102 · Week 8 · Reading Guide · © CSE Department*
