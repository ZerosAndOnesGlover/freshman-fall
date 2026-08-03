# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 7: Dynamic Programming I — Principles

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 7** (released Friday, due Friday of Week 8), Lab 7, **Quiz 7 —
which covers Week 6**.
**PROJECT 1 is assigned this week** and due Friday of Week 9. **10% of the course** — the largest
single piece of work this term. See `assignments/PROJECT 1 A Working Diff.md`.

---

### Why This Week Exists

Dynamic programming has a reputation for difficulty that it does not deserve, and the reason is that
it is usually introduced as a technique rather than as a definition. The definition is one sentence:

> **Dynamic programming is recursion in which you do not recompute anything.**

You already wrote one. **Bellman–Ford** is a dynamic program — subproblems indexed by edge count, each
defined from smaller ones, evaluated bottom-up in place. It needed no ordering argument and no greedy
insight; it worked by solving every subproblem once. This week names that and makes it deliberate.

Two conditions decide whether it applies, and **knowing which one a problem lacks tells you what to do
instead**:

| | optimal substructure | overlapping subproblems | technique |
| --- | --- | --- | --- |
| merge sort | yes | **no** | divide and conquer |
| Fibonacci, LCS, knapsack | yes | yes | **DP** |
| longest simple path | **no** | yes | NP-complete (Week 12) |

### Learning Objectives

By the end of Week 7, you should be able to:

1. State both conditions for DP, and give a problem failing each.
2. Convert a recurrence into a memoised and a tabulated implementation without further thought.
3. **Choose between memoisation and tabulation from the shape of the subproblem graph**, not by
   preference.
4. Write the LCS and edit-distance recurrences from scratch, including base cases, and recover the
   solution by traceback.
5. State precisely how LCS and edit distance are related, and where the relation breaks.
6. Reduce a 2-D table to a rolling row, and say what that costs you.
7. Write the 0/1 knapsack recurrence, and explain why the loop must descend.
8. **Explain why $\Theta(nW)$ is not polynomial**, and why that does not contradict NP-completeness.
9. Choose the state for a problem you have not seen — the actual skill, and the one that requires
   practice.

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L22 Optimal Substructure and Memoisation.md` | The two conditions, Fibonacci, memoisation vs tabulation measured |
| `lectures/L23 Longest Common Subsequence and Edit Distance.md` | Both recurrences, traceback, space, and how they relate |
| `lectures/L24 Knapsack and Choosing the State.md` | Knapsack, pseudo-polynomiality, and a checklist for state design |
| `assignments/PS 7 Dynamic Programming.md` | 100 points, due Friday of Week 8 |
| `assignments/QUIZ 7 Week 7 Monday.md` | 20 points, formative — **covers Week 6** |
| `assignments/PROJECT 1 A Working Diff.md` | **10% of the course**, due Friday of Week 9 |
| `lab/LAB 7 Visualising DP Tables.md` | Print the tables, trace them, and measure the two techniques |
| `resources/Reading Guide Week 7.md` | CLRS §14.1–14.4, with §14.3 flagged as the section that matters |
| `solutions_instructor/` | PS 7 and Lab 7 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. Memoisation and tabulation do not do the same amount of work.** They have the same complexity, so
textbooks present the choice as stylistic. Measured on 0/1 knapsack with weights that are multiples of
1,000: top-down computes **161** subproblems where bottom-up fills **200,020** — a factor of
**1,242×**. On LCS the same comparison gives **1.39×**, and tabulation wins on the clock. The
deciding property is **what fraction of the state space is reachable**, and it is visible only if you
look at the subproblem graph.

**2. $\Theta(nW)$ is not polynomial.** The input contains $W$ written in $\log_2 W$ bits, so the
running time is exponential in the input *size*. Measured at $n=30$: $W$ from 10,000 to 100,000 takes
71 ms to 742 ms. **Add one bit to $W$ and the running time doubles.** This is why 0/1 knapsack can be
NP-complete and have this algorithm at the same time.

**3. Rolling the table down to two rows destroys the traceback.** You get the length and not the
answer. That is not a technicality — it is the reason **Hirschberg's algorithm** exists, and it is
Project 1's third part. Measured: 139× less memory for 1.18× the time.

### One Bug and One Beautiful Number

**The one-character bug.** In the rolled knapsack, the inner loop must run **downwards**. Run it
upwards and `dp[w - wi]` has already been updated in this row, so the item can be taken repeatedly.
The result is not broken — it correctly solves the **unbounded** knapsack, and differs from 0/1 on
**258 of 300** random instances. Two different problems, one character apart, both returning plausible
numbers.

**The beautiful number.** Computing `fib(20)` naively makes 21,891 calls to solve 21 distinct
subproblems. How many times is `fib(1)` evaluated? **6,765** — which is $F(20)$. The identity is that
`fib(k)` is evaluated exactly $F(n-k+1)$ times. **The redundancy of naive Fibonacci is itself
Fibonacci.**

### A Note on the Measurements

**Counts are deterministic** — call counts, subproblem counts, all verification totals. The Fibonacci
call identity and the subproblem identity are *exact*, not approximate.

**Timings are not.** Note in particular that memoisation and tabulation differ by about 6× on
Fibonacci despite identical complexity, for the ordinary reasons: function calls and dictionary
hashing against array indexing.

### Connections

**Back:** **Week 5**'s Bellman–Ford was a dynamic program over subproblems indexed by edge count, and
its optimal-substructure argument — subpaths of shortest paths are shortest paths — is this week's
first condition. The exchange argument justifying the greedy match in LCS is the shape of **Week 6**'s
cut property. **Week 0**'s doubling-ratio method reads the pseudo-polynomial table in Lecture 24 §2.

**Forward:** **Week 8** is five more DP problems and is entirely about state design — matrix chain,
optimal BSTs, LIS, coin change, DP on trees and bitmasks, and Floyd–Warshall, whose state ("which
vertices may be intermediates") nobody guesses first. **Week 9** does the opposite: greedy makes one
choice and never revisits it, which is faster when it works, and Week 9 is about proving when.
**Week 10**'s KMP is a DP over pattern positions. **Week 12** explains why knapsack's
pseudo-polynomial algorithm is exactly what NP-completeness predicts.

---

*CS 102 · Week 7 · © CSE Department*
