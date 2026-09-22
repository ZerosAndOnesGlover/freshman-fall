# CS 102 · Problem Set 10
## String Matching

**Released:** Friday 2 April 2027, 10:00 (after L33) · Week 10
**Due:** Friday 9 April 2027, 17:00 · Week 11 — late penalty from 17:01 (syllabus late policy)
**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4–5 hours

**Submit:** `ps10.py` (runnable end to end) and `ps10.md` (written answers and tables).

## What this problem set uses

Week 10: naive matching, the failure function, KMP and its potential argument (L31), Rabin–Karp and
Boyer–Moore's bad-character rule (L32), suffix arrays by prefix doubling, binary-search queries,
Kasai's LCP array and its applications (L33).

**Not needed and not expected:** Boyer–Moore's good-suffix rule (L32 says it is not covered),
computational geometry (Week 11). No timing is asked for.

> **Midterm 2 was Monday 29 March.** **PROJECT 2 is due Friday 16 April** and Part C of this set is
> directly reusable in it.

---

## Part A — Naive Matching and KMP (31 points)

**A1.** *(5)* `naive(t, p)` returning all match positions, instrumented with a character-comparison
counter.

**A2.** *(7)* `failure(p)` in $\Theta(m)$.

Verify **against the definition** — that $f[i]$ is the length of the longest proper prefix of
$p[0..i]$ that is also a suffix — on at least 1,000 random patterns. Report mismatches.

Give the failure function for `ababaca`, `aaaa`, `abcabcabd`, and `abababab`.

**A3.** *(7)* `kmp(t, p)`. Verify against `naive` on at least 1,000 random (text, pattern) pairs over a
2-letter and a 4-letter alphabet, **including empty patterns and empty texts**. Report mismatches.

**A4.** *(6)* Construct the worst case for naive matching. For $(n, m) \in \{(1000,10), (2000,20),
(4000,40)\}$ report naive's comparison count, $nm$, and KMP's.

State what fraction of the $nm$ bound naive achieves, and what KMP's count is as a multiple of $n$.

**A5.** *(6)* **Prove KMP is $\Theta(n+m)$.**

The `while` loop can run many times in one iteration, so a per-iteration argument does not work. Give
the potential argument: what quantity increases at most once per character, and what does each `while`
iteration do to it?

---

## Part B — Rabin–Karp and Boyer–Moore (26 points)

**B1.** *(7)* `rabin_karp(t, p, base, mod)` with a rolling hash, returning matches **and** a count of
spurious hits (hash matches that fail verification).

Verify against `naive` on at least 1,000 pairs.

**B2.** *(5)* Run it on 20,000 characters over an 8-letter alphabet with a 6-character pattern, using
$\text{mod} = 2^{61}-1$ and $\text{mod} = 101$. Report the spurious-hit count for each.

Then state the worst-case complexity in each case, and what determines it.

**B3.** *(5)* Explain in two sentences why the `t[i:i+m] == p` verification cannot be removed, and what
the algorithm would be without it.

**B4.** *(9)* `boyer_moore(t, p)` with the **bad-character** rule only.

- **(a)** *(4)* Verify against `naive` on at least 1,000 pairs. Explain what the `max(1, ...)` guard
  prevents — construct an input where omitting it fails, and say how.
- **(b)** *(5)* For $n = 200{,}000$ and $m = 8$, report comparisons for Boyer–Moore, naive and KMP over
  alphabets of size 2, 8 and 26, plus Boyer–Moore's comparisons **per text character**.

  State the alphabet size at which Boyer–Moore stops being sublinear, and which algorithm you would
  ship for DNA.

---

## Part C — Suffix and LCP Arrays (32 points)

**C1.** *(6)* `suffix_array(s)` by prefix doubling, verified against directly sorting the suffixes on
at least 300 random strings.

Give the suffix array of `banana` with the suffixes listed in sorted order.

**C2.** *(6)* `sa_search(s, sa, p)` returning all occurrences by binary search, verified against brute
force on at least 300 searches.

State the query complexity and compare it with running KMP per query.

**C3.** *(7)* `lcp_array(s, sa)` by Kasai's algorithm in $\Theta(n)$.

