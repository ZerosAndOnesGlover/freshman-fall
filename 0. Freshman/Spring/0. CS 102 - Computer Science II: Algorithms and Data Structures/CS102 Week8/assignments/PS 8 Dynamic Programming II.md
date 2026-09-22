# CS 102 · Problem Set 8
## Dynamic Programming II — Applications

**Released:** Friday 19 March 2027, 10:00 (after L27) · Week 8
**Due:** Friday 26 March 2027, 17:00 · Week 9 — late penalty from 17:01 (syllabus late policy)
**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4 hours — kept short because Project 1 is due the same day

**Submit:** `ps8.py` (runnable end to end) and `ps8.md` (written answers, tables, recurrences).

## What this problem set uses

Weeks 0–8: interval DP, matrix chain and optimal BSTs (L25), LIS both ways with `bisect`, coin change,
tree DP and bitmask DP (L26). Brute-force references use Week 7's methods and CS 101 recursion.

**Not needed and not expected:** greedy proofs (Week 9 — D4 asks only what testing can and cannot
show). Floyd–Warshall is Lab 8's job, not this set's.

> **PROJECT 1 is due the same day.** If something has to slip, let it be this set rather than the
> project — the project is worth 10% of the course and this problem set about 3%.

---

## Part A — Matrix Chain (20 points)

**A1.** *(7)* `mcm(p)` returning the minimum scalar-multiplication count and the split table.

Verify against an exhaustive recursion on at least 200 random chains with $n \le 8$. Report
mismatches.

**A2.** *(4)* `parens(s, i, j)` reconstructing the parenthesisation as a string.

Report both for $p = [30, 35, 15, 5, 10, 20, 25]$.

**A3.** *(5)* Compute the cost of the **left-to-right** order $(((A_1A_2)A_3)\cdots)$ for the same
$p$, and give the ratio to the optimum.

Then construct a chain of 6 matrices where that ratio is **larger than 10**, and report it.

**A4.** *(4)* Tabulate, for $n \in \{4, 8, 12, 16, 20\}$, the number of parenthesisations (the Catalan
number $C_{n-1}$) against the number of DP subproblems.

State the two complexities being compared, and what the table shows.

---

## Part B — Optimal BSTs (16 points)

**B1.** *(7)* `optimal_bst(p)` returning the minimum expected comparisons, verified against exhaustive
enumeration of all BST shapes on at least 150 random distributions with $n \le 7$.

**B2.** *(4)* Compute the cost of the **perfectly balanced** BST for $p = [0.7, 0.1, 0.1, 0.1]$ and
compare with the optimum.

**B3.** *(5)* Answer both:

- **(a)** *(3)* Week 2 spent three lectures making trees balanced, and here balance is the wrong
  answer. **Reconcile these.** What does each algorithm know that the other does not?
- **(b)** *(2)* The recurrence adds $\sum_{t=i}^{j} p_t$ to every choice of root. Explain what that
  term accounts for, and what happens to your answers if you omit it.

---

## Part C — Longest Increasing Subsequence (19 points)

**C1.** *(5)* The $\Theta(n^2)$ version. State why the answer is $\max_i L[i]$ and not $L[n-1]$.

**C2.** *(7)* The $O(n\log n)$ version using `bisect`. Verify against C1 on at least 1,000 random
arrays.

**C3.** *(7)* **The trap.** The `tails` array has the right length but is generally **not** an
increasing subsequence of the input.

- **(a)** *(2)* Find the **smallest** array demonstrating this, by exhaustive search over short
  arrays. Report it, its `tails`, and an actual LIS.
- **(b)** *(2)* Over 1,000 random arrays, report what fraction of the time `tails` fails to be a
  subsequence. Then say what you would have to store to recover a real LIS.

---

## Part D — Coin Change (20 points)

**D1.** *(5)* `coin_dp(T, coins)` returning the fewest coins, or `None` if impossible.

