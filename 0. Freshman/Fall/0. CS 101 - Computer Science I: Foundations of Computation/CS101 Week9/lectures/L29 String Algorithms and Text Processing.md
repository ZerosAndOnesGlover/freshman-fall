# CS 101 — Lecture 29 (Week 9, Lecture 2)
## String Algorithms: Searching, Tokenising, and Text Processing

---

## 0. From Representation to Algorithms

Wednesday established what a string *is* — an immutable sequence of code points with a specific
cost model. Today we use it. Three problems recur in essentially every program that touches text:

1. **Search** — does this substring occur, and where?
2. **Tokenise** — split this text into meaningful pieces.
3. **Transform** — count, normalise, rebuild.

Each has an obvious solution that is correct and slow, and a better solution that is worth
knowing. More importantly, each has a *wrong* solution that looks right on the example you tested.

---

## 1. The Substring Search Problem

**Given** a haystack of length `n` and a needle of length `m`, find the first index where the needle
occurs, or report absence.

The obvious algorithm tries every alignment:

```python
def naive_search(haystack, needle):
    n, m = len(haystack), len(needle)
    for i in range(n - m + 1):        # every starting position
        j = 0
        while j < m and haystack[i + j] == needle[j]:
            j += 1
        if j == m:
            return i                  # matched all m characters
    return -1
```

**Best case Θ(n):** the needle's first character rarely matches, so each alignment fails
immediately.

**Worst case Θ(n·m):** the needle *almost* matches everywhere. The adversarial input is a haystack
of repeated characters and a needle that repeats then differs — `"aaaa…a"` searched for
`"aaaa…ab"`. Every alignment compares `m` characters before failing on the last.

Measured, with `m = 51`:

| n | Naive comparisons | Naive time | `str.find` |
|---|---|---|---|
| 2,000 | 99,450 | 8.47 ms | **4.2 µs** |
| 8,000 | 405,450 | 30.2 ms | 12.0 µs |
| 32,000 | 1,629,450 | 120.9 ms | 116.1 µs |

The comparison count tracks `n·m` exactly (2000 × 51 ≈ 102,000). And the built-in is **2000× faster**
at n = 2000.

### Why the built-in wins

`str.find` and the `in` operator do not use the naive algorithm. CPython implements a hybrid: a
tuned naive scan for very short needles, and a **two-way algorithm** (Crochemore–Perrin) for longer
ones, giving **O(n + m)** worst case with O(1) extra space.

The key insight behind all fast string search — Knuth–Morris–Pratt, Boyer–Moore, two-way — is the
same: **a failed match tells you something.** If you matched 40 characters of the needle before
failing, you already know what those 40 characters were, so you can skip alignments that cannot
possibly work instead of re-comparing from scratch. Naive search throws that information away at
every step.

> **The practical rule: use `in`, `.find`, and `.index`.** Do not hand-roll substring search. The
> value of knowing the naive algorithm is understanding *why* the built-in is not merely a
> convenience, and recognising the same "reuse what the failure told you" idea when it appears in
> CS 220's string algorithms and in `grep`.

---

## 2. Tokenising: Splitting Text Into Pieces

### The easy case

```python
"the quick brown fox".split()        # ['the', 'quick', 'brown', 'fox']
"a,b,,c".split(",")                  # ['a', 'b', '', 'c']
```

Recall from L28 that bare `split()` collapses whitespace runs while `split(sep)` preserves empty
fields. That distinction *is* the difference between prose and delimited data.

### The case that catches everyone

Here is a CSV line and the obvious way to parse it:

```python
line = 'name,"Smith, John",42'
line.split(",")
# ['name', '"Smith', ' John"', '42']      <- WRONG: four fields, should be three
```

The quoted field contains a comma, and `split` does not know about quoting. The correct tool
already exists:

```python
import csv, io
next(csv.reader(io.StringIO(line)))
# ['name', 'Smith, John', '42']           <- correct
```

**This is the central lesson of tokenising.** The moment your format has *escaping* — quotes,
backslashes, nesting — `split` is no longer sufficient, because splitting is a **flat** operation
and escaping is a **stateful** one. You need a parser that tracks whether it is inside a quoted
region.

The failure mode is nasty because it is data-dependent: the code works perfectly until the first
customer named "Smith, John" appears. It is the exact shape of the `feof` bug in PROG 101 Week 8 —
correct on the data you tested, wrong on the data you will receive.

**Rule: never write your own CSV parser.** Use `csv`. Likewise `json`, `configparser`, and
`urllib.parse` for their formats. Tomorrow's lecture adds regular expressions, which handle a
wider class of splitting — but *still* not nested or escaped structure.

