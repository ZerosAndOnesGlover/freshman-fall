# CS 101 · Problem Set 9
## Strings, Text Processing, and Regular Expressions

**Released:** Friday 27 November 2026, 10:00 (after L30) · Week 9
**Due:** Friday 4 December 2026, 17:00 · Week 10 — late penalty from 17:01
**Submission:** `ps9.py` and your answer sheet in `"$CS101/week9"`, committed to the Freshman Fall repo.
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: Lab 9, on Tuesday 1 December, already covers the concatenation trap, `naive_search`
with its cost formula, the log parser, `valid_email`, catastrophic backtracking and regex-vs-HTML. Those
items (old A1, A3(b)–(c), A4, B3, B4 and `valid_email`) left this set, and Part C reuses your Lab 9
parser. The answer key moved out of this handout.)*

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

## Part A: Written Questions (20 points)

### A1: Encoding (14 points)

(a) Give `len(s)` and `len(s.encode("utf-8"))` for each of `"hello"`, `"café"`, `"日本語"`, `"👋🏽"`,
and explain in one sentence why the last has `len(s) == 2`. *(6 pts)*

(b) `"é" == "é"` can evaluate to `False`. Give the two code-point sequences and the standard-library
call that repairs the comparison. *(4 pts)*

(c) A web form stores usernames as dict keys without normalising. Describe the concrete failure a
user experiences, and state where in the program the normalisation belongs. *(4 pts)*

### A2: Regular Expressions (6 points)

State the difference between `re.match`, `re.search`, and `re.fullmatch`, and say which you must use for
**validation** and why.

---

## Part B: Python Implementation (52 points)

Implement each function in `ps9.py`. Docstrings and tests are in the starter file.

### B1: Text Normalisation and Counting (14 points)

```python
def normalise(text):
    """NFC-normalise and casefold. Returns a str."""

def word_frequencies(text):
    """Return a Counter of normalised words. Words are runs of [\\w'].
       word_frequencies("The the QUICK") -> Counter({'the': 2, 'quick': 1})"""
```

Both must treat `"café"` written with a combining accent as the same word as the precomposed form.

### B2: Palindromes, Two Pointers (14 points)

```python
def is_palindrome(s):
    """True if s reads the same forwards and backwards, ignoring case,
       punctuation, and Unicode composition differences.
       MUST use two pointers and O(1) extra space — no slicing, no filtered list."""
```

Required to pass: `""`, `"x"`, `"ab"`, `"racecar"`, `"A man, a plan, a canal: Panama"`, `"Été"`,
and `"!!!"` (all-punctuation → `True`).

### B3: Splitting and Doubled Words (24 points)

```python
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

## Part C: Applied — Log Analyser (28 points)

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
- One pass over `lines`; reuse the named-group pattern from your Lab 9 log parser (Exercise 3.2).
- Build the word list with the accumulator pattern (append to a list), not string `+=`.
- Malformed lines are counted, never crash the run; an empty list gives zeros and `busiest_hour` `None`.

Test it on the eight-line sample `SAMPLE_LOG` in the starter.

---

## Grading Rubric

| Part | Points | Focus |
|---|---|---|
| A1–A2 (written) | 20 | Encoding, regex semantics |
| B1–B2 | 28 | Normalisation, two-pointer palindrome |
| B3 | 24 | Correct splitting, whitespace, backreferences |
| C | 28 | Log analyser |
| **Total** | **100** | |

**Automatic deductions:** any function that crashes on `""`; using `+=` in a loop to build a
string; hand-rolling CSV parsing.

---

*CS 101 · Week 9 · Problem Set 9 · Due Friday 4 December 2026, 17:00 · © CSE Department*
