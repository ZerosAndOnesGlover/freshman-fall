# CS 101 · Problem Set 10
## Files, I/O, and Error Handling

**Released:** Friday, Week 10 | **Due:** Friday, Week 11 (11:59 PM)
**Total:** 100 points + 8 bonus

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

## Part A: Written Questions (28 points)

### A1: Modes and Truncation (7 points)

(a) For a file containing `EXISTING`, state its contents after `open(path, mode)` followed
immediately by `close()` — no read or write — for `"r"`, `"w"`, `"a"`, `"r+"`, `"w+"`. *(3 pts)*

(b) Explain why `"w"` is dangerous even in a program that never writes anything wrong, and give a
two-line snippet that loses data. *(2 pts)*

(c) When would you use `"x"`, and what does it convert a silent bug into? *(2 pts)*

### A2: Encoding at the Boundary (7 points)

(a) Why should `encoding=` always be passed explicitly to `open()`? Name what decides it otherwise.
*(2 pts)*

(b) Reading a UTF-8 file with `encoding="ascii", errors="replace"` produces no exception. Explain
precisely what it produces and why that is worse than a crash. *(3 pts)*

(c) When is `newline=""` required, and what goes wrong without it? *(2 pts)*

### A3: Exceptions (8 points)

(a) Give the exact execution order for `try`/`except`/`else`/`finally` in both the success and
failure cases. *(2 pts)*

(b) Why does ordering `except OSError` before `except FileNotFoundError` make the second clause
unreachable? *(2 pts)*

(c) Name two things a bare `except:` catches that you almost never want to catch. *(2 pts)*

(d) What does `raise NewError(...) from exc` preserve that a plain `raise NewError(...)` loses?
*(2 pts)*

### A4: EAFP and TOCTOU (6 points)

(a) Explain why `if os.path.exists(p): open(p)` is not safer than `open(p)` in a `try`. Name the bug
class. *(3 pts)*

(b) Measured over 200,000 dict lookups, EAFP took 18.6 ms on hits and 52.7 ms on misses, against
LBYL's 25.9 ms and 14.8 ms. Explain the pattern and state when each style is preferable. *(3 pts)*

---

## Part B: Python Implementation (60 points)

### B1: Counting and Reading (10 points)

```python
def count_lines(path):
    """Number of lines in a text file. Streams; never loads the whole file.
       count_lines on an empty file returns 0."""
```

Then answer in **this file**:

> **B1(b) (3 of the 10 pts):** The naive `while True: line = f.readline(); n += 1; if not line:
> break` overcounts. State by how much, whether it depends on the file's contents, and how this
> differs from C's `while (!feof(f))`.

### B2: Configuration Loading with Custom Exceptions (14 points)

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

### B3: Atomic Writing (12 points)

```python
def atomic_write(path, data, encoding="utf-8"):
    """Write data to path such that path is never left partially written.
       On any failure the original file must be intact and no .tmp debris left."""
```

Your implementation must place the temporary in the **target's directory**, `fsync` before
renaming, use `os.replace`, and clean up under `BaseException`. Then answer:

> **B3(d) (3 of the 12 pts):** For each of those four requirements, state precisely what breaks if
> it is reversed.

### B4: Defensive CSV Loading (14 points)

```python
def load_records(path):
    """Return (good, bad).
       good: list of {"name": str, "score": int}
       bad:  list of (line_number, reason) for every row that could not be parsed.
       Header is line 1, so the first data row is line 2.
       One malformed row must not abort the rest."""
```

Must handle: quoted fields containing commas, a non-numeric score, and a row missing a column.

### B5: Writing and Summarising (10 points)

```python
def save_records(path, records):
    """Write records to a CSV with a header, atomically, with correct quoting."""

def summarise(records):
    """Return {"count": int, "mean": float, "best": name_of_highest_scorer}.
       An empty list gives {"count": 0, "mean": 0.0, "best": None} — not a crash."""
```

---

## Part C: The Pipeline (12 points)

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

## Part D: Challenge (8 bonus points)

**D1 (4 pts).** Extend `load_records` to accept a `strict=False` parameter. When `strict=True`, the
first malformed row raises `SourceMalformed` naming the line number instead of being collected.
Explain in two sentences when a caller should want each mode.

