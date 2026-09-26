# CS 101 · Problem Set 10 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: the set no longer asks old A1, A2, A3(a)–(c), B3 or B4 — Lab 10 covers them — so
those answers below serve the lab. Old A3(d) → A1 (4), A4 → A2 (6/6), B1 → B1 (14), B2 → B2 (22),
B5 → B3 (18), C (30).)*

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