---

## 3. Transformation Patterns

### Palindromes, done properly

```python
import unicodedata

def is_palindrome(s):
    cleaned = [unicodedata.normalize("NFC", ch).casefold()
               for ch in s if ch.isalnum()]
    return cleaned == cleaned[::-1]
```

Verified:

| Input | Result |
|---|---|
| `"racecar"` | `True` |
| `"A man, a plan, a canal: Panama"` | `True` |
| `""` | `True` (vacuously) |
| `"ab"` | `False` |
| `"Été"` | `True` |

Three decisions are doing work here. `isalnum()` discards punctuation and spaces. `casefold()`
makes it case-insensitive — and handles more than `lower()` does. `normalize` means an accented
character typed two different ways still matches itself, which is why `"Été"` works.

The reversal `cleaned[::-1]` costs Θ(n) space. A two-pointer walk is Θ(1) space and worth writing
once (see the exercises), but the slice version is clearer and the constant factor is small.

### Anagrams: three approaches, one wrong

```python
sorted(a) == sorted(b)          # Θ(k log k) — correct, simple
Counter(a) == Counter(b)        # Θ(k)       — correct, and faster
sum(map(ord, a)) == sum(map(ord, b))    # Θ(k)  — WRONG
```

The character-sum "optimisation" is a genuine trap. It is fast and it is broken, because addition
is commutative *and* lossy:

```python
sorted("ad") == sorted("bc")            # False — not anagrams
sum(map(ord, "ad")) == sum(map(ord, "bc"))   # True — 97+100 == 98+99 == 197
```

**Any two strings whose codes happen to sum equally will be declared anagrams.** This is the same
defect as the `charsum` hash function from L25 §3 — order-insensitivity is a *feature* for hashing
into buckets and a *bug* when you need equality. Use `Counter`.

### Word frequency

```python
from collections import Counter
Counter(text.split()).most_common(3)
# [('the', 3), ('fox', 2), ('quick', 1)]
```

Θ(n) in the number of words, and the direct application of L27's counting pattern. Compare against
scanning the list once per distinct word, which is Θ(n·k).

---

## 4. Building Strings: The Accumulator Pattern

L28 established that `+=` in a loop is Θ(n²). The general shape of the fix:

```python
parts = []
for item in source:
    parts.append(transform(item))    # amortised O(1)
result = separator.join(parts)       # one Θ(n) pass
```

