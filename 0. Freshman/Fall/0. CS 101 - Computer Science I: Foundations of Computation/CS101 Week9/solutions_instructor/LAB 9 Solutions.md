# CS 101 — Week 9
## LAB 9 Solutions — INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Absolute timings are
> machine-specific — grade the *ratios* and the conclusions, never the raw milliseconds.

---

## Part 1 — The Concatenation Trap

### 1.1 The misleading benchmark

```
n =  2000  concat   0.225 ms   join 0.056 ms   ratio  4x
n =  8000  concat   0.772 ms   join 0.118 ms   ratio  7x
n = 32000  concat   2.653 ms   join 0.496 ms   ratio  5x
```

A student stopping here concludes `+=` is a small constant factor slower — **linear**. That is the
trap, and it is the point of the exercise.

### 1.2 Defeating the optimisation

```
n =  2000    1.129 ms
n =  8000   20.126 ms      (4x the input -> 17.8x the time)
n = 32000  313.717 ms      (4x the input -> 15.6x the time)
```

**Quadrupling n multiplies the time by ~16 = 4², so the growth is Θ(n²).** Expect ratios in the
15–18 range; anything near 4 means the alias was not actually keeping the string alive.

**Why it works:** CPython contains an optimisation in `unicode_concatenate` — when the target
string's reference count is 1, nobody else can observe it, so the interpreter resizes the existing
buffer instead of allocating and copying. `keep.append(s)` creates a second reference, the refcount
exceeds 1, and the general copying path is taken.

**Expected answer to question 3.** A microbenchmark can hide the very behaviour it is meant to
measure. The naive loop is an unusually favourable case for the optimisation and is *not*
representative of real code, where the accumulated string is stored, returned, passed to a
function, or logged — any of which defeats it. The lesson generalises: **when a measurement
contradicts the theory, suspect the measurement setup before discarding the theory.**

> Award full marks for identifying refcounting as the mechanism. Award partial credit for
> "something in CPython optimises it" *with* a correct honest measurement. Award nothing for
> concluding that concatenation is actually linear.

---

## Part 2 — Substring Search

### 2.1 Reference implementation

```python
def naive_search(haystack, needle):
    n, m = len(haystack), len(needle)
    if m == 0:
        return 0, 0                      # empty needle matches at 0
    comparisons = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if haystack[i + j] != needle[j]:
                break
            j += 1
        if j == m:
            return i, comparisons
    return -1, comparisons
```

Verified against `str.find`:

| Call | Result | `str.find` |
|---|---|---|
| `("hello world", "world")` | `(6, 11)` | 6 ✓ |
| `("aaaa", "aab")` | `(-1, 6)` | −1 ✓ |
| `("abc", "")` | `(0, 0)` | 0 ✓ |
| `("abc", "abc")` | `(0, 3)` | 0 ✓ |

The empty-needle case is the one students omit; `str.find` returns 0 and the implementation must
agree.

### 2.2 The adversarial input (k = 50)

| n | Comparisons | (n−k)(k+1) | Naive | `str.find` |
|---|---|---|---|---|
| 2,000 | **99,450** | 1950 × 51 ✓ | 8.47 ms | **4.2 µs** |
| 8,000 | **405,450** | 7950 × 51 ✓ | 30.2 ms | 12.0 µs |
| 32,000 | **1,629,450** | 31950 × 51 ✓ | 120.9 ms | 116.1 µs |

The formula matches **exactly** — this is arithmetic, not a fit, so any deviation means a bug in
the student's comparison counter (usually counting alignments rather than character comparisons, or
missing the final failing comparison).

Speed ratio at n = 32,000: roughly **1000×**. At n = 2,000 it is about **2000×**.

### 2.3 Expected answer

A failed match tells you *what the characters were* up to the point of failure. Having matched 40
characters of the needle, you know those 40 characters, so you can compute how far to shift without
re-examining them — many alignments can be ruled out without a single comparison. The naive
algorithm discards this and restarts one position later from scratch.

Algorithms exploiting it: **Knuth–Morris–Pratt** (precomputes the longest proper prefix that is
also a suffix), **Boyer–Moore** (scans right-to-left, skips using a bad-character table), and the
**two-way / Crochemore–Perrin** algorithm CPython actually uses.

---

