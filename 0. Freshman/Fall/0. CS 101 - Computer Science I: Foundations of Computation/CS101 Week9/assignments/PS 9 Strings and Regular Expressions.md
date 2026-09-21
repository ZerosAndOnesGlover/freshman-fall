# CS 101 · Problem Set 9
## Strings, Text Processing, and Regular Expressions

**Released:** Friday 27 November 2026, 10:00 (after L30) · Week 9
**Due:** Friday 4 December 2026, 17:00 · Week 10 — late penalty from 17:01
**Submission:** `ps9.py` and your answer sheet in `"$CS101/week9"`, committed to the Freshman Fall repo.
**Total:** 100 points · **Expected time:** about 4 hours

**What this uses:** Weeks 0–9 — strings, encoding and `unicodedata` (L28), text algorithms, the
accumulator pattern, and `csv.reader(io.StringIO(line))` for one line (L29), and the `re` module:
`match`/`search`/`fullmatch`, groups and named groups, `re.VERBOSE`, backreferences, `re.sub`,
backtracking (L30). **Not needed:** reading files (Week 10), `re.IGNORECASE` (never taught).

---

## Overview

This problem set exercises the three ideas of Week 9: strings as an immutable data structure with a
real cost model, the algorithms that operate on them, and regular expressions as a declarative
pattern language.

Written answers go in this file. Code goes in `ps9.py`, scaffolded by `ps9_starter.py`.

**Every function you write must handle the empty string.** Half the defects in text-processing code
live there, and the test suite checks it.

> **📌 Project 1 was due today at 17:00.** Submit it before starting this set.

---

## Part A: Written Questions (28 points)

### A1: Immutability and Cost (7 points)

(a) Explain why `s += c` inside a loop over `n` characters is Θ(n²), and state the exact number of
character copies performed. *(2 pts)*

(b) A student benchmarks the naive loop and finds it only ~5× slower than `"".join(parts)`, not
quadratically slower. Explain the CPython behaviour responsible, and describe a modification to the
benchmark that reveals the true complexity. *(3 pts)*

(c) State why relying on that behaviour in production code is unwise. *(2 pts)*

### A2: Encoding (8 points)

(a) Give `len(s)` and `len(s.encode("utf-8"))` for each of `"hello"`, `"café"`, `"日本語"`, `"👋🏽"`,
and explain in one sentence why the last has `len(s) == 2`. *(4 pts)*

(b) `"é" == "é"` can evaluate to `False`. Give the two code-point sequences and the standard-library
call that repairs the comparison. *(2 pts)*

(c) A web form stores usernames as dict keys without normalising. Describe the concrete failure a
user experiences, and state where in the program the normalisation belongs. *(2 pts)*

### A3: Regular Expressions (8 points)

(a) State the difference between `re.match`, `re.search`, and `re.fullmatch`, and say which you
must use for **validation** and why. *(3 pts)*

(b) `re.findall(r"<.+>", "<a><b>")` returns one match, not two. Explain, and give the one-character
fix. *(2 pts)*

(c) Explain why no regular expression can correctly strip tags from arbitrary HTML. Name the two
language classes involved. *(3 pts)*

### A4: Catastrophic Backtracking (5 points)

The pattern `^(a+)+$` takes 983 ms on 24 `a`s followed by `!`, while `^a+$` handles 100,000
characters in 1.2 ms.

(a) Explain the mechanism causing the exponential blow-up. *(2 pts)*
(b) Name the attack class. *(1 pt)*
(c) Give two structural rules for avoiding vulnerable patterns. *(2 pts)*

---

## Part B: Python Implementation (60 points)

Implement each function in `ps9.py`. Docstrings and tests are in the starter file.

### B1: Text Normalisation and Counting (12 points)

```python
def normalise(text):
    """NFC-normalise and casefold. Returns a str."""

def word_frequencies(text):
    """Return a Counter of normalised words. Words are runs of [\\w'].
       word_frequencies("The the QUICK") -> Counter({'the': 2, 'quick': 1})"""
```

Both must treat `"café"` written with a combining accent as the same word as the precomposed form.

### B2: Palindromes, Two Pointers (10 points)

