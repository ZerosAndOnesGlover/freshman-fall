# CS 102 · Problem Set 9
## Greedy Algorithms and Huffman Coding

**Released:** Friday 26 March 2027, 10:00 (after L30) · Week 9
**Due:** Friday 2 April 2027, 17:00 · Week 10 — late penalty from 17:01 (syllabus late policy)
**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4–5 hours

**Submit:** `ps9.py` (runnable end to end) and `ps9.md` (written answers, tables, **proofs**).

## What this problem set uses

Weeks 0–9: exchange arguments and activity selection (L28), total completion time, maximum lateness
and fractional knapsack (L29), Huffman coding and the entropy bound (L30), plus Week 7's knapsack DP
and Week 8's coin-change DP as references. `heapq` is Week 3.

**Not needed and not expected:** string algorithms (Week 10). Bit-packing the encoded output is Lab 9's
job, not this set's.

> **MIDTERM 2 is Monday 29 March 2027, 18:00–19:15** (Week 10) and covers Weeks 5–9. **The exchange arguments in Parts A and B are the
> single most examinable thing in this problem set** — four of those five weeks contain one.

---

## Part A — Breaking Greedy Rules (24 points)

Before proving anything, learn to disprove it.

**A1.** *(6)* Implement a brute-force **activity selection** (exhaustive over subsets, $n \le 10$) as
your reference, and these four greedy rules: earliest finish time, shortest duration, earliest start
time, fewest conflicts.

Run all four against the reference on at least 1,000 random instances. Report a table of four rows.

**A2.** *(6)* Two of the rules fail quickly. For **each**, give the smallest counterexample you can
find, with the intervals, what the rule selects, and the optimum.

**A3.** *(8)* One rule fails on **none** of your 1,000 instances and is still not optimal.

- **(a)** *(5)* Find a counterexample by randomised search over larger instances. Report the intervals,
  the rule's answer, the optimum, and **roughly how many trials it took**.
- **(b)** *(3)* Verify it is minimal in the sense that removing any single interval destroys it. Then
  say what this rule's survival of 1,000 tests tells you about testing greedy algorithms.

**A4.** *(4)* Prove the **earliest finish time** rule correct by an exchange argument.

Your proof must state what is exchanged, why the exchange is legal, and why the result is no worse.
Three or four sentences.

---

## Part B — Scheduling (20 points)

**B1.** *(5)* $n$ jobs on one machine, minimising **total completion time**. Implement the greedy rule
and verify against exhaustive permutation search on at least 500 instances with $n \le 7$.

**B2.** *(5)* **Prove it** by an adjacent exchange. State exactly how the objective changes when two
adjacent jobs are swapped.

**B3.** *(6)* Now minimise **maximum lateness**, with each job having a deadline. Test three rules —
earliest deadline, shortest duration, smallest slack — against exhaustive search on at least 500
instances. Report the three failure counts.

**B4.** *(4)* One rule was provably optimal in B1 and is wrong most of the time in B3.

Name it, give its failure rate, and explain in two sentences what changed. **Nothing about the jobs
changed.**

---

## Part C — Fractional and 0/1 Knapsack (16 points)

**C1.** *(4)* `fractional_knapsack(W, items)` by value-to-weight ratio.

**C2.** *(4)* Prove it optimal by an exchange argument. Identify the **one word** in the problem
statement your proof depends on.

**C3.** *(5)* Apply the same greedy rule to **0/1** knapsack and compare against your Week 7 DP on at
least 1,000 random instances. Report the fraction where greedy is suboptimal, and the worst
greedy/optimal ratio you observe.

**C4.** *(3)* Construct a 0/1 instance where greedy achieves an **arbitrarily small** fraction of the
optimum. Give the family, and the ratio as a function of your parameter.

---

## Part D — Huffman Coding (28 points)

**D1.** *(7)* `huffman(freq)` returning a code, using `heapq`.

Verify on at least 300 random frequency sets that the code is **prefix-free**, and that its total cost
matches an exhaustive optimum for $n \le 7$ symbols.

> Your heap entries need a tie-break field. Say in one sentence what goes wrong without it.

**D2.** *(6)* Reproduce the CLRS example $\{a{:}45, b{:}13, c{:}12, d{:}16, e{:}9, f{:}5\}$: report the
code length per symbol, the total bits, and the fixed-length cost.