This is the **accumulator pattern**, and it generalises beyond strings: accumulate into a mutable
structure, then convert once. You have already used it for lists (L15's `reverse_fast`) and you
will use it for files next week, where the equivalent mistake is opening and closing a file inside
the loop.

For the common cases, Python offers something better than a manual loop:

```python
", ".join(str(x) for x in values)          # generator — no intermediate list
"".join(ch.upper() for ch in s if ch.isalpha())
```

A **generator expression** inside `join` avoids materialising the list at all. `join` still needs
two passes internally (it must know the total length before allocating), so it will consume the
generator into a sequence — but the code is clearer, and for the list-comprehension case the
allocation is identical.

---

## 5. Choosing the Right Tool

| Task | Tool | Not |
|---|---|---|
| Does this substring occur? | `in`, `.find` | hand-written search |
| Split on a fixed delimiter | `.split(sep)` | regex |
| Split on whitespace | `.split()` | `.split(" ")` |
| Delimited data with quoting | `csv` module | `.split(",")` |
| Structured config/data | `json`, `configparser` | anything hand-rolled |
| Flexible pattern matching | **regex** (tomorrow) | nested loops |
| Nested or recursive structure | a real parser | regex |
| Build a string from pieces | `.join` | `+=` in a loop |
| Count occurrences | `Counter` | manual dict updates |

**The pattern to notice: the right answer is almost always "a library you already have".** Text
processing is one of the oldest problems in computing, and the standard library encodes decades of
discovered edge cases — quoting, encodings, locale, escaping. Hand-rolling reintroduces bugs that
were fixed in 1995.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| Naive search is Θ(n·m) worst case | Measured: 1.6 M comparisons at n=32k, m=51 |
| CPython uses a two-way algorithm | O(n+m); 2000× faster than naive on adversarial input |
| Fast search reuses failure information | The idea behind KMP, Boyer–Moore, two-way |
| `split` cannot handle quoting | Use `csv`; the bug is data-dependent and will reach production |
| Palindrome needs normalise + casefold + filter | Three separate decisions, all necessary |
| Char-sum anagram test is broken | `"ad"` and `"bc"` both sum to 197 |
| Accumulate then join | Θ(n) instead of Θ(n²) |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** For `haystack = "aaaaaaaa"` (8 a's) and `needle = "aaab"`, how many character comparisons does `naive_search` perform before returning? Give the general formula for a haystack of `n` a's and a needle of `k` a's followed by `b`.

**2. (Explain.)** This function is supposed to split a line of comma-separated fields. Give an input on which it silently produces the wrong number of fields, and explain why no amount of patching `split` will fix the general case.

```python
def fields(line):
    return line.split(",")
```

**3. (Build.)** Write `is_palindrome(s)` using **two pointers** and Θ(1) extra space, handling punctuation, case, and accents correctly. Explain what your version gains and loses against the slicing version.

**4. (Stretch.)** `sum(map(ord, a)) == sum(map(ord, b))` is a fast, wrong anagram test. Give a counterexample, explain the structural reason it fails, and name the place earlier in this course where the *same* property was desirable rather than a bug.

### Answers

**1.** Each of the alignments compares the 3 matching `a`s and then fails on `b` versus `a` — **4
comparisons per alignment**. There are `n − m + 1 = 8 − 4 + 1 = 5` alignments, so
**5 × 4 = 20 comparisons**, then it returns `-1`.

General formula: with a haystack of `n` a's and a needle of `k` a's plus a final `b`, the needle has
length `m = k + 1`, each alignment costs `k + 1` comparisons, and there are `n − k` alignments:

$$\text{comparisons} = (n-k)(k+1) \in \Theta(n\cdot m)$$

Check against the measured data: `n = 2000, k = 50` gives `1950 × 51 = 99,450` ✓ — exactly the
figure in §1.

**2.** Any input with a **quoted field containing a comma**:

```python
fields('name,"Smith, John",42')
# ['name', '"Smith', ' John"', '42']   — 4 fields, should be 3
```

Patching `split` cannot fix this in general because **splitting is a flat, stateless operation and
quoting is stateful**. To decide whether a given comma is a separator you must know whether you are
currently inside a quoted region, which requires scanning left to right and maintaining state. Add
escaped quotes (`""` inside a quoted field) and embedded newlines — both legal CSV — and you have
written a small parser. That parser already exists as the `csv` module.

The reason this bug reaches production is that it is **data-dependent**: the code is correct for
every input without a quoted comma, which is most of them, right up until it isn't.

**3.**

```python
import unicodedata

def is_palindrome(s):
    s = unicodedata.normalize("NFC", s)
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        if s[i].casefold() != s[j].casefold():
            return False
        i += 1
        j -= 1
    return True
```

**Gains:** Θ(1) extra space instead of Θ(n) — no filtered list, no reversed copy. It also **exits
early** on the first mismatch, so `"ab…"` fails in one comparison rather than after building both
lists.

**Loses:** it is longer and materially harder to get right — the two inner `while` loops must each
re-check `i < j`, or an all-punctuation input walks off the end. The slicing version is four lines
and obviously correct.

Note `normalize` is applied **once to the whole string**, not per character, because normalisation
can merge adjacent code points and so is not safely done in isolation.

**Which to ship?** The slicing version, unless profiling says otherwise. Θ(n) auxiliary space on a
string is rarely the bottleneck, and clarity is worth more than a constant factor.

**4.** Counterexample: `"ad"` and `"bc"`. Neither is an anagram of the other, yet
`97 + 100 = 197 = 98 + 99`, so the test wrongly reports `True`.

The structural reason is that summing is **commutative and lossy** — it maps a multiset of
characters onto a single integer, and many distinct multisets collide on the same total. Order is
destroyed (which the test wants, since anagrams differ only in order) but so is *identity*, which
it needs.

**The same property was desirable in L25**, where a hash function deliberately compresses an
unbounded key space into a small integer range and collisions are unavoidable by the pigeonhole
principle. There, a collision is handled by the table and costs only time. Here, a collision is a
**wrong answer** — because the sum is being used as a test of equality rather than as a bucket
index.

That is the general distinction worth carrying: **a hash may collide because something else checks
equality afterwards.** Using a hash *as* the equality test removes that safety net. The correct
tool is `Counter`, which compares the multisets themselves in Θ(k).

---

## Reading

- **Guttag, Ch. 4** — string methods (review)
- **CLRS, Ch. 32.1** — the naive string-matching algorithm and its analysis (optional; §32.4 covers
  KMP for the ambitious)
- **Python docs — `csv` module** — read the introduction, especially the dialect discussion

---

*CS 101 · Week 9 · Lecture 29 (Thu) · © CSE Department*
