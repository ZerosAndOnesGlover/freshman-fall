# CS 102 · Problem Set 7 — Solutions
## Dynamic Programming I

**INSTRUCTOR / TA COPY — not for distribution**

Every number was produced by running code. **Deterministic** figures should match a correct
submission; **machine-dependent** ones will not.

---

## Part A — Fibonacci (18)

### A1 (4) — deterministic

$\text{calls}(n) = 2F(n+1) - 1$, **exact for every $n = 0 \dots 25$**. At $n = 20$: 21,891 calls.

Growth: calls $\approx 1.447\,\varphi^{\,n}$. *(Verified: the ratio calls$/\varphi^n$ is 1.439, 1.447,
1.447, 1.447 at $n = 10, 20, 30, 40$.)* Accept $\Theta(\varphi^n)$; the constant is a bonus.

*The constant is $2\varphi/\sqrt5 = 1.447$, which a strong student may derive. Do not require it.*

### A2 (5) — deterministic

Computing `fib(20)`:

| $k$ | 18 | 15 | 10 | 5 | 2 | 1 |
| --- | --- | --- | --- | --- | --- | --- |
| evaluations | 2 | 8 | 89 | 987 | 4,181 | **6,765** |

**The identity**: `fib(k)` is evaluated $F(n-k+1)$ times, for $1 \le k \le n$. (And `fib(0)` is
evaluated $F(n-1)$ times.) *(Verified exact for all $2 \le n \le 23$.)*

Expected observation: those counts are themselves Fibonacci numbers — **the redundancy of naive
Fibonacci is Fibonacci**.

*3 for the counts, 2 for stating the identity. A student who notices the numbers are Fibonacci but does
not pin down the index gets 1 of those 2.*

### A3 (4) — machine-dependent

| $n$ | naive | memoised | tabulated |
| --- | --- | --- | --- |
| 20 | 2.00 ms | 0.0045 ms | 0.00097 ms |
| 25 | 23.59 ms | 0.0063 ms | 0.00101 ms |
| 30 | 253.88 ms | 0.0068 ms | 0.00114 ms |
| 32 | 685.63 ms | 0.0072 ms | 0.00120 ms |

Expected: **tabulation is ~6× faster** despite identical complexity. The reasons: no function-call
overhead per subproblem, no dictionary hashing, and array indexing instead. Both are $\Theta(n)$; the
constants differ.

*2 for the table, 2 for naming at least two of (call overhead, dict hashing, allocation).*

### A4 (5)

**(a) (2)** `fib_memo(5000)` raises **`RecursionError`**; `fib_tab(5000)` returns a 1,045-digit
integer. Memoisation recurses to the depth of the subproblem chain; tabulation iterates.

**(b) (3)** The default `{}` is evaluated **once, at function-definition time**, and the same object is
reused by every call. Here that is deliberate — the cache persists across top-level calls. It is a bug
in general because callers expect a fresh default, and a mutable one silently accumulates state
between unrelated calls.

*Full marks require "evaluated once at definition time". "It's a global" is 1 of 3.*

---

## Part B — LCS (22)

### B1 (6), B2 (5) — deterministic: 0 failures

Reference: 300 random pairs — recovered length correct **and** the result verified to be a subsequence
of both inputs. **0 failures.**

*The check that matters is the subsequence test. A student who only compares lengths has not verified
recovery, which is where the bugs are. Cap B2 at 3 without it.*

### B3 (5)

Expected: **you give up the traceback.** Two rows give the length and cannot recover the subsequence,
because the walk back needs the whole table. Mention Hirschberg (Project 1) as the resolution.

### B4 (6)

The table:

```
       -  G  X  T  X  A  Y  B
    -  0  0  0  0  0  0  0  0
    A  0  0  0  0  0  1  1  1
    G  0  1  1  1  1  1  1  1
    G  0  1  1  1  1  1  1  1
    T  0  1  1  2  2  2  2  2
    A  0  1  1  2  2  3  3  3
    B  0  1  1  2  2  3  3  4
```

**(a) (2)** Extending a prefix can only add options, never remove them — $L[i][j] \ge L[i-1][j]$ and
$L[i][j] \ge L[i][j-1]$ directly from the recurrence.

