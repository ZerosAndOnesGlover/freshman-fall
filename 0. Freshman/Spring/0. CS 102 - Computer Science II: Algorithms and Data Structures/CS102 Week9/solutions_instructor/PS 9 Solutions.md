# CS 102 · Problem Set 9 — Solutions
## Greedy Algorithms and Huffman Coding

**INSTRUCTOR / TA COPY — not for distribution**

Every number was produced by running code. **Deterministic** figures should match; **machine-dependent**
ones will not.

> **Proofs are marked as proofs on this set.** A correct rule with no argument scores about a third.
> MIDTERM 2 does the same, so be consistent and say so in the feedback.

---

## Part A — Breaking Greedy Rules (24)

### A1 (6) — deterministic

| rule | suboptimal on 2,000 |
| --- | --- |
| earliest finish time | **0** |
| shortest duration | 28 |
| earliest start time | 201 |
| fewest conflicts | **0** |

*Accept ±10 on the two non-zero counts; the two zeros must be zero. A student reporting failures for
earliest-finish has a bug — most often an overlap test using `>` where `>=` is needed, which rejects
activities that start exactly when the previous one ends.*

### A2 (6) — deterministic

```
shortest duration:  (0,5) (4,6) (5,10)    picks 1, optimal 2
earliest start:     (0,10) (1,2) (3,4)    picks 1, optimal 2
```

Both are minimal at 3 intervals. *3 marks each. Accept any 3-interval counterexample.*

### A3 (8) — the assessed question

**(a) (5)** A fewest-conflicts counterexample:

$$(0,4)\ (1,4)\ (2,6)\ (3,5)\ (4,7)\ (6,9)\ (8,10)\ (9,12)\ (9,13)\ (11,14)$$

Selects **3**, optimum **4**. Found after roughly **43,000** randomised trials over instances of 6–11
intervals.

**(b) (3)** Removing any single interval destroys it. Exhaustive search finds **no** counterexample
with 6 intervals or fewer.

Expected conclusion: **the rule survived 2,000 random tests and is wrong.** Testing can refute a greedy
rule quickly and cheaply; it can never establish one. Only a proof does that, and for this rule none
exists.

*5 for a genuine counterexample with a trial count. Accept any valid one — there are many, but they
are not easy to find, so a student who reports one has done the work. 3 for the minimality check and
the conclusion. A student who reports "I couldn't find one, so it's probably optimal" gets 2 of 8 and
a comment: that is the exact error the question is about.*

### A4 (4)

Expected proof: let $a_1$ finish earliest and let $O$ be optimal with first activity $a_k \ne a_1$.
Since $f_{a_1} \le f_{a_k}$, everything in $O$ after $a_k$ starts at or after $f_{a_k} \ge f_{a_1}$, so
replacing $a_k$ with $a_1$ creates no overlap. $O' = O - a_k + a_1$ is feasible and the same size, so
it is optimal and begins with the greedy choice. Induct on the activities starting after $f_{a_1}$.

*4 requires: what is exchanged, why it is legal (the inequality), and why it is no worse (same size).
Missing the inequality is 2.*

---

## Part B — Scheduling (20)

### B1 (5), B2 (5) — deterministic: 0 failures

Shortest processing time first, verified on 2,000 instances.

**The proof**: if adjacent jobs $A, B$ have $d_A > d_B$, swapping changes no other job's completion
time — the pair occupies the same interval — and changes the sum by $d_B - d_A < 0$. So no optimal
schedule has a longer job immediately before a shorter one. $\square$

*The mark is for "changes no other job's completion time". Without that the swap's effect is not
localised and the argument does not close. 2 of 5 without it.*

### B3 (6) — deterministic

| rule | suboptimal on 2,000 |
| --- | --- |
| earliest deadline first | **0** |
| shortest duration first | **1,233** |
| smallest slack first | 508 |

### B4 (4)

Shortest duration first: optimal in B1, wrong on **62%** in B3.

Expected: **nothing about the jobs changed — the objective did.** Minimising a *sum* rewards getting
short jobs out of the way; minimising a *maximum* rewards respecting deadlines, and a short job with a
distant deadline should wait. The sorting key must follow the objective, and the only way to know which
key is to prove it.

*This is Part B's graded idea. "Because deadlines matter now" is 2 of 4; the mark is for identifying
that the objective changed while the input did not.*

---

## Part C — Knapsack (16)

### C1 (4), C2 (4)

Proof: if an optimal solution takes some of item $j$ while item $i$ with a strictly greater ratio is
not fully taken, move $\varepsilon$ of weight from $j$ to $i$. Weight unchanged; value changes by
$\varepsilon(v_i/w_i - v_j/w_j) > 0$. Contradiction. $\square$

**The word is "fractional"** — or equivalently "divisible". The exchange needs to move an arbitrarily
small amount of weight, and with indivisible items you cannot.

*2 of 4 for the argument without identifying the word. The question asks for it explicitly.*

### C3 (5) — deterministic

Greedy-by-ratio on 0/1: suboptimal on **11%** of 2,000 instances; worst observed ratio **0.412**.

Classic case $W = 50$, items $(10,60), (20,100), (30,120)$: greedy **160**, optimum **220**, fractional
**240**.

### C4 (3)

Family: $W = N$, items $(1, 2)$ and $(N, N)$.

Greedy takes the ratio-2 item and then cannot fit the other, achieving **2**. The optimum is **$N$**.
Ratio $2/N \to 0$.

*Accept any family with an unbounded gap. The point is that greedy on 0/1 knapsack has **no**
approximation guarantee — not a bad constant, none at all.*

---

## Part D — Huffman (28)

### D1 (6) — deterministic: 0 failures