**D3.** *(7)* **The entropy bound.** Compute $H = -\sum p_s\log_2 p_s$ and verify
$H \le \bar{\ell} < H+1$ on at least 1,000 random distributions. Report violations of each side.

Then tabulate entropy against Huffman's average for a **two-symbol** alphabet with
$P(a) \in \{0.5, 0.7, 0.9, 0.99\}$, and explain in two sentences why the overhead grows.

**D4.** *(8)* Prove Part 1 of the optimality argument:

> If $x$ and $y$ are the two least frequent symbols, some optimal tree has them as siblings at maximum
> depth.

Your proof must exhibit the exchange and show the cost change is $\le 0$. **State the product whose
sign settles it.**

---

## Part E — Recognising the Paradigm (12 points)

For each, say whether a greedy algorithm solves it optimally. If yes, give the rule **and one sentence
of the exchange argument**. If no, give a counterexample and name the right technique.

**E1.** *(2)* Make change for $T$ using the fewest coins, denominations $[1, 7, 10]$.
**E2.** *(2)* Select the maximum number of non-overlapping intervals.
**E3.** *(2)* Fill a knapsack of capacity $W$ with divisible goods.
**E4.** *(3)* Find a minimum spanning tree.
**E5.** *(3)* Find a shortest path in a graph with some negative edge weights.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 24 | Disproving rules, and one that survives testing |
| B | 20 | Two objectives, two rules, one adjacent-exchange proof each |
| C | 16 | Where divisibility is load-bearing |
| D | 28 | Huffman: implementation, entropy, and the optimality proof |
| E | 12 | Recognising which paradigm applies |
| **Total** | **100** | |

**Proofs are marked as proofs.** A correct rule with no argument scores about a third. This is
deliberate and it is what MIDTERM 2 will do.

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Counts are deterministic; timings are not.**

**A1** — 2,000 random instances:

| rule | suboptimal on |
| --- | --- |
| earliest finish time | **0** |
| shortest duration | 28 |
| earliest start time | 201 |
| fewest conflicts | **0** |

**A2** — smallest counterexamples:

```
shortest duration:  (0,5) (4,6) (5,10)    picks 1, optimal 2
earliest start:     (0,10) (1,2) (3,4)    picks 1, optimal 2
```

**A3** — a fewest-conflicts counterexample, found after ~43,000 randomised trials:

$$(0,4)\ (1,4)\ (2,6)\ (3,5)\ (4,7)\ (6,9)\ (8,10)\ (9,12)\ (9,13)\ (11,14)$$

Selects **3**; optimum **4**. No counterexample exists with 6 intervals or fewer.

**B3** — 2,000 instances:

| rule | suboptimal on |
| --- | --- |
| earliest deadline first | **0** |
| shortest duration first | **1,233** |
| smallest slack first | 508 |

**C3** — greedy-by-ratio on 0/1 knapsack: suboptimal on **11%** of 2,000 instances, worst observed
ratio **0.412**. Classic case $W=50$, items $(10,60),(20,100),(30,120)$: greedy **160**, optimum
**220**, fractional **240**.

**D2** — CLRS example: code lengths $a{:}1, b{:}3, c{:}3, d{:}3, e{:}4, f{:}4$; total **224 bits**
against **300** fixed-length.

**D3** — 2,000 distributions: **0** violations on each side. Two-symbol alphabet:

| $P(a)$ | 0.5 | 0.7 | 0.9 | 0.99 |
| --- | --- | --- | --- | --- |
| entropy | 1.0000 | 0.8813 | 0.4690 | **0.0808** |
| Huffman | 1.0000 | 1.0000 | 1.0000 | **1.0000** |

---

## A Note on Part A3

A3 is the point of this problem set, and it is worth reading before you start.

The "fewest conflicts" rule is genuinely appealing — it looks more sophisticated than the others, and
it is optimal on every small random instance you will generate. Breaking it takes **ten intervals** and
about **forty thousand** attempts.

If your standard of correctness is "I tested it and it worked", this rule passes and is wrong.

**That is why Parts A4, B2, C2 and D4 ask for proofs.** An exchange argument is three or four
sentences; it is not hard, and it is the only thing that distinguishes a greedy algorithm that works
from one that has not yet met its counterexample. You have now seen the same lesson in Week 5
(Dijkstra, wrong on 2.3%), Week 8 (coin change, wrong on 42%) and here — three different algorithms,
one failure of method.

---

*CS 102 · Week 9 · Problem Set 9 · © CSE Department*
