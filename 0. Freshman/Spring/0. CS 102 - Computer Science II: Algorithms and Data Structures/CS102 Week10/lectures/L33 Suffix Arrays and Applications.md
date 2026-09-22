# CS 102 · Computer Science II
## Lecture 33: Suffix Arrays and Applications

**Date:** Friday 2 April 2027 · 09:00–09:50 · Week 10

---

## 1. Preprocessing the Text Instead

Every algorithm so far preprocesses the **pattern** and then scans the text. That is right for `grep`,
where the text changes every time. It is wrong for a search engine, where the text is fixed and the
queries keep coming.

Flip it: preprocess the text once, then answer each query in time proportional to the **pattern**.

> A **suffix array** is the array of starting positions of all suffixes of $s$, sorted
> lexicographically.

For `banana`:

| rank | index | suffix |
| --- | --- | --- |
| 0 | 5 | `a` |
| 1 | 3 | `ana` |
| 2 | 1 | `anana` |
| 3 | 0 | `banana` |
| 4 | 4 | `na` |
| 5 | 2 | `nana` |

$$\mathrm{SA} = [5, 3, 1, 0, 4, 2]$$

$n$ integers — **$\Theta(n)$ space**, which is the point. A suffix *tree* answers the same queries
faster but costs 10–20 bytes per character in practice. Suffix arrays largely replaced them for that
reason.

---

## 2. Searching

**Every occurrence of $p$ in $s$ is the start of a suffix beginning with $p$.** Sorted order puts those
suffixes in one contiguous block, so two binary searches find it.

```python
def sa_search(s, sa, p):
    lo = bisect_left (sa, p, key=lambda i: s[i:i+len(p)])
    hi = bisect_right(sa, p, key=lambda i: s[i:i+len(p)])
    return sorted(sa[lo:hi])
```

$O(m\log n)$ — $\log n$ comparisons, each up to $m$ characters. *(Verified against brute force on 500
random searches. **0 mismatches.**)*

Compare with the pattern-preprocessing algorithms: each of those costs $\Theta(n)$ **per query**. For a
1 GB text and a 10-character query, that is a gigabyte read against roughly 300 character comparisons.

**The trade is explicit**: pay $O(n\log n)$ once, then $O(m\log n)$ per query. Worth it above a
handful of queries, and never worth it for a single one.

---

## 3. Construction

Sorting the suffixes directly is $\Theta(n^2\log n)$ worst case — $n$ strings of length up to $n$.

**Prefix doubling** does better. Sort suffixes by their first character, then use those ranks to sort
by the first 2, then 4, then 8 — each round reuses the previous ranks, so comparisons are $O(1)$:

```python
def suffix_array(s):
    n = len(s)
    sa = sorted(range(n), key=lambda i: s[i])
    rank = [0]*n
    for i in range(1, n): rank[sa[i]] = rank[sa[i-1]] + (s[sa[i]] != s[sa[i-1]])
    k = 1
    while k < n and rank[sa[-1]] < n-1:
        key = lambda i: (rank[i], rank[i+k] if i+k < n else -1)
        sa.sort(key=key)                                # each comparison is O(1)
        nr = [0]*n
        for i in range(1, n): nr[sa[i]] = nr[sa[i-1]] + (key(sa[i]) != key(sa[i-1]))
        rank = nr; k *= 2
    return sa
```

$O(n\log^2 n)$ — $\log n$ rounds of an $O(n\log n)$ sort. Replacing the sort with radix sort gives
$O(n\log n)$, and the DC3/skew algorithm achieves $\Theta(n)$.

*(Verified against direct suffix sorting on 500 random strings. **0 mismatches.**)*

Measured, on random DNA-like text:

| $n$ | prefix doubling | sorting suffixes directly |
| --- | --- | --- |
| 2,000 | 6.1 ms | **1.9 ms** |
| 8,000 | 25.0 ms | 19.3 ms |
| 32,000 | **141.0 ms** | 389.0 ms |

**The naive method wins until about $n = 10{,}000$** — Python's `sorted` is C and string slicing is
fast, so the asymptotically worse method has the better constant over a useful range. It is the same
story as Weeks 2, 3, 6 and 8, and by now the response should be automatic: *check where the crossover
is before choosing.*

