# CS 102 · Problem Set 8 — Solutions
## Dynamic Programming II

**INSTRUCTOR / TA COPY — not for distribution**

Every number was produced by running code. **Deterministic** figures should match; **machine-dependent**
ones will not.

> **This set is due the same day as Project 1.** See the grading note at the end before applying late
> penalties.

---

## Part A — Matrix Chain (20)

### A1 (7) — deterministic: 0 mismatches

Reference: 300 random chains against exhaustive recursion. **0 mismatches.**

**The bug to look for** is looping `for i: for j:` instead of by increasing length. It reads cells that
are still 0, so it returns an answer that is **too small** and never errors. If a submission's optimum
is *below* the brute-force value, this is why.

### A2 (4) — deterministic

$p = [30,35,15,5,10,20,25]$: **15,125**, order `((A1(A2A3))((A4A5)A6))`.

### A3 (5) — deterministic for the given $p$

Left-to-right costs **40,500**, ratio **2.68×**.

For a ratio above 10, any chain alternating large and small dimensions works. Reference examples:

| $p$ | optimal | left-to-right | ratio |
| --- | --- | --- | --- |
| $[500,1,1,500,1,500,1]$ | 1,502 | 1,000,500 | **666×** |
| $[100,1,100,1,100,1,100]$ | 10,301 | 50,000 | 4.9× |

*Accept any chain with ratio > 10. A search over random dimension vectors finds them easily; the
insight is that the naive order keeps the first matrix's row count as a factor in every product.*

### A4 (4) — deterministic

| $n$ | 4 | 8 | 12 | 16 | 20 |
| --- | --- | --- | --- | --- | --- |
| parenthesisations $C_{n-1}$ | 5 | 429 | 58,786 | 9,694,845 | **1,767,263,190** |
| subproblems | 8 | 32 | 72 | 128 | **200** |

Expected: exhaustive search is $\Theta(4^n/n^{1.5})$ (Catalan); DP is $\Theta(n^3)$ over $\Theta(n^2)$
states. **1.8 billion against 200 at $n=20$.**

---

## Part B — Optimal BSTs (16)

### B1 (7) — deterministic: 0 mismatches

Reference: 200 random distributions against exhaustive enumeration of BST shapes. **0 mismatches.**

### B2 (4) — deterministic

$p = [0.7,0.1,0.1,0.1]$: optimal **1.500**, balanced **2.000**, so balanced is **1.333× worse**.

### B3 (5)

**(a) (3)** Week 2 knows **nothing** about the query distribution and must guarantee a worst case, so
it minimises height. Here the distribution is **known**, and the objective is the *expected* cost, so
it pays to put a frequent key near the root even at the cost of a taller tree. **Different information,
different objective, and neither algorithm is wrong.**

*Full marks require naming both the information difference and the objective difference. One of the two
is 2 of 3.*

**(b) (2)** The term $\sum_{t=i}^{j} p_t$ accounts for **every key in the interval moving one level
deeper** when a root is placed above them. It does not depend on which root is chosen, which is why it
sits outside the `min`. Omitting it makes every cost too small and the recurrence degenerate — the
computed value stops being an expected depth at all.

---

## Part C — LIS (18)

### C1 (4)

Answer is $\max_i L[i]$ because the LIS need not end at the last element. *A student returning
$L[n-1]$ will be wrong on almost every array; if their C2 check passes anyway, their fast version has
the same bug.*

### C2 (5) — deterministic: 0 mismatches

2,000 random arrays.

### C3 (5) — machine-dependent

| $n$ | $\Theta(n^2)$ | $O(n\log n)$ | speedup |
| --- | --- | --- | --- |
| 1,000 | 27.7 ms | 0.15 ms | 185× |
| 4,000 | 421.5 ms | 0.64 ms | 661× |
| 16,000 | 6,725.9 ms | 2.81 ms | **2,397×** |

### C4 (4) — deterministic

**(a) (2)** Smallest failing array: **`[2, 3, 1]`**, `tails` = `[1, 3]`, which is not a subsequence
(3 precedes 1 in the input). An actual LIS is `[2, 3]`.

A clearer illustration for the report: `[1, 3, 5, 2]` gives `tails` = `[1, 2, 5]`; an actual LIS is
`[1, 3, 5]`.

**(b) (2)** Over 3,000 random arrays, `tails` fails to be a subsequence **47%** of the time.

To recover a real LIS, store for each element the index of its predecessor — the length at which it was
placed, and which element occupied the previous length at that moment — then walk the chain back.

*Accept "predecessor pointers". This is the third time the pattern has appeared (rolled DP tables,
rolled knapsack rows, here); mention that in feedback.*

---

## Part D — Coin Change (14)

### D1 (4), D2 (4) — deterministic

| system | greedy failures, $T=1\dots199$ | smallest failure |
| --- | --- | --- |
| UK $[1,2,5,10,20,50,100,200]$ | **0** | — |
| US $[1,5,10,25]$ | **0** | — |
| $[1,5,6,9]$ | **84** | $T=11$: greedy 3 ($9{+}1{+}1$), optimal 2 ($5{+}6$) |
| $[1,3,4]$ | **49** | $T=6$: greedy 3 ($4{+}1{+}1$), optimal 2 ($3{+}3$) |