Give the LCP array of `banana`, and verify on at least 300 strings that each entry really is the
longest common prefix of consecutive sorted suffixes.

**C4.** *(7)* **Longest repeated substring** from the LCP array.

Verify against brute force on at least 200 random strings, and report the answer for `banana`,
`mississippi`, `abracadabra`.

> **Your brute-force reference must count *overlapping* occurrences.** `ana` occurs twice in `banana`,
> at positions 1 and 3, and those overlap. A reference written with `str.count` disagrees with the
> correct answer on a substantial fraction of inputs — report how many, and say why.

**C5.** *(6)* The number of **distinct substrings** of $s$ is
$\frac{n(n+1)}{2} - \sum_i \mathrm{LCP}[i]$.

Verify on at least 300 strings against a brute-force set, and **explain the formula in two sentences.**

---

## Part D — Choosing (11 points)

**D1.** *(11)* For each situation, name the algorithm and justify in two sentences:

- **(a)** `grep` for one pattern in a file you have never seen before.
- **(b)** Matching 50,000 virus signatures against a stream, in one pass.
- **(c)** Substring queries against a fixed 3-gigabyte genome, thousands per second.
- **(d)** Finding a pattern in a stream you cannot rewind.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 31 | KMP, the failure function, and the amortised proof |
| B | 26 | Hashing and skipping, and what each depends on |
| C | 32 | Suffix and LCP arrays, and their applications |
| D | 11 | Choosing |
| **Total** | **100** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Counts are deterministic; timings are not.**

**A2** — failure functions:

| pattern | $f$ |
| --- | --- |
| `ababaca` | `[0, 0, 1, 2, 3, 0, 1]` |
| `aaaa` | `[0, 1, 2, 3]` |
| `abcabcabd` | `[0, 0, 0, 1, 2, 3, 4, 5, 0]` |
| `abababab` | `[0, 0, 1, 2, 3, 4, 5, 6]` |

**A4** — text `aaa…a`, pattern `a…ab`:

| $n$ | $m$ | naive | $nm$ | KMP |
| --- | --- | --- | --- | --- |
| 1,000 | 10 | 9,910 | 10,000 | 1,991 |
| 2,000 | 20 | 39,620 | 40,000 | 3,981 |
| 4,000 | 40 | **158,440** | 160,000 | **7,961** |

**B2** — 20,000 characters, 8-letter alphabet, $m = 6$: modulus $2^{61}-1$ gives **0** spurious hits;
modulus 101 gives **214** over 19,995 windows.

**B4(b)** — $n = 200{,}000$, $m = 8$:

| alphabet | Boyer–Moore | naive | KMP | BM per char |
| --- | --- | --- | --- | --- |
| 2 | 298,090 | 398,942 | 276,298 | **1.490** |
| 8 | 46,211 | 228,504 | 224,801 | 0.231 |
| 26 | 28,898 | 207,977 | 207,659 | **0.144** |

**C1 / C3** — `banana`: $\mathrm{SA} = [5, 3, 1, 0, 4, 2]$, $\mathrm{LCP} = [0, 1, 3, 0, 0, 2]$.

**C4** — longest repeated substrings: `banana` → `ana`; `mississippi` → `issi`; `abracadabra` → `abra`.

**C5** — `banana` has **15** distinct substrings; `aaaa` has **4**; `abc` has **6**.

**All verification mismatch counts should be 0.**

---

## A Note on Part C4

C4 asks you to build a brute-force reference and then tells you it will be wrong if you write it the
obvious way.

`str.count` counts **non-overlapping** occurrences: `"aaa".count("aa")` is **1**, not 2. But the
longest repeated substring of `aaa` is `aa`, occurring at positions 0 and 1 — overlapping. A reference
built on `str.count` disagrees with the LCP method on about **22%** of random strings, and **the LCP
method is the one that is right.**

This is the second time this term a *reference implementation* has been the wrong thing (the first was
PS 4's circular verification of the parenthesis theorem). **A verification is only as good as the thing
you verify against**, and "my two implementations disagree" does not tell you which one to fix.

---

*CS 102 · Week 10 · Problem Set 10 · © CSE Department*