---

## 4. The LCP Array

Store, alongside the suffix array, the length of the longest common prefix of each suffix and the one
before it in sorted order.

For `banana` with $\mathrm{SA} = [5,3,1,0,4,2]$:

$$\mathrm{LCP} = [0, 1, 3, 0, 0, 2]$$

The 3 says `ana` and `anana` share three characters; the 2 says `na` and `nana` share two.

**Kasai's algorithm computes it in $\Theta(n)$**, which is surprising — it processes suffixes in *text*
order rather than sorted order and exploits the fact that the LCP can drop by at most 1 when you move
to the next text position. It is a fourth amortised argument of exactly the shape you have now seen
three times.

### What it buys

**Longest repeated substring** = the largest LCP entry.

| string | longest repeated substring |
| --- | --- |
| `banana` | `ana` |
| `mississippi` | `issi` |
| `abracadabra` | `abra` |

*(Verified against brute force on 300 random strings — **0 mismatches** — using a reference that counts
**overlapping** occurrences. `ana` occurs twice in `banana` at positions 1 and 3, which overlap, and a
brute force written with `str.count` gets this wrong.)*

Also: the number of **distinct substrings** is $\frac{n(n+1)}{2} - \sum \mathrm{LCP}$, and the
**longest common substring of two strings** is found by concatenating them with a separator and looking
for the largest LCP between suffixes originating in different halves.

---

## 5. Applications

**Search engines.** A suffix array over the concatenated corpus supports substring search directly.
Real engines use an **inverted index** instead — word to document list — because most queries are
word-level and an inverted index is smaller and easier to distribute. Suffix arrays win where queries
are *not* word-aligned: source code, DNA, logs, CJK text without spaces. **Project 2 builds one of
each.**

**Bioinformatics.** A genome is 3×10⁹ characters with a 4-letter alphabet and no word boundaries, and
it is searched constantly with a fixed text. This is exactly the case suffix arrays were designed for.
The FM-index — a compressed relative built on the Burrows–Wheeler transform — is what `bwa` and
`bowtie` actually use, and it stores an index *smaller than the genome itself*.

**Plagiarism detection.** Long common substrings between documents, which is Lab 10 from the other
direction.

**Data compression.** The Burrows–Wheeler transform is a permutation read off the suffix array; `bzip2`
is BWT plus move-to-front plus Huffman. **Week 9's Huffman is the last stage of a pipeline whose first
stage is this lecture.**

---

## 6. The Week in One Table

| you have | you want | use |
| --- | --- | --- |
| text changes every query | one pattern | naive, or Boyer–Moore |
| adversarial or streamed text | one pattern | **KMP** |
| many patterns, one pass | thousands of patterns | **Rabin–Karp** |
| fixed text, many queries | substring search | **suffix array** |
| fixed text, word queries | word search | inverted index (Project 2) |

**No algorithm here dominates.** Each is the answer to a different question about what stays fixed and
what varies, and identifying that is the skill the week is teaching.

---

## 7. Where Week 10 Leaves You

**MIDTERM 2 is this week** and covers Weeks 5–9 — not this material.

**PROJECT 2 is assigned** and due Friday of Week 12. It builds a search engine from this week's
suffix array, Week 7's edit distance for fuzzy matching, and Week 3's bounded heap for ranking.

**Week 11** turns to geometry and to segment trees, which decompose an interval the way Week 8's
interval DP did. **Week 12** asks which problems have no efficient algorithm at all — and the string
matching in this lecture is a good thing to have fresh, because the first NP-complete problems you
meet are about strings.

---

## 8. What to Do

- Read CLRS §32.3 (finite automata) for a different view of KMP. Suffix arrays are not in CLRS;
  **Sedgewick §6.3** is the standard undergraduate treatment.
- **PS 10** builds a suffix array, an LCP array, and finds the longest repeated substring.
- **Lab 10** is the plagiarism detector.
- **Quiz 10 covers Week 9.**

---

*CS 102 · Week 10 · Lecture 33 · © CSE Department*
