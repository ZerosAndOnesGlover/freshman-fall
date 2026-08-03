# CS 102 · Problem Set 7
## Dynamic Programming I

**Released:** Friday, Week 7 · **Due:** Friday, Week 8, 23:59
**100 points · counts toward the Problem Sets component (35% of the final grade)**

**Submit:** `ps7.py` (runnable end to end) and `ps7.md` (written answers, tables, recurrences).
Written answers inside code comments will not be marked.

> **PROJECT 1 was also assigned this week** and is due Friday of Week 9. Parts B and C of this
> problem set are directly reusable in it. Do them properly and you have started the project.

---

## Part A — Fibonacci and the Cost of Recomputation (18 points)

**A1.** *(4)* Naive recursive `fib`, instrumented with a call counter. Tabulate calls for
$n = 0 \dots 25$ alongside $2F(n+1) - 1$.

State whether the identity holds exactly, and give the growth rate of the call count in terms of
$\varphi$.

**A2.** *(5)* Instrument differently: count **how many times each subproblem** `fib(k)` is evaluated
while computing `fib(20)`. Report the counts for $k = 18, 15, 10, 5, 2, 1$.

You should recognise those numbers. **State the identity** and verify it for all $2 \le n \le 20$ and
$1 \le k \le n$.

**A3.** *(4)* Implement memoised and tabulated versions. Time all three at $n \in \{20, 25, 30, 32\}$
and report the table.

Then: the memoised and tabulated versions are both $\Theta(n)$. **One is several times faster.** Which,
and why?

**A4.** *(5)* Answer both:

- **(a)** *(2)* What does `fib_memo(5000)` do, and what does `fib_tab(5000)` do? Explain the
  difference in one sentence.
- **(b)** *(3)* The memoised version uses `memo={}` as a default argument. Explain what Python
  actually does with that, why it works here, and why it is a bug in most other functions.

---

## Part B — LCS (22 points)

**B1.** *(6)* `lcs(a, b)` returning the length and the full table.

**B2.** *(5)* `recover(a, b, T)` returning an actual longest common subsequence.

Verify on at least 300 random pairs over a small alphabet that the recovered string has the right
length **and is genuinely a subsequence of both**. Report failures.

**B3.** *(5)* `lcs_len_only(a, b)` using two rows, in $\Theta(\min(n,m))$ space.

Verify it agrees with B1 on the same 300 pairs. Then state, in one sentence, **what you gave up**.

**B4.** *(6)* Print the table for $a = $ `AGGTAB`, $b = $ `GXTXAYB` with row and column labels, and
answer:

- **(a)** *(2)* Reading left to right or top to bottom, the values never decrease. Why?
- **(b)** *(2)* The value increases only on diagonal steps. What does a diagonal step correspond to?
- **(c)** *(2)* Give a pair of strings with **more than one** distinct LCS of maximum length, and say
  which one your traceback returns and why.

---

## Part C — Edit Distance (20 points)

**C1.** *(6)* `edit(a, b)` — Levenshtein distance with insert, delete, and substitute.

Verify against an independent recursive implementation on at least 300 random pairs. Report
mismatches.

**C2.** *(4)* Report the distance for `kitten`→`sitting`, `sunday`→`saturday`, and
`intention`→`execution`.

**C3.** *(6)* Implement `edit_indel(a, b)` — insertions and deletions only, no substitution.

Verify the identity
$$\texttt{edit\_indel}(a,b) = |a| + |b| - 2\cdot\mathrm{LCS}(a,b)$$
on at least 300 random pairs, and **prove it** in three sentences.

**C4.** *(4)* Give three string pairs where the full edit distance is **strictly less** than
$|a|+|b|-2\,\mathrm{LCS}(a,b)$, with both numbers.

Explain what substitution buys, and name one real tool whose behaviour depends on this choice.

---

## Part D — Knapsack (24 points)

**D1.** *(6)* `knapsack(W, items)` with the $\Theta(nW)$ table, verified against brute-force
enumeration of all $2^n$ subsets on at least 200 instances with $n \le 12$. Report mismatches.

**D2.** *(4)* `which_items(...)` recovering the chosen items from the table. Verify their total weight
is within capacity and their total value equals the reported optimum.

**D3.** *(6)* The rolled 1-D version.

- **(a)** *(3)* Implement it with a **descending** inner loop and verify it matches D1.
- **(b)** *(3)* Change the inner loop to **ascending** and report how many of 300 random instances now
  differ. **The ascending version is not broken.** Say precisely what problem it solves instead.