### D3 (3)

Reference: over all $[1,a,b]$ with $2 \le a < b \le 19$, **65 of 125** are canonical up to $T = 200$.

- **Canonical**: every $[1, 2, b]$ — e.g. $[1,2,5]$.
- **Not canonical**: $[1,3,4]$, $[1,4,5]$, $[1,5,6]$, $[1,5,7]$, …

*Accept any correct pair. The $[1,2,b]$ family being uniformly canonical is a nice observation and
worth a comment if a student notices it.*

### D4 (3)

Expected: greedy coin change is correct on **every real currency** and wrong on 84 of the first 199
targets for $[1,5,6,9]$. Testing on the examples you have does not establish correctness; **a proof
that the coin system is canonical does.** Week 9 requires exactly that kind of argument — an exchange
argument — for every greedy algorithm it introduces.

*This links D4 to Week 9 explicitly. A student who says only "testing isn't proof" gets 2 of 3; the
third mark is for connecting it to what a correctness argument would have to establish.*

---

## Part E — Trees, Bitmasks, All Pairs (32)

### E1 (8) — deterministic: 0 mismatches

200 random trees against $2^n$ brute force. **0 mismatches.**

Path graph of 100,000 vertices, all weights 1: MIS = **50,000**, in about **61 ms**. A recursive
implementation raises `RecursionError`.

*4 for correctness, 2 for the iterative postorder, 2 for the 100,000-vertex run. A student who used
recursion and raised the limit should be told why that is not a fix — Week 4 Lecture 15 §1.*

### E2 (8) — deterministic: 0 mismatches

150+ instances against $(n-1)!$ brute force.

| $n$ | $(n-1)!$ | $2^n n^2$ |
| --- | --- | --- |
| 10 | 362,880 | 102,400 |
| 15 | 87,178,291,200 | 7,372,800 |
| 20 | $1.22\times10^{17}$ | 419,430,400 |
| 25 | $6.20\times10^{23}$ | 20,971,520,000 |

Expected answer: **no, this does not make TSP tractable.** $O(2^n n^2)$ is still exponential; it moves
the practical limit from about $n=13$ to about $n=20$. TSP is NP-hard.

*The last sentence is the mark. A student who tabulates the ratio and concludes "so it's efficient"
has missed the question.*

### E3 (8) — deterministic: 0 mismatches

300 non-negative graphs and 300 with negative edges (no negative cycles), against Bellman–Ford from
every source.

### E4 (8) — deterministic, and the assessed question

| loop order | wrong on 200 |
| --- | --- |
| `k,i,j` | **0** |
| `k,j,i` | **0** |
| `i,k,j` | 78 |
| `i,j,k` | 70 |
| `j,i,k` | 70 |
| `j,k,i` | 73 |

Expected explanation: $d^{(k)}[i][j]$ means "shortest $i \rightsquigarrow j$ using only
$\{0,\dots,k-1\}$ as intermediates". The recurrence for level $k+1$ reads **level-$k$ values for all
$i,j$**, so the entire level must be complete before the next begins. Only `k` outermost guarantees
that; the inner two loops may be in either order because within a level the updates do not interfere
(row $k$ and column $k$ are unchanged during round $k$).

*4 for the table, 4 for an explanation in terms of the state's meaning. An explanation in terms of
"the array isn't updated yet" without saying what the array is supposed to contain is 2 of 4.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 20 |
| B | 16 |
| C | 18 |
| D | 14 |
| E | 32 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. This set collides with Project 1.** The handout told students to prioritise the project and to
let Part E slip if anything had to. **Apply that consistently**: a strong project with a thin Part E is
the outcome the instructions asked for, and should not be penalised twice. Check submission timestamps
before assuming a student mismanaged the week.

**2. D4 and E4 are the same lesson** and should be marked together. Both are cases where testing
cannot distinguish a correct implementation from an incorrect one, and where the only defence is
knowing what the state or the precondition *means*. Students who answer one well and the other badly
have not seen the connection; say so.

**3. Expect A1's silent-zero bug.** An incorrectly ordered interval loop gives an answer *below* the
true optimum. It is easy to spot when marking — compare against the reference value 15,125 — and it is
worth diagnosing rather than just deducting, because the student will hit it again in Week 11.

**4. Carried forward.** PS 7 Part E asked students to design states; every part of this set exercises
one. The failures cluster: a student who could not do PS 7 E2 (LIS "ending at $i$") will also struggle
with C1 here. **Week 9 does not need state design at all**, so this is the last opportunity to fix it
before the final.

**5. Forward.** D2's greedy failure is **Week 9 Lecture 28's opening example.** E2's TSP returns in
**Week 12** as the canonical NP-hard problem, with Week 6's MST supplying a 2-approximation.

---

*CS 102 · Week 8 · PS 8 Solutions · © CSE Department*