300+ random frequency sets: prefix-free and matching the exhaustive optimum.

**The tie-break**: heap entries must carry a unique second field. Without it, Python falls through to
comparing the third element, which for merged internal nodes may be a non-orderable object — raising
`TypeError` on *some* inputs and not others, depending on whether a tie ever occurs.

*A student whose code works on their tests may still have this bug. Ask whether they have a tie-break
field; do not deduct if they do not hit it, but note it.*

### D2 (5)

Round trip on 200+ texts including the three edge cases.

**The bugs to look for:**
- forgetting the **padding length**, which corrupts exactly the final symbol;
- the **single-symbol** case, where the tree has one node and the natural code is the empty string —
  which encodes to zero bits and cannot be decoded. Must be assigned `'0'`;
- the **empty string**, which should round-trip to itself.

### D3 (5) — deterministic

Code lengths $a{:}1,\ b{:}3,\ c{:}3,\ d{:}3,\ e{:}4,\ f{:}4$. Total **224 bits** against **300**
fixed-length — a 25% saving, essentially all of it from `a`.

*Code lengths are determined; the actual bit strings are not. Do not mark against specific codewords.*

### D4 (6) — deterministic

1,000+ distributions: **0** violations on each side of $H \le \bar\ell < H+1$.

| $P(a)$ | 0.5 | 0.7 | 0.9 | 0.99 |
| --- | --- | --- | --- | --- |
| entropy | 1.0000 | 0.8813 | 0.4690 | **0.0808** |
| Huffman | 1.0000 | 1.0000 | 1.0000 | **1.0000** |
| overhead | 0 | 0.1187 | 0.5310 | **0.9192** |

Expected explanation: with two symbols Huffman must assign one bit to each — there is nothing shorter
than a single bit. As the distribution skews, the entropy falls towards 0 while the code length stays
at 1, so the overhead approaches the full bit. At $P(a) = 0.99$ Huffman spends **12× the entropy**.

*2 of 6 for the table alone. The explanation must say that the integer-bits constraint is what binds.*

### D5 (6)

Let $T$ be optimal and $a, b$ two siblings at maximum depth. Suppose $x \ne a$, where $x$ is a least
frequent symbol. Then $f_x \le f_a$ and $\mathrm{depth}(a) \ge \mathrm{depth}(x)$. Swapping them
changes the cost by

$$\boxed{(f_x - f_a)\big(\mathrm{depth}(a) - \mathrm{depth}(x)\big) \;\le\; 0}$$

a product of a non-positive and a non-negative factor. So the swapped tree is no worse; $T$ was
optimal, so it remains optimal. Repeat for $y$ and $b$. $\square$

*The boxed product is the mark. 6 for the product with both signs justified; 3 for a hand-waving
"swapping a rare symbol deeper cannot hurt"; 0 for asserting the lemma.*

---

## Part E — Recognising the Paradigm (12)

| | answer |
| --- | --- |
| **E1** $[1,7,10]$ | **No.** Not canonical — greedy fails for **57** of $T = 1\dots199$, first at $T = 14$ (greedy $10{+}1{+}1{+}1{+}1 = 5$; optimum $7{+}7 = 2$). Use DP. |
| **E2** activity selection | **Yes** — earliest finish time. Exchange: swapping in the earliest-finishing activity cannot create an overlap. |
| **E3** fractional knapsack | **Yes** — value/weight ratio. Exchange: move $\varepsilon$ of weight to the better ratio. |
| **E4** MST | **Yes** — Prim or Kruskal. Exchange: the cut property (Week 6). |
| **E5** shortest path with negative edges | **No.** Dijkstra fails on 2.3% of such instances (Week 5). Use Bellman–Ford. |
| **E6** fewest late jobs | **Yes**, but **not** by the obvious rule. Plain EDF is suboptimal on **50%** of instances; **Moore–Hodgson** — process by deadline, and whenever the schedule goes late, drop the longest job scheduled so far — is optimal on 2,000 of 2,000. |

*E1 and E6 are the discriminators. E1 catches students who assume any coin system with a 1 is
canonical. **E6 catches the assumption that "greedy works" means "the first rule you thought of
works"** — the answer is yes *and* the naive rule fails half the time. Full marks on E6 require the
repair step.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 24 |
| B | 20 |
| C | 16 |
| D | 28 |
| E | 12 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. Mark the proofs as proofs.** A4, B2, C2 and D5 are 19 marks between them and they are the reason
this problem set exists. Students have spent nine weeks being rewarded for working code; this is the
set where an unjustified correct answer scores a third. **Say so in the feedback**, because MIDTERM 2
applies the same standard a week later.

**2. A3 is the one to read first.** A student who found a counterexample has genuinely engaged; one
who concluded the rule is optimal because testing did not refute it has demonstrated exactly the
failure the whole week is about. Both deserve a written comment, and they are different comments.

**3. Three failures, one lesson.** Dijkstra on negative weights (Week 5, 2.3%), coin change on
$[1,5,6,9]$ (Week 8, 42%), fewest-conflicts (here, needed 43,000 trials). If a student has seen all
three and still writes "I tested it thoroughly" as a justification, that is worth a conversation
rather than a deduction.

**4. Project 1 was due the same week this was released.** Submissions may be thin at the front end.
Check timestamps before assuming a student ran out of ability rather than time.

**5. Forward.** MIDTERM 2 (Week 10) covers Weeks 5–9 and will ask for an exchange argument. **Week 12**
returns to greedy in the approximation setting — where the greedy-choice property fails and you settle
for a provable ratio instead, which is the natural sequel to Part C4's unbounded gap.

---

*CS 102 · Week 9 · PS 9 Solutions · © CSE Department*
