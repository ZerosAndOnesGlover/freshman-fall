# CS 101 · Problem Set 9 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

## Answer Key (Instructor Copy)

*(Revised 2026-09-26: the set no longer asks old A1, A3(b)–(c), A4, B3, B4 or `valid_email` — Lab 9 covers
them — so their answers below serve the lab. Old A2 → A1, A3(a) → A2, B5 → B3. Marks: A1 6/4/4, A2 6,
B1 14, B2 14, B3 8 each for `split_fields`, `collapse_whitespace`, `find_doubled_words`, C 28.)*

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