**(b) (2)** A diagonal step is a **matched character**, the only case that adds 1.

**(c) (2)** Any pair with two maximal LCSs; e.g. $a = $ `AB`, $b = $ `BA` has LCSs `A` and `B`, both of
length 1. The `>=` tie-break prefers moving **up** (dropping a character of $a$) when the two
candidates are equal.

*Accept any valid example. The point is that the **length** is unique and the **subsequence** is not.*

---

## Part C — Edit Distance (20)

### C1 (6) — deterministic: 0 mismatches

Reference: 400 random pairs against an independent recursion. **0 mismatches.**

**The bug to look for**: initialising the borders to 0 instead of $D[i][0] = i$, $D[0][j] = j$. It
gives a wrong answer on every pair where one string is a prefix of the other, and it is the most
common error on this problem.

### C2 (4) — deterministic

`kitten`→`sitting` **3**; `sunday`→`saturday` **3**; `intention`→`execution` **5**.

### C3 (6) — deterministic: 0 failures

Verified over 400 pairs.

**The proof** (three sentences): any indel-only edit sequence deletes some characters of $a$ and
inserts some of $b$, and the characters left untouched form a common subsequence. Conversely, given a
common subsequence of length $L$, delete the other $|a| - L$ characters of $a$ and insert the other
$|b| - L$ of $b$, giving $|a| + |b| - 2L$ operations. So the minimum is achieved exactly when $L$ is
maximised.

### C4 (4) — deterministic

| $a$ | $b$ | LCS | indel | edit |
| --- | --- | --- | --- | --- |
| `abc` | `abd` | 2 | 2 | **1** |
| `kitten` | `sitting` | 4 | 5 | **3** |
| `abcd` | `dcba` | 1 | 6 | **4** |

Expected: substitution replaces a delete **and** an insert with a single operation, so it can halve the
cost of a changed character. Real tool: **`diff`**, which reports changed lines rather than a delete
plus an insert — or a spell-checker, where a typo is one substitution rather than two edits.

---

## Part D — Knapsack (24)

### D1 (6), D2 (4) — deterministic: 0 mismatches

Reference: 300 instances against brute-force enumeration. **0 mismatches.**

### D3 (6)

**(a) (3)** Descending matches the 2-D table on **300 of 300**.

**(b) (3)** The ascending version differs on **258 of 300** instances, and **it is not broken** — it
correctly solves the **unbounded knapsack**, where each item may be taken any number of times.
Ascending reads `dp[w - wi]` *after* it has already been updated in this row, so the same item is
available again.

*Full marks require naming unbounded knapsack. "It's wrong / it double-counts" is 1 of 3 — the question
asks what problem it solves, and "a different one" is not an answer.*

### D4 (8) — machine-dependent times, deterministic sizes

| $W$ | bits | cells | time |
| --- | --- | --- | --- |
| 100 | 7 | 3,000 | 0.4 ms |
| 1,000 | 10 | 30,000 | 7.8 ms |
| 10,000 | 14 | 300,000 | 71.0 ms |
| 100,000 | 17 | 3,000,000 | 741.9 ms |

**(a) (3)** The input size is the number of *characters* needed to write the instance, and $W$
contributes $\log_2 W$ bits. So $\Theta(nW) = \Theta(n\,2^{\text{bits}})$ — exponential in the input
size. It is polynomial in the *value* $W$, not in its *encoding*.

**(b) (3)** Adding one bit **doubles** $W$, hence doubles the table and the time. Confirmed by the
table: going from $W = 1{,}000$ to $W = 10{,}000$ adds $\log_2 10 \approx 3.3$ bits, so the predicted
factor is $2^{3.3} \approx 10$; the measured time goes 7.8 → 71.0 ms, a factor of **9.1**.

**(c) (2)** NP-completeness says no algorithm is polynomial in the *input size* unless P = NP. This
algorithm is polynomial in $n$ and $W$ but exponential in the encoding of $W$, so it is consistent. It
is useful precisely when $W$ is small.

*This is the graded idea of Part D. A student who says "the algorithm is polynomial so knapsack must
be in P" has the misconception the question is for — mark it, and write a sentence.*

---

## Part E — Choosing the State (16)

### E1 (4) — coin change