**D4.** *(8)* **Pseudo-polynomiality.** Fix $n = 30$ and time your D1 for
$W \in \{100,\ 1000,\ 10000,\ 100000\}$. Tabulate $W$, the number of bits needed to write $W$, the
table size, and the time.

Then answer:

- **(a)** *(3)* $\Theta(nW)$ looks polynomial. **Why is it not polynomial in the input size?**
- **(b)** *(3)* By what factor does the running time grow when you add **one bit** to $W$? Confirm
  from your table.
- **(c)** *(2)* 0/1 knapsack is NP-complete. Explain why your algorithm does not contradict that.

---

## Part E — Choosing the State (16 points)

For each problem: state the subproblem, the recurrence with base cases, the number of states, and the
running time. **No code required** — this part is about design.

**E1.** *(4)* **Coin change.** Given coin denominations $c_1 \dots c_k$ (unlimited supply) and a target
$T$, find the fewest coins summing to exactly $T$, or report that it is impossible.

**E2.** *(4)* **Longest increasing subsequence** of an array of $n$ numbers. Give the
$\Theta(n^2)$ formulation; you do not need the $\Theta(n\log n)$ one (Week 8).

**E3.** *(4)* **Maximum-sum contiguous subarray** (the array may contain negatives). Your state should
give a $\Theta(n)$ algorithm — if it gives $\Theta(n^2)$, you have chosen the wrong one.

**E4.** *(4)* A problem where the obvious state is **wrong**:

> You are climbing $n$ stairs, one or two at a time, but **you may not take two singles in a row**.
> Count the distinct ways to reach step $n$.

State why "the number of ways to reach step $i$" is not a sufficient state, give one that is, and
count the states.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 18 | Why recomputation is fatal, and the two fixes |
| B | 22 | LCS, recovery, space, and what the table looks like |
| C | 20 | Edit distance, and its precise relation to LCS |
| D | 24 | Knapsack, the loop-direction bug, pseudo-polynomiality |
| E | 16 | State design — the actual skill |
| **Total** | **100** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Counts are deterministic; timings are not.**

A1: calls$(n) = 2F(n+1)-1$ exactly for $n = 0\dots25$; 21,891 calls at $n=20$; the ratio
calls$/\varphi^n \to 1.447$.

A2, computing `fib(20)`:

| $k$ | 18 | 15 | 10 | 5 | 2 | 1 |
| --- | --- | --- | --- | --- | --- | --- |
| times evaluated | 2 | 8 | 89 | 987 | 4,181 | **6,765** |

A3:

| $n$ | naive | memoised | tabulated |
| --- | --- | --- | --- |
| 20 | 2.00 ms | 0.0045 ms | 0.00097 ms |
| 30 | 253.88 ms | 0.0068 ms | 0.00114 ms |
| 32 | 685.63 ms | 0.0072 ms | 0.00120 ms |

C2: `kitten`→`sitting` **3**; `sunday`→`saturday` **3**; `intention`→`execution` **5**.

C4:

| $a$ | $b$ | LCS | $\lvert a\rvert+\lvert b\rvert-2\mathrm{LCS}$ | edit distance |
| --- | --- | --- | --- | --- |
| `abc` | `abd` | 2 | 2 | **1** |
| `kitten` | `sitting` | 4 | 5 | **3** |
| `abcd` | `dcba` | 1 | 6 | **4** |

D3(b): the ascending loop differs from 0/1 knapsack on **258 of 300** random instances.

D4, $n = 30$:

| $W$ | bits | cells | time |
| --- | --- | --- | --- |
| 100 | 7 | 3,000 | 0.4 ms |
| 1,000 | 10 | 30,000 | 7.8 ms |
| 10,000 | 14 | 300,000 | 71.0 ms |
| 100,000 | 17 | 3,000,000 | 741.9 ms |

**All verification mismatch counts should be 0.**

---

## A Note on Parts D3 and E4

**D3(b) is the most instructive bug in the course so far.** One character — the direction of a `range`
— turns 0/1 knapsack into unbounded knapsack. Neither version errors, both return plausible numbers,
and no test that only checks "is the answer sensible" will separate them. The only defence is knowing
what the loop order *means*: descending reads the row above, ascending reads the row you are writing.

**E4 exists because state design is the part that does not come from reading.** The obvious state
fails, you will notice it failing, and fixing it is a small version of exactly what Week 8 asks you to
do repeatedly. If you find yourself unable to write a recurrence, the problem is almost always the
state and almost never the algebra.

---

*CS 102 · Week 7 · Problem Set 7 · © CSE Department*
