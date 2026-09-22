# CS 102 · Problem Set 10 — Solutions
## String Matching

**INSTRUCTOR / TA COPY — not for distribution**

Every number was produced by running code. **Deterministic** figures should match; **machine-dependent**
ones will not.

---

> **Revised 2026-09-22.** Removed D1, D2 and D4 (timing the matchers, suffix-array construction and
> `str.find`). D3 is now D1; items re-weighted to keep 100 points.

## Part A — Naive and KMP (31)

### A1 (5), A3 (7) — deterministic: 0 mismatches

1,000+ pairs over 2- and 4-letter alphabets, including empty patterns and texts.

**The empty pattern** matches at every position including the end — $n+1$ occurrences. It is the most
common off-by-one here and the handout warns about it, so mark it.

### A2 (7) — deterministic: 0 mismatches

| pattern | $f$ |
| --- | --- |
| `ababaca` | `[0, 0, 1, 2, 3, 0, 1]` |
| `aaaa` | `[0, 1, 2, 3]` |
| `abcabcabd` | `[0, 0, 0, 1, 2, 3, 4, 5, 0]` |
| `abababab` | `[0, 0, 1, 2, 3, 4, 5, 6]` |

*The definition check must be independent — computing $f$ two ways with the same code proves nothing.
A correct reference enumerates $k$ and tests `p[:k] == p[i+1-k:i+1]`. This is the same circularity trap
as PS 4 C3(b); flag it in feedback if a student fell into it twice.*

### A4 (6) — deterministic

| $n$ | $m$ | naive | $nm$ | KMP |
| --- | --- | --- | --- | --- |
| 1,000 | 10 | 9,910 | 10,000 | 1,991 |
| 2,000 | 20 | 39,620 | 40,000 | 3,981 |
| 4,000 | 40 | 158,440 | 160,000 | 7,961 |

Expected: naive reaches **99%** of $nm$; KMP is almost exactly $2n$.

### A5 (6) — the assessed proof

$k$ increases by at most 1 per text character, so it increases at most $n$ times overall. Every
iteration of the inner `while` **strictly decreases** $k$, and $k \ge 0$ throughout. So the total
number of `while` iterations across the entire run is bounded by the total increase, which is $n$.
Hence at most $2n$ comparisons. $\square$

*The mark is for identifying $k$ as the potential and for the "total decrease ≤ total increase"
step. An argument that says "the while loop is usually short" scores 0 — it is a worst-case claim.*

---

## Part B — Rabin–Karp and Boyer–Moore (26)

### B1 (7) — deterministic: 0 mismatches

### B2 (5) — deterministic

| modulus | spurious hits |
| --- | --- |
| $2^{61}-1$ | **0** |
| 101 | **214** of 19,995 windows |

Expected: with a large modulus, $O(n+m)$ expected. With a small one each spurious hit costs $O(m)$
verification and the worst case is $\Theta(nm)$. **What determines it is the modulus — a parameter the
programmer chooses**, not a property of the input.

### B3 (5)

Without verification the algorithm reports every hash collision as a match — it becomes a
**probabilistic filter**, not a matcher. It would have false positives at a rate depending on the
modulus and would still never have false negatives.

*Accept "it would be Monte Carlo rather than Las Vegas" as a full answer.*

### B4 (9)

**(a) (4)** The `max(1, ...)` prevents a **negative or zero shift**. If the mismatched text character
occurs in the pattern *to the right* of the mismatch position, `j - last[c]` is negative and the
algorithm would move backwards or stall — an infinite loop.

Simplest failing input: pattern `ba`, text `aab`. At $i=0$, $j=1$: `t[1]='a'` vs `p[1]='a'` matches;
$j=0$: `t[0]='a'` vs `p[0]='b'` mismatches, `last['a'] = 1`, so `j - last['a'] = -1`. Without the
guard, $i$ decreases and the loop never terminates.

**(b) (4)** — deterministic

| alphabet | Boyer–Moore | naive | KMP | BM per char |
| --- | --- | --- | --- | --- |
| 2 | 298,090 | 398,942 | 276,298 | **1.490** |
| 8 | 46,211 | 228,504 | 224,801 | 0.231 |
| 26 | 28,898 | 207,977 | 207,659 | **0.144** |

