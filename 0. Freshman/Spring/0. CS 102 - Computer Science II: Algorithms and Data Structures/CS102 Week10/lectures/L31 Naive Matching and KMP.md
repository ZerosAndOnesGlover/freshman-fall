# CS 102 · Computer Science II
## Lecture 31: Naive Matching and the Knuth–Morris–Pratt Algorithm

*“Computer programming is an art, because it applies accumulated knowledge to the world, because it requires skill and ingenuity, and especially because it produces objects of beauty.”* — Donald Knuth, "Computer Programming as an Art" (Turing Award lecture, 1974)

**Date:** Monday 29 March 2027 · 09:00–09:50 · Week 10

**Reading:** CLRS §32.1, §32.4 · §32.3 optional

**Coursework:** 📊 **Quiz 10** today 09:00–09:15 · 📋 **Project 2** released today 09:00, due Fri 16 Apr 17:00 · 📘 **Midterm 2** today 18:00–19:15 · 🔬 **Lab 9** Tue 30 Mar 15:00–16:50 · 📝 **PS 10** released Fri 2 Apr 10:00, due Fri 9 Apr 17:00 · 📝 **PS 9** due Fri 2 Apr 17:00

---

## 1. The Problem

Find every occurrence of a pattern $p$ of length $m$ inside a text $t$ of length $n$.

You have used this a thousand times — `Ctrl-F`, `grep`, `str.find`. It is worth knowing that the
obvious algorithm is quadratic and that the fix, published in 1977, is one of the few genuinely
surprising algorithms in this course.

### The naive method

```python
def naive(t, p):
    n, m = len(t), len(p)
    return [i for i in range(n - m + 1)
            if all(t[i+j] == p[j] for j in range(m))]
```

$O(nm)$ in the worst case, and — importantly — **fast on ordinary text**, because a mismatch usually
happens on the first character. The worst case needs a pattern that keeps nearly matching:

| $n$ | $m$ | text | pattern | naive comparisons | $nm$ | KMP |
| --- | --- | --- | --- | --- | --- | --- |
| 1,000 | 10 | `aaa…a` | `aaaaaaaaab` | 9,910 | 10,000 | **1,991** |
| 2,000 | 20 | `aaa…a` | `a…ab` | 39,620 | 40,000 | **3,981** |
| 4,000 | 40 | `aaa…a` | `a…ab` | **158,440** | 160,000 | **7,961** |

*(Verified.)*

**The naive algorithm achieves 99% of its worst-case bound on that input**, and KMP does about $2n$
comparisons regardless.

### Where the waste is

Match `abcabcabd` against `abcabcabx…`:

```
text:    a b c a b c a b x . . .
pattern: a b c a b c a b d
                           ^ mismatch at index 8
```

The naive algorithm now restarts at text position 1 and compares `a` against `b`. But **we already
know** text positions 0–7 are `abcabcab`, so we know positions 1 and 2 cannot start a match. Position
3 can — `abcab` is both a prefix and a suffix of what we matched.

**All of that is a property of the pattern alone.** It can be computed once, before looking at the
text.

---

## 2. Borders and the Failure Function

> A **border** of a string is a proper prefix that is also a suffix.

`abcabcab` has borders `ab` and `abcab`; the longest is `abcab`, of length 5. So after a mismatch we
may slide the pattern forward until that border lines up, and resume — **without moving backwards in
the text.**

> The **failure function** $f[i]$ is the length of the longest border of $p[0 \dots i]$.

| pattern | failure function |
| --- | --- |
| `ababaca` | `[0, 0, 1, 2, 3, 0, 1]` |
| `aaaa` | `[0, 1, 2, 3]` |
| `abcabcabd` | `[0, 0, 0, 1, 2, 3, 4, 5, 0]` |
| `abababab` | `[0, 0, 1, 2, 3, 4, 5, 6]` |

*(Verified against the definition — that $p[:f[i]]$ equals $p[i+1-f[i]:i+1]$ and is maximal — on 2,000
random patterns. **0 mismatches.**)*

### Computing it

The trick is that **the pattern is matched against itself**, using the failure function as it is built:

```python
def failure(p):
    m = len(p); f = [0] * m; k = 0
    for i in range(1, m):
        while k > 0 and p[i] != p[k]: k = f[k-1]     # fall back to a shorter border
        if p[i] == p[k]: k += 1
        f[i] = k
    return f
```

$\Theta(m)$. **The `while` loop looks like it could be expensive and cannot be**, by the same
amortisation argument as the main loop — §3.

The line `k = f[k-1]` is the one to understand: if the current border cannot be extended, **the next
candidate is the longest border of that border**, and $f$ already knows it. Borders of borders are
themselves borders, which is why one array suffices.

---

## 3. The Algorithm

```python
def kmp(t, p):
    if not p: return list(range(len(t) + 1))
    f = failure(p); out = []; k = 0
    for i, ch in enumerate(t):                       # i never decreases
        while k > 0 and ch != p[k]: k = f[k-1]
        if ch == p[k]: k += 1
        if k == len(p):
            out.append(i - len(p) + 1)
            k = f[k-1]                               # keep going for overlaps
    return out
```

**The text index `i` only ever moves forward.** *(Verified: over 500 runs, the text position decreased
**zero** times.)* That is the whole achievement — the naive algorithm's cost comes entirely from
re-reading text it has already seen.

### Why it is $\Theta(n + m)$

The `while` loop can run many times in one iteration, so the bound is not obvious. Use a potential
argument:

- $k$ increases by **at most 1** per character of text — so it increases at most $n$ times in total;
- every `while` iteration **strictly decreases** $k$, and $k \ge 0$.

So the total number of `while` iterations across the whole run is at most the total increase, which is
$n$. **The main loop does at most $2n$ character comparisons.** Same argument for `failure`, giving
$2m$. $\square$

> **This is the third amortised argument of the course** — after Week 3's linear `BUILD-HEAP` and
> Week 6's union-find. All three have the same shape: an operation that is expensive in isolation
> cannot be expensive often, because each expensive step consumes something that was paid for earlier.

*(Verified: KMP agrees with the naive algorithm on 3,000 random (text, pattern) pairs. **0
mismatches.**)*

---

## 4. Two Details That Matter

**Overlapping matches.** After a hit we set `k = f[k-1]` rather than `k = 0`. Searching for `aa` in
`aaaa` finds **three** matches at 0, 1, 2 — which is usually what you want. Setting `k = 0` finds two.
Neither is wrong; know which you have.

**The empty pattern** matches at every position including the end — $n+1$ of them. Every string
algorithm in this lecture needs that case handled explicitly, and it is the most common source of an
off-by-one in a submitted implementation.

---

## 5. Is It Worth It?

Honestly: **usually not, for ordinary text.** The naive algorithm's bad case requires the pattern to
nearly match repeatedly, and English does not do that. Python's `str.find` uses a hybrid of naive
scanning and a Boyer–Moore-style skip, not KMP.

KMP earns its place when:

- the input is adversarial or highly repetitive — **DNA, binary data, log files**;
- you cannot back up in the text at all, because it is **a stream** and you are not storing it;
- you need a **guarantee** rather than good average behaviour.

The third is the honest general reason, and it is the same argument as Week 3's heap sort: **the
worst-case bound is the product, not the average speed.**

The failure function also turns out to be independently useful: it computes all borders of all
prefixes, which answers questions about a string's periodicity that have nothing to do with searching.
PS 10 has one.

---

## 6. What to Do

- Read CLRS §32.1 (naive) and §32.4 (KMP). §32.4's presentation is 1-indexed; convert carefully, as
  in Week 3.
- **PS 10** implements KMP and the failure function, and verifies both against their definitions.
- **Quiz 10 covers Week 9** — greedy and Huffman. Not this material.
- **MIDTERM 2 is this week**, covering Weeks 5–9. See [[CS102 Week10/resources/MIDTERM 2 Revision Guide|MIDTERM 2 Revision Guide]].
- **PROJECT 2 is assigned this week** and due Friday of Week 12.
- Next lecture: Rabin–Karp and Boyer–Moore — one algorithm that hashes and one that skips.

---

*CS 102 · Week 10 · Lecture 31 · © CSE Department*