## Part 3 — Regular Expressions

### 3.1 Verified outputs

```
re.findall(r"<.+>",  "<a><b>")            ['<a><b>']
re.findall(r"<.+?>", "<a><b>")            ['<a>', '<b>']
re.match(r"world", "hello world")         None
re.search(r"world", "hello world")        <Match span=(6, 11)>
re.fullmatch(r"\w+", "hello world")       None
re.split(r"[,;]\s*", "a, b; c")           ['a', 'b', 'c']
re.sub(r"\s+", " ", "a   b \t c")         'a b c'
re.findall(r"\b(\w+) \1\b", "the the quick fox fox")   ['the', 'fox']
```

The two most-missed predictions are the greedy `<.+>` (students expect two matches) and
`re.fullmatch(r"\w+", "hello world")` returning `None` (a space is not `\w`).

### 3.2 Log parser

```python
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
        if m:                     # <- skip, do not raise
            out.append(m.groupdict())
    return out
```

Verified: three input lines with one malformed → two dicts returned, malformed silently skipped.

**Three marking points.** `^`/`$` anchor the whole line rather than merely finding the pattern
inside it. `.+` for the message is safe *here* because it is last and anchored by `$`. And `if m:`
is what makes malformed lines skip — without it, `None.groupdict()` raises `AttributeError`, which
is the single most common regex runtime error.

### 3.3 Validation

```python
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
def valid_email(s):
    return EMAIL.fullmatch(s) is not None
```

| Input | `fullmatch` | `search` |
|---|---|---|
| `bob@example.com` | ✓ | ✓ |
| `a@b.co` | ✓ | ✓ |
| `not-an-email` | ✗ | ✗ |
| `@x.com` | ✗ | ✗ |
| **`"hello bob@example.com world"`** | **✗** | **✓ ← wrongly accepted** |

Any input *containing* a valid address is accepted by the `search` version — that is the answer to
look for. Also acceptable: `"bob@example.com; DROP TABLE users"`.

> This is a **real security bug class**, not a curiosity: using a containment test where an equality
> test was intended is a standard validation bypass.

---

## Part 4 — Catastrophic Backtracking

```
18 a's:     15.90 ms
20 a's:     60.70 ms      ratio 3.8x
22 a's:    246.78 ms      ratio 4.1x
24 a's:    983.50 ms      ratio 4.0x
safe ^a+$ on 100000 a's + '!':   1.22 ms
```

**Two extra characters ≈ ×4, so the cost is Θ(2ⁿ).** Extrapolating, 40 characters would take over a
year.

**Expected answer to Q2.** `^(a+)+$` is **ambiguous**: a run of n a's can be partitioned among the
outer group's repetitions in exponentially many ways — `(aaaa)`, `(aaa)(a)`, `(aa)(aa)`,
`(a)(a)(a)(a)`, … When the trailing `!` makes `$` fail, the backtracking engine must try **every**
partition before it can conclude failure.

**Q3.** `^a+$` admits exactly one way to match any given string, so there is nothing to backtrack
through — linear, and 100,000 characters take about a millisecond.

**Q4.** **ReDoS** (regular expression denial of service). Real incidents: the **Cloudflare outage of
2 July 2019**, caused by a WAF rule containing `.*.*=.*`, which took global CPU to 100%; also a
Stack Overflow outage in 2016 from a trailing-whitespace pattern.

> Students sometimes report much larger absolute times on shared machines. Grade the **ratio**
> (should be 3.5–4.5×), not the milliseconds.

---

## Part 5 — Where Regex Stops Working

```
'<a href="x">link</a>'      ->  'link'      (works)
'<a href="a>b">link</a>'    ->  'b">link'   (WRONG)
```

The lazy `.*?` stops at the **first** `>`, which is inside the quoted attribute value, so the
"tag" it removes is `<a href="a>` and the remainder `b">link` survives.

**Expected general statement.** Regular expressions describe **regular languages**; HTML is
**context-free**. Regular languages cannot count arbitrary nesting depth, so no regex can correctly
parse a format that nests inside itself. This is a theorem, not a limitation of Python's engine —
CS 301 proves it, and Week 11 of this course begins building the machinery.

Correct tools: `html.parser` in the standard library, or `lxml` / `BeautifulSoup`.