```python
def is_palindrome(s):
    """True if s reads the same forwards and backwards, ignoring case,
       punctuation, and Unicode composition differences.
       MUST use two pointers and O(1) extra space — no slicing, no filtered list."""
```

Required to pass: `""`, `"x"`, `"ab"`, `"racecar"`, `"A man, a plan, a canal: Panama"`, `"Été"`,
and `"!!!"` (all-punctuation → `True`).

### B3: Naive Search and Its Cost (12 points)

```python
def naive_search(haystack, needle):
    """Return (index, comparisons) where index is the first match or -1,
       and comparisons counts character comparisons performed.
       An empty needle matches at index 0 with 0 comparisons."""
```

Your index must agree with `str.find` on every test case. Then answer in **this file**:

> **B3(d) (3 of the 12 pts):** Run your function on a haystack of `n` a's and a needle of `k` a's
> followed by `b`, for `(n,k)` in `(8,3)`, `(2000,50)`, `(8000,50)`. Report the comparison counts,
> give the closed-form formula, and confirm your measurements match it.

### B4: Log Parsing with Named Groups (12 points)

```python
def parse_logs(lines):
    """Parse lines of the form '2026-07-26 11:02:33 ERROR disk full'.
       Return a list of dicts with keys date, time, level, message.
       Malformed lines are SKIPPED, not raised on."""
```

Use `re.VERBOSE` with named groups and anchor the pattern at both ends.

### B5: Validation and Splitting (14 points)

```python
def valid_email(s):
    """Loose structural check: local@domain.tld. Use fullmatch."""

def split_fields(line):
    """Split one line of comma-separated fields, correctly handling
       quoted fields that contain commas.
       split_fields('name,\"Smith, John\",42') -> ['name', 'Smith, John', '42']"""

def collapse_whitespace(s):
    """Replace every run of whitespace with a single space; strip the ends."""

def find_doubled_words(text):
    """Return each word that appears twice in a row, exactly (same case),
       using a backreference as in L30 §3.
       find_doubled_words('the the quick Fox fox fox') -> ['the', 'fox']"""
```

`split_fields` must **not** be a hand-rolled parser — use the right module and say which in a
comment.

---

## Part C: Applied — Log Analyser (12 points)

