# CS 101 · Problem Set 10
## Files, I/O, and Error Handling

**Released:** Friday 4 December 2026, 10:00 (after L33) · Week 10
**Due:** Friday 11 December 2026, 17:00 · Week 11 — late penalty from 17:01
**Submission:** `ps10.py` and your answer sheet in `"$CS101/week10"`, committed to the Freshman Fall repo.
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: Lab 10, on Tuesday 8 December, already covers file modes and truncation, encoding,
exception ordering, `atomic_write` and the defensive CSV loader. Those items (old A1, A2, A3(a)–(c), B3 and
B4) left this set; B3 and Part C reuse your Lab 10 `atomic_write` and `load_records`. The answer key
moved out of this handout.)*

---

## Overview

This set builds one small program properly: a records pipeline that reads CSV, validates, survives
malformed input, and writes results without ever destroying the file it is updating.

Written answers go in this file. Code goes in `ps10.py`, scaffolded by `ps10_starter.py`.

**Every function must survive a missing file, an empty file, and a malformed row.** The starter's
test suite checks all three.

> **📌 Midterm 2 is this week** and covers Weeks 6–9. See
> [[CS101 Week10/assignments/MIDTERM 2 Review and Practice Exam|MIDTERM 2 Review and Practice Exam]].

---

## Part A: Written Questions (16 points)

### A1: Exception Chaining (4 points)

What does `raise NewError(...) from exc` preserve that a plain `raise NewError(...)` loses?

### A2: EAFP and TOCTOU (12 points)

(a) Explain why `if os.path.exists(p): open(p)` is not safer than `open(p)` in a `try`. Name the bug
class. *(6 pts)*

(b) Measured over 200,000 dict lookups, EAFP took 18.6 ms on hits and 52.7 ms on misses, against
LBYL's 25.9 ms and 14.8 ms. Explain the pattern and state when each style is preferable. *(6 pts)*

---

## Part B: Python Implementation (54 points)

### B1: Counting and Reading (14 points)

```python
def count_lines(path):
    """Number of lines in a text file. Streams; never loads the whole file.
       count_lines on an empty file returns 0."""
```

Then answer in **this file**:

> **B1(b) (4 of the 14 pts):** The naive `while True: line = f.readline(); n += 1; if not line:
> break` overcounts. State by how much, whether it depends on the file's contents, and how this
> differs from C's `while (!feof(f))`.

### B2: Configuration Loading with Custom Exceptions (22 points)

```python
class DataError(Exception): ...
class SourceMissing(DataError): ...
class SourceMalformed(DataError): ...

def read_config(path):
    """Return a dict from a JSON file.
       Raises SourceMissing if absent, SourceMalformed if the JSON is invalid
       OR is valid JSON that is not an object. Any other OS failure raises
       DataError. Every raise must preserve its cause."""
```

### B3: Writing and Summarising (18 points)

Paste your Lab 10 `atomic_write` and `load_records` into `ps10.py` first; `save_records` and Part C use them.

```python
def save_records(path, records):
    """Write records to a CSV with a header, atomically, with correct quoting."""

def summarise(records):
    """Return {"count": int, "mean": float, "best": name_of_highest_scorer}.
       An empty list gives {"count": 0, "mean": 0.0, "best": None} — not a crash."""
```

---

## Part C: The Pipeline (30 points)

Write `run_pipeline(config_path)` in `ps10.py`. It reads a JSON config with keys `input`, `output`,
and optional `min_score` (default 0), then:

1. loads records from `input`, skipping and **reporting** malformed rows,
2. filters to `score >= min_score`,
3. writes the survivors to `output` **atomically**,
4. returns the summary dict from `summarise`.

Requirements:

- Every failure raises a `DataError` subclass with a message naming the file and the problem.
- A malformed input row is skipped and counted, never fatal.
- The output file must survive a crash at any point.
- Nothing is loaded entirely into memory that does not need to be.

---

## Grading Rubric

| Part | Points | Focus |
|---|---|---|
| A1–A2 (written) | 16 | Exception chaining, TOCTOU |
| B1–B2 | 36 | Streaming, custom exceptions, cause preservation |
| B3 | 18 | Atomic output, edge cases |
| C | 30 | End-to-end pipeline |
| **Total** | **100** | |

**Automatic deductions:** any `except:` without an exception type; any re-raise losing its cause;
`open()` without an explicit `encoding`; a function that crashes on an empty file; building a path
with `+` or an f-string instead of `pathlib`.

---

*CS 101 · Week 10 · Problem Set 10 · Due Friday 11 December 2026, 17:00 · © CSE Department*
