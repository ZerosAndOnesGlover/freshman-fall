# CS 102 · Lab 7 — Solutions and Checkoff Notes
## Visualising DP Tables

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

This is a **light-compute lab** — everything runs instantly. It is also the week Project 1 is
assigned, so students will arrive with the project on their minds.

**Use that.** Part A and Part B are Project 1 Part 1.1 with printing attached. Say so at the start:
a student who leaves the lab with a working `lcs` and traceback has done the first 10 marks of the
project, and the ones who realise this will start the project a week earlier than the ones who do not.

**Part D is the only part with a real finding.** Protect at least 30 minutes for it.

---

## Part A — Print the Tables (10)

### A1 (4), A2 (3) — deterministic

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

LCS length **4**, subsequence `GTAB`.

*Off-by-one in the labelling is the common error: row $i$ is labelled with `a[i-1]`, not `a[i]`. It
does not affect the numbers, so it survives unless you look.*

### A3 (3) — deterministic

`kitten` → `sitting`, distance **3**. Borders: top row $0,1,2,\dots,7$; left column $0,1,\dots,6$.

Expected: the top row is "turn the empty string into the first $j$ characters of $b$" — $j$
insertions. The left column is $i$ deletions. **With zero borders you get a confidently wrong answer**
— every pair where one string is a prefix of the other returns 0.

---

## Part B — The Traceback (10)

### B1 (5), B2 (3) — deterministic

| cell | move | character |
| --- | --- | --- |
| (6,7) | match | `B` |
| (5,6) | left | |
| (5,5) | match | `A` |
| (4,4) | left | |
| (4,3) | match | `T` |
| (3,2) | up | |
| (2,2) | left | |
| (2,1) | match | `G` |

Read in reverse: `G`, `T`, `A`, `B`.

### B3 (2)

- A **diagonal** step means the two characters matched and were taken into the subsequence; it is the
  only case in the recurrence that adds 1.
- Changing `>=` to `>` may return a **different** subsequence of the **same** length. The length is
  determined by the table and cannot change; only the choice among equal-length answers does.

*The second half is what to mark. A student who says the length might change has not understood that
the traceback only reads a table it did not alter.*

---

## Part C — Watch It Fill (10)

### C1 (4)

Six snapshots. No marking subtleties; check they print after each row and not after each cell.

### C2 (3) — deterministic

Anti-diagonal sizes for the $6\times7$ interior: $1, 2, 3, 4, 5, 6, 6, 5, 4, 3, 2, 1$. Largest **6**.

### C3 (3)

- Row-by-row needs **2 rows** = $\Theta(n)$ for a square table. Anti-diagonal needs the two previous
  diagonals, and the longest diagonal of an $n \times n$ table has $n$ cells — so **also $\Theta(n)$**,
  with a worse constant and much worse locality.
- Reasons to do it anyway: **parallelism** — every cell on a diagonal is independent, so a wavefront
  is the standard way to put this DP on a GPU or a vector unit. Accept also "it is the natural order
  for a systolic/hardware implementation".

*Most students will guess anti-diagonal saves space. It does not. Mark the comparison, not the guess.*

---

## Part D — Memoisation Against Tabulation (10)

### D1 (4), D2 (3) — deterministic

| $n$ | $W$ | weights | top-down | bottom-up | ratio |
| --- | --- | --- | --- | --- | --- |
| 20 | 1,000 | $[1,100]$ | 5,839 | 20,020 | 3.4× |
| 20 | 10,000 | $[1,100]$ | 5,839 | 200,020 | 34.3× |
| 10 | 100,000 | $[1,100]$ | **636** | 1,000,010 | **1,572×** |
| 20 | 10,000 | multiples of 1,000 | **161** | 200,020 | **1,242×** |

Note row 2 against row 1: the top-down count is **identical** (5,839) while $W$ grew tenfold. The
reachable state space did not change, only the table that tabulation insists on allocating.

*That observation is worth a mark in feedback even though the question does not ask for it.*

### D3 (3) — deterministic and the assessed question

| $\lvert a\rvert = \lvert b\rvert$ | top-down | bottom-up | ratio |
| --- | --- | --- | --- |
| 200 | 28,739 | 40,000 | **1.39×** |

Expected answer: **the fraction of the state space that is reachable.**

For knapsack the reachable capacities are only those expressible as sums of item weights; with weights
that are multiples of 1,000 and $W = 10{,}000$ there are about eleven per item, so tabulation
allocates 200,020 cells to use 161. For LCS essentially every $(i,j)$ pair is reached, so there is
nothing to skip — and tabulation's cells are cheaper, so it wins on the clock.

*3 for naming reachability. 1 for "it depends on the problem" without saying which property. 0 for
"memoisation is better", which the LCS row refutes.*

---

## Checkoff Checklist

1. The A2 table matches exactly, including the border row and column.
2. The edit-distance borders are $i$ and $j$, not zeros.
3. B3 says the **length** cannot change under a different tie-break.
4. C3 does **not** claim anti-diagonal saves space.
5. D3 names reachability, not a preference.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 10 |
| B | 10 |
| C | 10 |
| D | 10 |
| **Total** | **40** |

Labs are pass/fail for progression: **10 of 13 required.**

---

## Note for the Week 8 Lecture

Week 8 is five new DP problems in one week, and the students who cope are the ones who stopped
thinking of DP as "fill a table" and started thinking of it as "choose a state".

**Part D is the lever for that.** It shows the table is an implementation detail — one that can cost
1,242× more work than necessary — and that the real object is the subproblem graph. Open Week 8 by
asking what the state is for matrix chain multiplication *before* writing any recurrence, and refer
back to this lab when someone reaches for a table too early.

If Part D went badly, it is worth five minutes rather than a deduction: the misconception it targets
(that the two techniques are interchangeable) is repeated in most textbooks, including the one they
are reading.

---

*CS 102 · Week 7 · Lab 7 Solutions · © CSE Department*
