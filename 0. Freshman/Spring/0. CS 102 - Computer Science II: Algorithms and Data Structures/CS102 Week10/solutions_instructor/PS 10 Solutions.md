# CS 102 · Problem Set 10 — Solutions
## String Matching

**INSTRUCTOR / TA COPY — not for distribution**

Every number was produced by running code. **Deterministic** figures should match; **machine-dependent**
ones will not.

---

## Part A — Naive and KMP (26)

### A1 (4), A3 (6) — deterministic: 0 mismatches

1,000+ pairs over 2- and 4-letter alphabets, including empty patterns and texts.

**The empty pattern** matches at every position including the end — $n+1$ occurrences. It is the most
common off-by-one here and the handout warns about it, so mark it.

### A2 (6) — deterministic: 0 mismatches

| pattern | $f$ |
| --- | --- |
| `ababaca` | `[0, 0, 1, 2, 3, 0, 1]` |
| `aaaa` | `[0, 1, 2, 3]` |
| `abcabcabd` | `[0, 0, 0, 1, 2, 3, 4, 5, 0]` |
| `abababab` | `[0, 0, 1, 2, 3, 4, 5, 6]` |

*The definition check must be independent — computing $f$ two ways with the same code proves nothing.
A correct reference enumerates $k$ and tests `p[:k] == p[i+1-k:i+1]`. This is the same circularity trap
as PS 4 C3(b); flag it in feedback if a student fell into it twice.*

### A4 (5) — deterministic

| $n$ | $m$ | naive | $nm$ | KMP |
| --- | --- | --- | --- | --- |
| 1,000 | 10 | 9,910 | 10,000 | 1,991 |
| 2,000 | 20 | 39,620 | 40,000 | 3,981 |
| 4,000 | 40 | 158,440 | 160,000 | 7,961 |

Expected: naive reaches **99%** of $nm$; KMP is almost exactly $2n$.

### A5 (5) — the assessed proof

$k$ increases by at most 1 per text character, so it increases at most $n$ times overall. Every
iteration of the inner `while` **strictly decreases** $k$, and $k \ge 0$ throughout. So the total
number of `while` iterations across the entire run is bounded by the total increase, which is $n$.
Hence at most $2n$ comparisons. $\square$

*The mark is for identifying $k$ as the potential and for the "total decrease ≤ total increase"
step. An argument that says "the while loop is usually short" scores 0 — it is a worst-case claim.*

---

## Part B — Rabin–Karp and Boyer–Moore (24)

### B1 (6) — deterministic: 0 mismatches

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

### B4 (8)

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

## Part C — Suffix and LCP Arrays (28)

### C1 (6) — deterministic: 0 mismatches

`banana`: $\mathrm{SA} = [5, 3, 1, 0, 4, 2]$, suffixes in order
`a`, `ana`, `anana`, `banana`, `na`, `nana`.

### C2 (5) — deterministic: 0 mismatches

$O(m\log n)$ per query against KMP's $\Theta(n+m)$. **The suffix array wins once the number of queries
exceeds roughly $\log n$**, ignoring construction; including construction the break-even is higher and
depends on $n/m$.

### C3 (6) — deterministic

`banana`: $\mathrm{LCP} = [0, 1, 3, 0, 0, 2]$.

### C4 (6) — deterministic: 0 mismatches, **with a correct reference**

`banana` → `ana`; `mississippi` → `issi`; `abracadabra` → `abra`.

**The `str.count` trap**: a reference using `s.count(sub) > 1` counts **non-overlapping** occurrences
and disagrees with the LCP method on about **22%** of random strings — 1,100 of 5,000 pooled over ten
independent samples, with per-sample rates ranging from 19.0% to 24.2%. `"aaa".count("aa")` is 1, but `aa` genuinely repeats in `aaa` at positions 0 and 1.

**The LCP method is correct; the naive reference is wrong.**

*Full marks require reporting the disagreement count and correctly identifying which side is wrong.
A student who "fixed" the LCP method to match `str.count` has broken working code — worth a comment,
not just a deduction.*

### C5 (5) — deterministic: 0 mismatches

`banana` **15**, `aaaa` **4**, `abc` **6**.

Expected explanation: there are $\frac{n(n+1)}{2}$ substrings counted with multiplicity — one per
(start, end) pair. Two suffixes adjacent in sorted order share exactly $\mathrm{LCP}[i]$ prefixes,
each of which is a substring already counted by the earlier suffix. Subtracting the LCP sum removes
every duplicate exactly once.

---

## Part D — Choosing (22)

### D1 (6), D2 (6) — machine-dependent

| $n$ | prefix doubling | direct suffix sort |
| --- | --- | --- |
| 2,000 | 6.1 ms | **1.9 ms** |
| 8,000 | 25.0 ms | 19.3 ms |
| 32,000 | **141.0 ms** | 389.0 ms |

Crossover around **$n \approx 10{,}000$**. Expected explanation: direct sorting is
$\Theta(n^2\log n)$ worst case, but its comparisons run in C (`sorted` on strings) while prefix
doubling executes a Python-level key function $\log n$ times. The asymptotically worse method has the
better constant over a useful range.

*This is the sixth appearance of this pattern. Students should recognise it without prompting by now.*

### D3 (6)

| | answer |
| --- | --- |
| **(a)** `grep`, unseen file | **Boyer–Moore** (or naive). No preprocessing of the text is possible; the alphabet is large; the pattern is short. |
| **(b)** 50,000 signatures, one pass | **Rabin–Karp** with a hash set of all patterns, or **Aho–Corasick** if lengths differ. Cost is independent of the number of patterns. |
| **(c)** fixed 3 GB genome, thousands of queries | **Suffix array** (or FM-index). The text is fixed, so pay $O(n\log n)$ once; per-query $O(m\log n)$ beats $\Theta(n)$ by six orders of magnitude. |
| **(d)** unrewindable stream | **KMP.** It never moves backwards in the text, so it needs no buffer. Boyer–Moore and suffix arrays both require random access. |

*(d) is the discriminator — it is the only situation where KMP is uniquely correct rather than merely
guaranteed.*

### D4 (4) — machine-dependent

Expected: `str.find` beats all four student implementations by a large factor, because it is C. The
conclusion is **not** "never write your own" — it is that you write your own when you need something
`str.find` does not do: streaming, many patterns, a fixed text with many queries, or a worst-case
guarantee.

*2 for the measurement, 2 for a conclusion that is not "libraries are always better".*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 26 |
| B | 24 |
| C | 28 |
| D | 22 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. C4 is the question to read first.** It hands students a reference implementation and tells them it
will be wrong. Students who reported the disagreement and correctly identified the LCP method as right
have understood something about verification; students who "corrected" their working LCP code to match
a broken reference have demonstrated the opposite. Both need a written comment.

**2. A2's independence trap** is the same as PS 4 C3(b). If a student fell into it there and again
here, that is a pattern worth naming rather than deducting twice.

**3. MIDTERM 2 was this week.** This set was released after it. Submissions may show midterm fatigue in
Part D; the front three parts are the examinable content and should be marked strictly.

**4. Forward.** Part C's suffix array is **Project 2 Part 3.1** and Part B's rolling hash is **Lab
10**. Say so on the scripts — a student with a clean C1–C3 has already written a quarter of Project 2.

---

*CS 102 · Week 10 · PS 10 Solutions · © CSE Department*