Accept any answer naming the regular/context-free distinction. Award partial credit for "regex
can't handle nesting" without the language classes.

---

## Part 6 — Concordance, n-grams, and One More Regex Limit

### 6.1 Reference implementation and expected output

```python
def concordance(text):
    index = defaultdict(list)
    for lineno, line in enumerate(text.splitlines(), start=1):
        for word in re.findall(r"[\w']+", line):
            index[normalise(word)].append(lineno)
    return index
```

Verified on the sample text — words spanning both lines:

| Word | Lines | Occurrences |
|---|---|---|
| `the` | 1, 2 | **4** |
| `fox` | 1, 2 | **3** |
| `quick` | 1, 2 | **2** |
| `dog` | 1, 2 | **2** |

Top words overall: `[('the', 4), ('fox', 3), ('quick', 2), ('dog', 2)]`.

**Marking points.** `The` / `the` must collapse to a single entry — a student whose output has both
has skipped `casefold`. Using `defaultdict(list)` rather than `if w not in index` is the L27
grouping pattern and worth a mark. Storing duplicate line numbers (as here) is correct if the
occurrence count is wanted; a `set` is also acceptable if the student states the trade-off.

### 6.2 n-grams

```python
def ngrams(text, n):
    words = [normalise(w) for w in re.findall(r"[\w']+", text)]
    return Counter(tuple(words[i:i+n]) for i in range(len(words) - n + 1))
```

**18 words → 17 bigrams**, confirming the general relationship **(W − n + 1) n-grams from W words**
— the same off-by-one as the alignment count in naive search, and worth pointing out as such.

Complexity: **Θ(W · n)** — there are W − n + 1 slices and each tuple costs Θ(n) to build. For fixed
small n this is Θ(W).

*The keys must be tuples, not lists — lists are unhashable and cannot be Counter keys. That is L25's
hashability rule appearing again.*

### 6.3 Sentence splitting

```
re.split(r"(?<=[.!?])\s+", "A dog. A cat.")
# ['A dog.', 'A cat.']                       correct

re.split(r"(?<=[.!?])\s+", "Dr. Smith went home. He slept.")
# ['Dr.', 'Smith went home.', 'He slept.']   WRONG — 3 pieces, should be 2
```

**Expected answer.** The pattern splits after any `.`, `!`, or `?` followed by whitespace, and the
period in `Dr.` satisfies that. Deciding whether a given period ends a sentence requires knowing
whether the preceding token is an abbreviation — **information the character sequence alone does
not contain**.

Patching with an abbreviation list is not a general fix because the list is unbounded and
context-dependent: `Dr.`, `Mr.`, `Inc.`, `etc.`, `e.g.`, initials like `J. R. R. Tolkien`, decimal
numbers, ellipses, and URLs all break it — and `etc.` genuinely *can* end a sentence, so even a
perfect list does not decide the case.

Real tools use trained statistical models over the surrounding context: `nltk`'s Punkt tokeniser or
spaCy. Accept any answer that identifies the need for context beyond the pattern.

> This is the **third** distinct regex boundary the lab demonstrates: performance (Part 4),
> language class (Part 5), and now *semantic* context (Part 6). Students who articulate all three
> as separate limits have understood the tool properly.

---

## Marking Scheme

Checkoff-graded against the criteria on the handout.

- **Method (≈60%).** Measurements actually taken (not copied from the lecture), required technique
  used, conclusions following from the student's own data.
- **Result (≈40%).** Correct implementations, correct ratios identified, written answers reaching
  the *mechanism* rather than restating the observation.

**Carry-through.** A wrong `naive_search` used consistently in Part 2 costs marks once.

**The three failure modes to watch for:**

1. **Reporting Part 1.1 as the answer** and concluding concatenation is linear. The entire point is
   that 1.2 contradicts it.
2. **Describing what happened without why.** "The regex was slow" is an observation; "the engine
   tried every partition of the a-run before failing" is the answer.
3. **Treating the three regex limits as one.** Performance (Part 4), language class (Part 5), and
   semantic context (Part 6) are independent failures with different fixes; conflating them
   suggests the student has memorised "regex is bad at some things" rather than understanding
   which things.

---

*CS 101 · Week 9 · Lab Solutions · Instructor Copy · © CSE Department*