**D2.** *(6)* `coin_greedy(T, coins)` taking the largest coin that fits.

For each of $[1,2,5,10,20,50,100,200]$ (UK), $[1,5,10,25]$ (US), $[1,5,6,9]$ and $[1,3,4]$, report how
many targets in $1 \dots 199$ greedy gets wrong, and the **smallest** failing target with both answers.

**D3.** *(5)* A coin system on which greedy is always optimal is called **canonical**.

Write a function that tests canonicality up to a bound, and use it to find **two** three-coin systems
containing 1: one canonical and one not.

**D4.** *(4)* In two sentences: what does D2 tell you about "I tested it and it worked"? Relate your
answer to Lecture 26 §3.

---

## Part E — Trees and Bitmasks (25 points)

**E1.** *(12)* **Maximum-weight independent set on a tree**, in $\Theta(V)$, using an explicit
(non-recursive) postorder.

Verify against $2^n$ brute force on at least 200 random trees with $n \le 12$. Then run it on a
**path graph of 100,000 vertices** and report that it completes — a recursive version will not.

**E2.** *(13)* **TSP by bitmask DP** in $O(2^n n^2)$, verified against $(n-1)!$ brute force on at least
150 instances with $n \le 8$.

Tabulate $(n-1)!$ against $2^n n^2$ for $n \in \{10, 15, 20, 25\}$, and state plainly whether this
makes TSP tractable.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 20 | Interval DP, reconstruction, and what DP buys |
| B | 16 | Optimal BSTs, and reconciling them with Week 2 |
| C | 19 | LIS both ways, and the `tails` trap |
| D | 20 | Coin change, and when greedy fails |
| E | 25 | Trees and bitmasks |
| **Total** | **100** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Counts are deterministic; timings are not.**

**A2** — $p = [30,35,15,5,10,20,25]$: optimum **15,125**, order `((A1(A2A3))((A4A5)A6))`.
**A3** — left-to-right costs **40,500**, a ratio of **2.68×**.

**A4:**

| $n$ | 4 | 8 | 12 | 16 | 20 |
| --- | --- | --- | --- | --- | --- |
| parenthesisations | 5 | 429 | 58,786 | 9,694,845 | **1,767,263,190** |
| subproblems | 8 | 32 | 72 | 128 | **200** |

**B2** — $p = [0.7,0.1,0.1,0.1]$: optimal **1.500**, balanced **2.000** (balanced is 1.333× worse).

**C3** — smallest failing array **`[2, 3, 1]`**, whose `tails` is `[1, 3]`. Over 3,000 random arrays,
`tails` is not a subsequence **47%** of the time.

**D2:**

| system | greedy failures, $T = 1\dots199$ | smallest failure |
| --- | --- | --- |
| UK $[1,2,5,10,20,50,100,200]$ | **0** | — |
| US $[1,5,10,25]$ | **0** | — |
| $[1,5,6,9]$ | **84** | $T=11$: greedy 3, optimal 2 |
| $[1,3,4]$ | **49** | $T=6$: greedy 3, optimal 2 |

**E2:**

| $n$ | $(n-1)!$ | $2^n n^2$ |
| --- | --- | --- |
| 10 | 362,880 | 102,400 |
| 15 | 87,178,291,200 | 7,372,800 |
| 20 | $1.22\times10^{17}$ | 419,430,400 |
| 25 | $6.20\times10^{23}$ | 20,971,520,000 |

**All verification mismatch counts should be 0.**

---

## A Note on Part D4

Greedy coin change works on every real currency and is wrong for 84 of the first 199 targets on
$[1,5,6,9]$. A student who tested on UK coins would have concluded it always works. **The error is not
visible in the code, and a small test suite does not catch it.** What catches it is knowing what
greedy needs from the coin system — and Lab 8's loop-order experiment shows the same failure of
reasoning in Floyd–Warshall.

---

*CS 102 · Week 8 · Problem Set 8 · © CSE Department*