Write `analyse_log(lines)` in `ps9.py`. Given a **list of log lines** (reading them from a file is
Week 10's topic), it returns a dict:

```python
{
  "total_lines":     int,   # lines given
  "parsed":          int,   # well-formed lines
  "malformed":       int,   # skipped
  "by_level":        Counter,          # {'ERROR': 3, 'INFO': 12, ...}
  "busiest_hour":    str,              # e.g. '11'
  "top_words":       list[tuple],      # 5 most common message words
}
```

Requirements:
- One pass over `lines`; reuse `parse_logs`'s pattern.
- Build the word list with the accumulator pattern (append to a list), not string `+=`.
- Malformed lines are counted, never crash the run; an empty list gives zeros and `busiest_hour` `None`.

Test it on the eight-line sample `SAMPLE_LOG` in the starter.

---

## Grading Rubric

| Part | Points | Focus |
|---|---|---|
| A1–A4 (written) | 28 | Cost model, encoding, regex semantics, ReDoS |
| B1–B2 | 22 | Normalisation, two-pointer palindrome |
| B3 | 12 | Naive search + measured cost analysis |
| B4–B5 | 26 | Named groups, validation, correct splitting |
| C | 12 | Log analyser |
| **Total** | **100** | |

**Automatic deductions:** any function that crashes on `""`; using `+=` in a loop to build a
string; hand-rolling CSV parsing; using `search` where `fullmatch` is required.

---

## Answer Key (Instructor Copy)

*All code below was executed; every stated output is real.*

### A1

**(a)** Each `+=` allocates a new string and copies everything accumulated so far, so the character
copies total `1 + 2 + … + n = n(n+1)/2` — **Θ(n²)**.

**(b)** CPython resizes the string **in place** when its reference count is 1, which the naive loop
satisfies. To reveal the true cost, keep a live alias:

```python
s = ""; keep = []
for c in src:
    s += c
    keep.append(s)
```

Measured: **1.13 ms, 20.1 ms, 313.7 ms** at n = 2000, 8000, 32000 — quadrupling n multiplies time
by ~16 = 4². Award full marks for any method that defeats the refcount optimisation.

**(c)** The optimisation vanishes the moment the string is stored, returned, or aliased — all
routine in real code. A program whose complexity class depends on an accident of reference counting
will change behaviour under refactoring that looks harmless.

### A2

**(a)** `hello` 5/5; `café` 4/**5**; `日本語` 3/**9**; `👋🏽` **2**/**8**. The last is two code
points — a base emoji plus a skin-tone modifier — rendered as one glyph.

**(b)** `U+00E9` (precomposed, `len` 1) versus `U+0065 U+0301` (`e` + combining acute, `len` 2).
Repair with `unicodedata.normalize("NFC", s)`.

**(c)** A user registers with one form and logs in with the other — trivially possible across
operating systems and input methods — and is **not found**, because `hash` follows `==` and the two
spellings land in different buckets. Normalisation belongs **at the input boundary**, before the
text is used as a key, compared, or stored.

### A3

**(a)** `match` anchors at position 0; `search` finds a match anywhere; `fullmatch` requires the
**entire** string to match. **Validation requires `fullmatch`** — `search(r"\d{4}", x)` accepts
`"drop table; 1234"` because it only asks whether the pattern occurs somewhere.

**(b)** `.+` is **greedy**: it runs to the end, then backtracks to the *last* `>`, producing one
match spanning both tags. Fix: `<.+?>` — the `?` makes it lazy, giving `['<a>', '<b>']`.

**(c)** Regular expressions describe **regular languages**, which cannot count unbounded nesting.
HTML is **context-free**. Concretely, `re.sub(r"<.*?>", "", '<a href="a>b">link</a>')` returns
`'b">link'` — the lazy quantifier stops at the `>` inside the attribute. This is a theorem, not an
implementation limit; CS 301 proves it.

### A4

**(a)** `^(a+)+$` is **ambiguous**: a run of n a's can be partitioned among the outer repetitions in
exponentially many ways. When `$` fails on the `!`, the backtracking engine tries every partition
before reporting failure. Measured: 15.9 → 60.7 → 246.8 → 983.5 ms for 18 → 24 characters — roughly
×4 per two characters, i.e. Θ(2ⁿ). `^a+$` admits one parse, so there is nothing to backtrack.

**(b)** **ReDoS** — regular expression denial of service.

**(c)** (i) Avoid **nested quantifiers over overlapping alternatives** — `(a+)+`, `(a*)*`, `(x|xx)+`.
(ii) Prefer **specific character classes and anchors** — `[^"]*` rather than `.*` inside quotes, so
the engine has no choice about where to stop. Also acceptable: use a non-backtracking engine (RE2).

### B — Reference Implementations

```python
import re, unicodedata, csv, io
from collections import Counter

def normalise(text):
    return unicodedata.normalize("NFC", text).casefold()

def word_frequencies(text):
    return Counter(normalise(w) for w in re.findall(r"[\w']+", text))

def is_palindrome(s):
    s = unicodedata.normalize("NFC", s)          # once, on the whole string
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum(): i += 1
        while i < j and not s[j].isalnum(): j -= 1
        if s[i].casefold() != s[j].casefold(): return False
        i += 1; j -= 1
    return True

def naive_search(haystack, needle):
    n, m = len(haystack), len(needle)
    if m == 0: return 0, 0
    comparisons = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if haystack[i + j] != needle[j]: break
            j += 1
        if j == m: return i, comparisons
    return -1, comparisons

LOG = re.compile(r"""
    ^(?P<date>\d{4}-\d{2}-\d{2})\s+
     (?P<time>\d{2}:\d{2}:\d{2})\s+
     (?P<level>[A-Z]+)\s+
     (?P<message>.+)$
""", re.VERBOSE)

def parse_logs(lines):
    out = []
    for line in lines:
        m = LOG.match(line)
        if m:                       # skip malformed, do not raise
            out.append(m.groupdict())
    return out

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
def valid_email(s):
    return EMAIL.fullmatch(s) is not None

def split_fields(line):
    return next(csv.reader(io.StringIO(line)))   # csv handles quoting

def collapse_whitespace(s):
    return re.sub(r"\s+", " ", s).strip()

def find_doubled_words(text):
    return re.findall(r"\b(\w+)\s+\1\b", text)
```

**Verified output:**

```
word_frequencies("The the QUICK quick fox") -> [('the',2), ('quick',2), ('fox',1)]
is_palindrome: '' T | 'x' T | 'ab' F | 'racecar' T | 'A man, a plan...' T | 'Été' T | '!!!' T
naive_search('hello world','world') -> (6, 11)   str.find -> 6   ✓
naive_search('abc','')             -> (0, 0)     str.find -> 0   ✓
parse_logs(3 lines, 1 malformed)   -> 2 dicts, malformed skipped
find_doubled_words('the the quick Fox fox fox') -> ['the', 'fox']
collapse_whitespace('  a   b \t\n c  ') -> 'a b c'
valid_email: bob@example.com T | a@b.co T | not-an-email F | @x.com F | a@b F
split_fields('name,"Smith, John",42') -> ['name', 'Smith, John', '42']
```

**Part C — reference** (run; uses `LOG` from above):

```python
SAMPLE_LOG = [
    "2026-12-01 09:15:02 INFO server started",
    "2026-12-01 11:02:33 ERROR disk full",
    "2026-12-01 11:05:10 WARN disk nearly full",
    "this line is not a log entry",
    "2026-12-01 11:40:00 ERROR disk full again",
    "2026-12-01 14:00:00 INFO backup complete",
    "2026-12-01 11:59:59 INFO user login",
    "",
]

def analyse_log(lines):
    by_level = Counter()
    hours = Counter()
    words = []
    parsed = 0
    for line in lines:
        m = LOG.match(line)
        if not m:
            continue
        parsed += 1
        by_level[m.group("level")] += 1
        hours[m.group("time")[:2]] += 1
        for w in m.group("message").casefold().split():
            words.append(w)
    return {
        "total_lines": len(lines),
        "parsed": parsed,
        "malformed": len(lines) - parsed,
        "by_level": by_level,
        "busiest_hour": hours.most_common(1)[0][0] if hours else None,
        "top_words": Counter(words).most_common(5),
    }
```

On `SAMPLE_LOG`: `total_lines 8, parsed 6, malformed 2, by_level {INFO: 3, ERROR: 2, WARN: 1},
busiest_hour '11', top_words [('disk', 3), ('full', 3), ('server', 1), ('started', 1), ('nearly', 1)]`.
On `[]`: all zeros, `busiest_hour None`, `top_words []`.

**B3(d).** With a haystack of `n` a's and needle of `k` a's plus `b`, every alignment compares
`k+1` characters and fails, and there are `n−k` alignments:

$$\text{comparisons} = (n-k)(k+1)$$

| (n, k) | Measured | Formula |
|---|---|---|
| (8, 3) | **20** | 5 × 4 = 20 ✓ |
| (2000, 50) | **99,450** | 1950 × 51 = 99,450 ✓ |
| (8000, 50) | **405,450** | 7950 × 51 = 405,450 ✓ |

Θ(n·m). For contrast, `str.find` on the n = 2000 case takes **4.2 µs** against the naive
implementation's **8.47 ms** — about 2000× faster, because CPython uses a two-way
(Crochemore–Perrin) algorithm that is O(n+m).

### Marking notes

- **`is_palindrome` must not build a filtered list** — that is Θ(n) space and the question asks for
  two pointers. Check the inner `while` loops each re-test `i < j`, or `"!!!"` walks off the end.
- **`normalize` applied per character is wrong** — normalisation can merge adjacent code points, so
  it must be applied to the whole string once.
- **`split_fields` using `.split(",")`** fails on the required test case and scores zero for that
  function regardless of other outputs.
- **`parse_logs` without `if m:`** raises `AttributeError` on `None` for the malformed line — the
  single most common regex runtime error.
- **Part C:** looping over `lines` more than once, or crashing on the malformed sample line, loses marks.