**D2 (4 pts).** Demonstrate the truncation hazard empirically. Write a file, attempt an update that
raises partway through using plain `open(path, "w")`, and show the file is now empty. Repeat using
your `atomic_write` and show the original survives. Include both transcripts.

---

## Grading Rubric

| Part | Points | Focus |
|---|---|---|
| A1–A4 (written) | 28 | Modes, encoding, exception semantics, TOCTOU |
| B1–B2 | 24 | Streaming, custom exceptions, cause preservation |
| B3 | 12 | Atomic write and the four requirements |
| B4–B5 | 24 | Defensive parsing, atomic output, edge cases |
| C | 12 | End-to-end pipeline |
| **Total** | **100** | |
| D (bonus) | +8 | strict mode, empirical truncation demo |

**Automatic deductions:** any `except:` without an exception type; any re-raise losing its cause;
`open()` without an explicit `encoding`; a function that crashes on an empty file; building a path
with `+` or an f-string instead of `pathlib`.

---

## Answer Key (Instructor Copy)

*All code below was executed; every stated output is real.*

### A1

**(a)** `'EXISTING'`, **`''`**, `'EXISTING'`, `'EXISTING'`, **`''`**. Only `"w"` and `"w+"`
truncate — and they do so **at `open()`**, before any write.

**(b)**

```python
Path("data.txt").write_text("IRREPLACEABLE")
with open("data.txt", "w") as f:
    raise RuntimeError("fetch failed")
# data.txt is now ''
```

Verified. Nothing was written incorrectly; the *opening* destroyed the file, and an unrelated
failure then left neither version.

**(c)** `"x"` when creating something that must not already exist. It converts a **silent
overwrite** into a loud `FileExistsError`.

### A2

**(a)** Otherwise the **locale** decides — `locale.getpreferredencoding(False)`, which is `UTF-8`
here and may be `cp1252` elsewhere. The same file then reads differently on different machines.

**(b)** Every undecodable byte becomes **U+FFFD**, irreversibly:
`'café 日本語'` read as ASCII with `errors="replace"` gives `'caf�� ���������'`. It is worse than a
crash because it is **silent and lossy** — the corruption propagates into whatever is stored next,
and the original bytes are unrecoverable. A `UnicodeDecodeError` stops the program at the point of
the problem.

**(c)** Required when reading or writing **CSV**. The `csv` module emits its own `\r\n`; without
`newline=""` text mode translates them again, producing **blank rows between records**.

### A3

**(a)** Success: `try` → `else` → `finally`. Failure: `try` → `except` → `finally`. Verified:
`['try','try-end','else','finally']` and `['try','except','finally']`.

**(b)** `FileNotFoundError` is a **subclass** of `OSError` (verified `True`), and clauses are tested
in written order, so the broad clause matches first and the specific one can never run. Python
issues no warning.

**(c)** **`KeyboardInterrupt`** and **`SystemExit`** — both derive from `BaseException`, not
`Exception` (verified). Catching them makes the program un-interruptible and able to ignore its own
shutdown. Also acceptable: your own `NameError`/`AttributeError` typos, misreported as the expected
failure.

**(d)** `from exc` sets `__cause__`, so the traceback shows both exceptions — *"The above exception
was the direct cause of the following exception."* Without it the original diagnosis is lost, and
you keep only the wrapper's message.

### A4

**(a)** Between `exists()` returning `True` and `open()` running, another process can delete or
replace the file. The check narrows the window without closing it, so the `open` still needs a
handler — and by making failure rare it makes the eventual crash harder to reproduce. Bug class:
**TOCTOU** (time-of-check to time-of-use), a genuine security category.

**(b)** Entering a `try` is nearly free; **raising** is expensive. So EAFP wins when the exception
is rare (18.6 vs 25.9 ms on hits) and loses when it is common (52.7 vs 14.8 ms on misses). Prefer
LBYL when failure is the expected case, e.g. validating untrusted input — **but the correctness
argument outranks this**: where a race is possible, EAFP is the only correct choice regardless.

### B — Reference Implementations

