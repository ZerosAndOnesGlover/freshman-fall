# CS 102 · Problem Set 8
## Dynamic Programming II — Applications

**Released:** Friday, Week 8 · **Due:** Friday, Week 9, 23:59
**100 points · counts toward the Problem Sets component (35% of the final grade)**

**Submit:** `ps8.py` (runnable end to end) and `ps8.md` (written answers, tables, recurrences).

> **PROJECT 1 is due the same day.** This is the heaviest week of the term. Parts A and B here are
> short; Part E is the longest. **Start now**, and if something has to slip, let it be Part E rather
> than the project — the project is worth 10% of the course and this problem set is worth about 3%.

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

## Part C — Longest Increasing Subsequence (18 points)

**C1.** *(4)* The $\Theta(n^2)$ version. State why the answer is $\max_i L[i]$ and not $L[n-1]$.

**C2.** *(5)* The $O(n\log n)$ version using `bisect`. Verify against C1 on at least 1,000 random
arrays.

**C3.** *(5)* Time both at $n \in \{1000, 4000, 16000\}$ and report the speedup.

**C4.** *(4)* **The trap.** The `tails` array has the right length but is generally **not** an
increasing subsequence of the input.

- **(a)** *(2)* Find the **smallest** array demonstrating this, by exhaustive search over short
  arrays. Report it, its `tails`, and an actual LIS.
- **(b)** *(2)* Over 1,000 random arrays, report what fraction of the time `tails` fails to be a
  subsequence. Then say what you would have to store to recover a real LIS.

---

## Part D — Coin Change (14 points)

**D1.** *(4)* `coin_dp(T, coins)` returning the fewest coins, or `None` if impossible.

**D2.** *(4)* `coin_greedy(T, coins)` taking the largest coin that fits.

For each of $[1,2,5,10,20,50,100,200]$ (UK), $[1,5,10,25]$ (US), $[1,5,6,9]$ and $[1,3,4]$, report how
many targets in $1 \dots 199$ greedy gets wrong, and the **smallest** failing target with both answers.

**D3.** *(3)* A coin system on which greedy is always optimal is called **canonical**.

Write a function that tests canonicality up to a bound, and use it to find **two** three-coin systems
containing 1: one canonical and one not.

**D4.** *(3)* In two sentences: what does D2 tell you about "I tested it and it worked"? Relate your
answer to what Week 9 will require.

---

## Part E — Trees, Bitmasks, and All Pairs (32 points)

**E1.** *(8)* **Maximum-weight independent set on a tree**, in $\Theta(V)$, using an explicit
(non-recursive) postorder.

Verify against $2^n$ brute force on at least 200 random trees with $n \le 12$. Then run it on a
**path graph of 100,000 vertices** and report that it completes — a recursive version will not.

**E2.** *(8)* **TSP by bitmask DP** in $O(2^n n^2)$, verified against $(n-1)!$ brute force on at least
150 instances with $n \le 8$.

Tabulate $(n-1)!$ against $2^n n^2$ for $n \in \{10, 15, 20, 25\}$, and state plainly whether this
makes TSP tractable.

**E3.** *(8)* **Floyd–Warshall**, verified against Bellman–Ford from every source on at least 200
graphs — including graphs with negative edges but no negative cycle.

**E4.** *(8)* **The loop order.** Implement a version parameterised by which of `i`, `j`, `k` is
outermost, and test all **six** orderings against a correct reference on at least 150 graphs.

Report a table of six rows. Then explain, in terms of what $d^{(k)}$ *means*, why exactly two of them
work.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 20 | Interval DP, reconstruction, and what DP buys |
| B | 16 | Optimal BSTs, and reconciling them with Week 2 |
| C | 18 | LIS both ways, and the `tails` trap |
| D | 14 | Coin change, and when greedy fails |
| E | 32 | Trees, bitmasks, Floyd–Warshall, and the loop order |
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

**C3:**

| $n$ | $\Theta(n^2)$ | $O(n\log n)$ | speedup |
| --- | --- | --- | --- |
| 1,000 | 27.7 ms | 0.15 ms | 185× |
| 4,000 | 421.5 ms | 0.64 ms | 661× |
| 16,000 | 6,725.9 ms | 2.81 ms | **2,397×** |

**C4** — smallest failing array **`[2, 3, 1]`**, whose `tails` is `[1, 3]`. Over 3,000 random arrays,
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

**E4:**

| loop order | wrong on |
| --- | --- |
| `k,i,j` | **0 of 200** |
| `k,j,i` | **0 of 200** |
| `i,k,j` | 78 of 200 |
| `i,j,k` | 70 of 200 |
| `j,i,k` | 70 of 200 |
| `j,k,i` | 73 of 200 |

**All verification mismatch counts should be 0.**

---

## A Note on Parts D4 and E4

Both are about the same failure of reasoning.

In **D4**, greedy coin change works on every real currency and is wrong for 84 of the first 199 targets
on $[1,5,6,9]$. A student who tested on UK coins would have concluded it always works.

In **E4**, four of the six loop orderings are wrong about a third of the time. A student who tested one
graph would very likely have concluded any order works.

**Neither error is visible in the code, and neither is caught by a small test suite.** What catches
them is knowing what the state *means* — that greedy needs the coin system to be canonical, and that
$d^{(k)}$ needs all of level $k$ before level $k+1$. **Week 9 is entirely about supplying that kind of
argument for greedy algorithms**, and this problem set is the last one before you need it.

---

*CS 102 · Week 8 · Problem Set 8 · © CSE Department*