**State** $C[t]$ = fewest coins summing to exactly $t$.
**Recurrence** $C[t] = 1 + \min_{c_i \le t} C[t - c_i]$, with $C[0] = 0$ and $C[t] = \infty$ if no
option applies.
**States** $T+1$; **time** $\Theta(kT)$.

*Worth mentioning in feedback: with coins $\{1, 5, 6, 9\}$ and $T = 11$, greedy gives $9+1+1 = 3$ and
the optimum is $5+6 = 2$. This is Week 9's opening example.*

### E2 (4) — LIS

**State** $L[i]$ = length of the longest increasing subsequence **ending at** $i$.
**Recurrence** $L[i] = 1 + \max\{L[j] : j < i,\ a[j] < a[i]\}$, or 1 if none.
Answer is $\max_i L[i]$ — **not** $L[n-1]$. **States** $n$; **time** $\Theta(n^2)$.

*The "ending at $i$" is the whole trick. A student whose state is "the LIS of the first $i$ elements"
cannot write the recurrence, because that state does not say what the last element was. This is the
same failure as E4 and worth linking in feedback.*

*Sanity value: LIS of `[10,9,2,5,3,7,101,18]` is **4**.*

### E3 (4) — maximum subarray

**State** $M[i]$ = maximum sum of a subarray **ending at** $i$.
**Recurrence** $M[i] = \max(a[i],\ M[i-1] + a[i])$. Answer $\max_i M[i]$.
**States** $n$; **time** $\Theta(n)$.

*Again "ending at". A state of "the best subarray within the first $i$" gives $\Theta(n^2)$ because it
does not compose. Sanity value: `[-2,1,-3,4,-1,2,1,-5,4]` → **6**.*

### E4 (4) — the staircase with no two consecutive singles

**Why the obvious state fails**: "ways to reach step $i$" does not record whether the last move was a
single, and the legality of the next move depends on exactly that. The naive state gives Fibonacci,
which **overcounts** — at $n = 13$ it says 377 when the answer is 28.

**A state that works**: $W[i][\ell]$ = ways to reach step $i$ with last move of size $\ell \in \{1,2\}$.

$$W[i][1] = W[i-1][2], \qquad W[i][2] = W[i-2][1] + W[i-2][2]$$

**States** $2n$; **time** $\Theta(n)$.

The correct sequence for $n = 0 \dots 13$:

$$1,\ 1,\ 1,\ 2,\ 2,\ 3,\ 4,\ 5,\ 7,\ 9,\ 12,\ 16,\ 21,\ 28$$

*(Verified against brute-force enumeration of all legal move sequences, and it satisfies
$a(n) = a(n-2) + a(n-3)$.)*

*2 for identifying why the 1-D state fails, 2 for a working state with a count. Accept any equivalent
state, e.g. tracking "is the previous move a single" as a boolean.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 18 |
| B | 22 |
| C | 20 |
| D | 24 |
| E | 16 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. Part E is where the marks separate**, and it is worth reading before the others. A–D are
mechanical for a student who read the lectures; E asks them to design, and E2, E3 and E4 all fail in
the *same* way — a state that does not record enough about the last decision. If a student got E4 and
missed E2, they have not seen the pattern; say so.

**2. D3(b) will produce "it's a bug" answers.** It is not a bug, it is a different problem, and the
distinction is the point. Do not accept "it double-counts".

**3. D4(c) is the NP-completeness misconception**, three weeks early. Students who answer it well are
ready for Week 12; students who do not should be flagged now rather than in Week 12.

**4. Project 1 was assigned this week.** Parts B and C here are directly reusable, and it is worth
saying so on the scripts — a student who wrote a clean `lcs` and `recover` for B1–B2 has done Project
1 Part 1.1 already.

**5. Carried forward.** Weeks 2, 3, 4 and 6 each contained a measurement that contradicted a
complexity comparison. **A3 is the same thing in miniature** — memoisation and tabulation are both
$\Theta(n)$ and one is 6× faster — and Lecture 22 §5 gives the large version at 1,242×. Students who
have internalised this by now should find A3 obvious; those who are still surprised will struggle in
Week 8.

---

*CS 102 · Week 7 · PS 7 Solutions · © CSE Department*