```python
def count_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)


class DataError(Exception): pass
class SourceMissing(DataError): pass
class SourceMalformed(DataError): pass


def read_config(path):
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise SourceMissing(f"config not found: {path}") from e
    except OSError as e:
        raise DataError(f"could not read {path}: {e.strerror}") from e
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise SourceMalformed(f"{path}: bad JSON at line {e.lineno} col {e.colno}: {e.msg}") from e
    if not isinstance(data, dict):
        raise SourceMalformed(f"{path}: expected object, got {type(data).__name__}")
    return data


def atomic_write(path, data, encoding="utf-8"):
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp); raise


def load_records(path):
    good, bad = [], []
    with open(path, newline="", encoding="utf-8") as f:
        for lineno, row in enumerate(csv.DictReader(f), start=2):
            try:
                good.append({"name": row["name"].strip(), "score": int(row["score"])})
            except (KeyError, ValueError, TypeError) as e:
                bad.append((lineno, str(e)))
    return good, bad


def save_records(path, records):
    buf = io.StringIO(newline="")
    w = csv.writer(buf); w.writerow(["name", "score"])
    for r in records:
        w.writerow([r["name"], r["score"]])
    atomic_write(path, buf.getvalue())


def summarise(records):
    if not records:
        return {"count": 0, "mean": 0.0, "best": None}
    scores = [r["score"] for r in records]
    return {"count": len(scores),
            "mean": sum(scores) / len(scores),
            "best": max(records, key=lambda r: r["score"])["name"]}
```

**Verified transcript:**

```
count_lines:  'a\nb\nc\n' -> 3 | 'a\nb\nc' -> 3 | '' -> 0
read_config:  nope.json -> SourceMissing   (cause FileNotFoundError)
              bad.json  -> SourceMalformed (cause JSONDecodeError)
              arr.json  -> SourceMalformed (cause None — shape check, not a parse failure)
atomic_write: after success 'NEW'; after simulated crash the target is unchanged; no .tmp left
load_records on a file with a quoted comma, a bad number, and a short row:
  good: [{'name':'Ada','score':95}, {'name':'Smith, John','score':88}, {'name':'Dee','score':70}]
  bad : [(4, "invalid literal for int() with base 10: 'notanumber'"),
         (5, "int() argument must be a string ... not 'NoneType'")]
save_records round-trip identical: True
summarise: {'count': 3, 'mean': 84.33333333333333, 'best': 'Ada'}
summarise([]): {'count': 0, 'mean': 0.0, 'best': None}
```

**B1(b).** It overcounts by **exactly one, regardless of the file's contents** — `readline()`
returns `""` at EOF and the counter has already been incremented. Verified: 4 for both
`"a\nb\nc\n"` and `"a\nb\nc"`, and 1 for an empty file. C's `while (!feof(f))` has the same root
cause but is **data-dependent**: it overcounts a file ending in a newline and is correct on one that
does not. Python's being consistently wrong is the better failure — it shows up on the first test.

**B3(d).** Temp file **elsewhere**: `os.replace` is atomic only within a filesystem; across one it
degrades to copy-then-delete (or raises `OSError: Invalid cross-device link`). **No `fsync`**: the
rename may be durable while the contents are still buffered, so a power cut leaves a correctly named
empty file. **`os.rename`**: fails on Windows when the destination exists, so the update silently
never happens. **`except Exception`**: `KeyboardInterrupt` derives from `BaseException`, so Ctrl-C
skips cleanup and leaks `.tmp` files.

### Marking notes

- **`load_records` must catch `TypeError` as well as `ValueError`.** A row missing a column gives
  `DictReader` a `None` value, and `int(None)` raises `TypeError`, not `ValueError`. Submissions
  catching only `ValueError` crash on the short row — a required test case.
- **`enumerate(..., start=2)`** — the header is line 1. Off-by-one here makes every reported line
  number wrong, which is precisely what the field is for.
- **`read_config` must check `isinstance(data, dict)`.** Valid JSON can be a list, string, or
  number; a syntactically perfect file can still be the wrong shape.
- **Part C: writing the output before the input is fully validated** is acceptable only if the write
  is atomic; otherwise a mid-stream failure has already truncated the destination.
