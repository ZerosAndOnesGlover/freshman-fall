# CS 102 · Quiz 9

**Date:** Monday 22 March 2027 · 09:00–09:15 (start of L28) · Week 9 · 20 points
**Covers Week 8** — interval DP, LIS, coin change, tree and bitmask DP, Floyd–Warshall. **Not** this
week's material.

Closed book. Every number here is exact.

> **PROJECT 1 is due this Friday.** **MIDTERM 2 is in Week 10** and covers Weeks 5–9.

---

**Q1.** *(3)* An interval DP fills a table indexed by $[i, j]$.

- **(a)** *(2)* In what order must the table be filled, and why?
- **(b)** *(1)* What happens if you loop `for i: for j:` in the natural order — does it crash, or
  return a wrong answer?

---

**Q2.** *(3)* Matrix chain multiplication has $\Theta(n^2)$ subproblems but runs in $\Theta(n^3)$.

Where does the extra factor of $n$ come from?

---

**Q3.** *(4)* State the Floyd–Warshall recurrence, and say precisely what $d^{(k)}[i][j]$ means.

Then explain why `k` must be the outermost loop, using only your definition.

---

**Q4.** *(3)* After Floyd–Warshall, how do you detect a negative cycle?

Give the test, and say what advantage it has over the Week 5 Bellman–Ford approach.

---

**Q5.** *(4)* The $O(n\log n)$ LIS algorithm maintains an array `tails`.

- **(a)** *(2)* For the input $[1, 3, 5, 2]$, give the final `tails` array and the LIS length.
- **(b)** *(2)* Is your `tails` array an increasing subsequence of the input? Justify from your answer
  to (a).

---

**Q6.** *(3)* Greedy coin change is optimal for the UK denominations and wrong for **84 of the first
199 targets** with $[1, 5, 6, 9]$.

What property do real currencies have, and what does this tell you about testing a greedy algorithm?

---

*20 points total. Solutions posted after Wednesday's lecture.*

*CS 102 · Week 9 · Quiz 9 · © CSE Department*
