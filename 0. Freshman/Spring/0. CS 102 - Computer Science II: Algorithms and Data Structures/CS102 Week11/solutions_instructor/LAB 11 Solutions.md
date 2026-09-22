# CS 102 · Lab 11 — Solutions and Checkoff Notes
## A 2-D Nearest-Neighbour Searcher

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Project 2 is due next Friday and the final exam is in Week 12.** This is the second-to-last lab and
students are stretched. Parts A and B are quick for anyone who has done PS 11; **protect the last
forty minutes for Part C**, which is the only part with a finding.

Compute cost is modest. Part C's $d = 32$ row is the slowest at roughly 40 ms per query over 200
queries — about eight seconds. Nothing needs to be started early.

**The one thing to insist on is A3 before any timing.** A pruning test written with `<=` instead of
`<`, or comparing unsquared against squared distances, produces a tree that is fast and wrong — and
every subsequent measurement then describes the wrong algorithm.

---

> **Revised 2026-09-22.** Part D (k-nearest neighbours with a bounded heap) was removed: $k$-NN search
> is never taught. Points re-weighted to keep 40.

## Part A — Build and Verify (14)

### A1 (6), A2 (5), A3 (3) — deterministic: 0 mismatches

**The three errors to check for:**

1. **Mixing squared and unsquared distances.** The pruning test compares `diff*diff` against a squared
   best distance. A student who takes a square root in one place and not the other gets a tree that
   prunes too aggressively and silently returns the wrong point.
2. **Recursing into the far side unconditionally.** Correct, and it visits every node — the tree
   becomes a slow linear scan. Their Part B node counts will be $n$, which is the giveaway.
3. **Not cycling the axis.** Splitting on $x$ at every level gives a valid BST on $x$ and no pruning
   power in $y$.

*A3 must come before B. Say so at the bench.*

---

## Part B — What It Buys in 2-D (12)

### B1 (5), B2 (4)

Mean nodes visited grows roughly **logarithmically** in $n$ — students should observe that going from
$n = 1{,}000$ to $n = 64{,}000$ (a factor of 64) increases visits by a small factor, not by 64.

Expected complexity statement: $O(\log n)$ **expected** for random points in low dimensions. *Accept
"about $\log n$"; do not require the precise average-case result, which is $O(n^{1-1/d})$ in the worst
case.*

### B3 (3)

Build time against query time. The arithmetic they should show:

$$\text{queries to break even} = \frac{\text{build time}}{\text{brute time} - \text{tree query time}}$$

Typically a few hundred queries in 2-D. *The mark is for showing the arithmetic, not the number.*

---

## Part C — The Curse of Dimensionality (14)

### C1 (6) — deterministic node counts

| $d$ | nodes visited | % of $n$ | brute | k-d tree |
| --- | --- | --- | --- | --- |
| 2 | **20** | **0.2%** | 6.75 ms | **0.02 ms** |
| 4 | 62 | 0.8% | 8.73 ms | 0.09 ms |
| 8 | 787 | 9.6% | 13.61 ms | 1.78 ms |
| **16** | **8,071** | **98.5%** | 22.49 ms | **25.06 ms** |
| 32 | 8,192 | 100.0% | 37.72 ms | 42.94 ms |

*Node counts are deterministic given the same points and queries; accept small deviations from a
different generator. **The percentages must show the same progression** — under 1% at $d \le 4$, around
10% at $d = 8$, essentially 100% by $d = 16$.*

### C2 (5) — the assessed question

**Between $d = 8$ and $d = 16$.**

Expected explanation: the pruning test asks whether the distance along **one coordinate** already
exceeds the best **total** distance found. In $d$ dimensions the total is a sum of $d$ contributions,
so a typical single coordinate accounts for roughly $1/d$ of it — and a quantity that is a small
fraction of the total almost never exceeds the total. The test stops firing, the far subtree is always
searched, and every node is visited.

*4 requires "one coordinate against the total". "The data is sparse in high dimensions" is the right
intuition without the mechanism — 2 of 4.*

### C3 (3)

**(a) (2)** **No — the tree is correct at $d = 32$.** It returns the true nearest neighbour on every
query, at every dimension; the lab's own correctness spot-checks confirm it.

What has failed is **the reason for using it**. And the implication is the one to draw out: **no test
of correctness would ever detect this.** A full test suite passes at $d = 32$. Only a measurement of
*work done* reveals that the structure has stopped earning its place.

**(b) (1)** Any of: locality-sensitive hashing, HNSW graphs, approximate nearest neighbour with an
$(1+\varepsilon)$ guarantee, dimensionality reduction (PCA / random projection) before indexing, or
simply a vectorised brute-force scan.

*(a) is the graded question of the lab. A student who answers "yes, it's incorrect" has misread their
own verification output — point at it.*

---

## Checkoff Checklist

1. A3 verified **before** any timing.
2. Squared distances used throughout — no square roots anywhere.
3. C1's percentages progress 0.2% → 9.6% → 98.5%.
4. C3(a) says the tree is **correct** at $d = 32$.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 14 |
| B | 12 |
| C | 14 |
| **Total** | **40** |

Labs are pass/fail for progression: **10 of 13 required**, and this is Lab 11. **A student who has
missed three labs must pass this one and Lab 12.** Check the register before the session and tell them
individually — Week 12 is too late.

---

## Note for the Week 12 Lecture

This is the last measurement of the course, and it is the right one to close the practical work on.

The k-d tree keeps every guarantee it ever made. It is correct at every dimension, its build is
$\Theta(n\log n)$, its query is $O(\log n)$ expected in low dimensions — nothing stated about it is
false at $d = 32$. **And it is slower than the three-line alternative it was supposed to replace.**

That is worth saying explicitly on Monday, because **Week 12 is about a different kind of limit
altogether.** This week's structure fails for a reason you can measure and fix — reduce the dimension,
use an approximate method, or scan. Week 12's problems fail for a reason nobody knows how to fix, and
the honest response is not a better algorithm but a proof that you should stop looking for one.

Two kinds of "this does not work", one week apart. **Students who can tell them apart have got what
this course was for.**

---

*CS 102 · Week 11 · Lab 11 Solutions · © CSE Department*