Expected: **Boyer–Moore stops being sublinear between alphabet 2 and 8** — it is already 0.231 at 8, so
the transition is at a small alphabet size. **For DNA (4 letters) the honest answer is that BM's
advantage is marginal**, and KMP's guarantee or a suffix-array index is preferable.

*Accept any well-argued answer for DNA. A student who says "Boyer–Moore, it's sublinear" without
noticing that 4 is close to the binary end has missed the table's point.*

---

## Part C — Suffix and LCP Arrays (32)

### C1 (6) — deterministic: 0 mismatches

`banana`: $\mathrm{SA} = [5, 3, 1, 0, 4, 2]$, suffixes in order
`a`, `ana`, `anana`, `banana`, `na`, `nana`.

### C2 (6) — deterministic: 0 mismatches

$O(m\log n)$ per query against KMP's $\Theta(n+m)$. **The suffix array wins once the number of queries
exceeds roughly $\log n$**, ignoring construction; including construction the break-even is higher and
depends on $n/m$.

### C3 (7) — deterministic

`banana`: $\mathrm{LCP} = [0, 1, 3, 0, 0, 2]$.

### C4 (7) — deterministic: 0 mismatches, **with a correct reference**

`banana` → `ana`; `mississippi` → `issi`; `abracadabra` → `abra`.

**The `str.count` trap**: a reference using `s.count(sub) > 1` counts **non-overlapping** occurrences
and disagrees with the LCP method on about **22%** of random strings — 1,100 of 5,000 pooled over ten
independent samples, with per-sample rates ranging from 19.0% to 24.2%. `"aaa".count("aa")` is 1, but `aa` genuinely repeats in `aaa` at positions 0 and 1.

**The LCP method is correct; the naive reference is wrong.**

*Full marks require reporting the disagreement count and correctly identifying which side is wrong.
A student who "fixed" the LCP method to match `str.count` has broken working code — worth a comment,
not just a deduction.*

### C5 (6) — deterministic: 0 mismatches

`banana` **15**, `aaaa` **4**, `abc` **6**.

Expected explanation: there are $\frac{n(n+1)}{2}$ substrings counted with multiplicity — one per
(start, end) pair. Two suffixes adjacent in sorted order share exactly $\mathrm{LCP}[i]$ prefixes,
each of which is a substring already counted by the earlier suffix. Subtracting the LCP sum removes
every duplicate exactly once.

---

## Part D — Choosing (11)

### D1 (11)

| | answer |
| --- | --- |
| **(a)** `grep`, unseen file | **Boyer–Moore** (or naive). No preprocessing of the text is possible; the alphabet is large; the pattern is short. |
| **(b)** 50,000 signatures, one pass | **Rabin–Karp** with a hash set of all patterns, or **Aho–Corasick** if lengths differ. Cost is independent of the number of patterns. |
| **(c)** fixed 3 GB genome, thousands of queries | **Suffix array** (or FM-index). The text is fixed, so pay $O(n\log n)$ once; per-query $O(m\log n)$ beats $\Theta(n)$ by six orders of magnitude. |
| **(d)** unrewindable stream | **KMP.** It never moves backwards in the text, so it needs no buffer. Boyer–Moore and suffix arrays both require random access. |

*(d) is the discriminator — it is the only situation where KMP is uniquely correct rather than merely
guaranteed.*

## Marking Summary

| Part | Points |
| --- | --- |
| A | 31 |
| B | 26 |
| C | 32 |
| D | 11 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. C4 is the question to read first.** It hands students a reference implementation and tells them it
will be wrong. Students who reported the disagreement and correctly identified the LCP method as right
have understood something about verification; students who "corrected" their working LCP code to match
a broken reference have demonstrated the opposite. Both need a written comment.

**2. A2's independence trap** is the same as PS 4 C3(b). If a student fell into it there and again
here, that is a pattern worth naming rather than deducting twice.

**3. MIDTERM 2 was Monday 29 March.** This set was released after it.

**4. Forward.** Part C's suffix array is **Project 2 Part 3.1** and Part B's rolling hash is what
**Lab 10** says a real fingerprinting system would store. Say so on the scripts — a student with a clean C1–C3 has already written a quarter of Project 2.

---

*CS 102 · Week 10 · PS 10 Solutions · © CSE Department*
