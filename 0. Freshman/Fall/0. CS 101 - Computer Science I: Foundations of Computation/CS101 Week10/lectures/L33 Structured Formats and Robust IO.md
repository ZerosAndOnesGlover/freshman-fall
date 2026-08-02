# CS 101 · Lecture 33 (Week 10, Lecture 3)
## Structured Formats and Robust I/O

---

## 0. From Bytes to Records

L31 gave you a stream of characters; L32 gave you a way to survive failure. Neither tells you what
the characters *mean*. This lecture covers the two formats you will actually meet — CSV and JSON —
the modern way to handle paths, and the technique that stops a crash from destroying a file.

The through-line is the same as L29's: **the right answer is almost always a library you already
have**, and hand-rolling reintroduces bugs that were solved decades ago.

---

## 1. CSV: Why `split(",")` Is Never Enough

L29 showed one failure — a quoted field containing a comma. Here is the full picture. These four
rows round-trip perfectly through the `csv` module:

```python
rows = [["name", "note",          "score"],
        ["Ada",  "Loves, commas",  95],
        ["Bob",  'He said "hi"',   88],
        ["Cy",   "line1\nline2",   70]]
```

What `csv.writer` actually emits:

```
'name,note,score'
'Ada,"Loves, commas",95'
'Bob,"He said ""hi""",88'
'Cy,"line1'
'line2",70'
```

Three escaping mechanisms are visible, and `split` handles none of them:

1. **A field containing the delimiter** is wrapped in quotes. `split(",")` on row 2 gives
   `['Ada', '"Loves', ' commas"', '95']` — **four fields where there should be three**.
2. **A quote inside a quoted field** is doubled (`""`). No amount of splitting undoes that.
3. **A field containing a newline** spans *two physical lines*. This is the one that destroys
   line-based processing entirely: `for line in f` sees five lines for a four-row file, and any
   per-line parser is now permanently out of step.

Round-tripping the whole thing through `csv` returns the original data exactly — verified `True`.

### Reading

```python
import csv

with open("data.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], row["score"])
# {'name': 'Ada', 'note': 'Loves, commas', 'score': '95'}
```

`DictReader` uses the header row for keys, so downstream code says `row["score"]` instead of
`row[2]` — and keeps working when a column is inserted.

> **Two mandatory details.** Pass **`newline=""`** — the `csv` module handles line endings itself,
> and letting text mode also translate them produces stray blank rows on some platforms. And note
> **every value arrives as a `str`**: `row["score"]` is `'95'`, not `95`. Converting, and deciding
> what to do when conversion fails, is your job.

---

## 2. JSON: What Survives the Round Trip

JSON handles nesting, which CSV cannot. But its type system is smaller than Python's, and the
mismatches are silent:

```python
obj = {"n": 1, "f": 1.5, "s": "x", "b": True,
       "none": None, "list": [1, 2], "dict": {"k": "v"}}
json.loads(json.dumps(obj)) == obj        # True — all of these survive
```

The ones that do not:

| Python | After a JSON round trip | Why |
|---|---|---|
| `(1, 2)` tuple | `[1, 2]` **list** | JSON has one sequence type |
| `{1: "a"}` int key | `{'1': 'a'}` **str key** | JSON object keys are always strings |
| `{1, 2}` set | **`TypeError`** | no set type at all |
| `datetime`, `Decimal` | `TypeError` | not JSON types |

All verified. The tuple and integer-key conversions are the dangerous pair, because they **do not
raise** — your data quietly changes type, and the bug surfaces later when something does
`d[1]` and gets a `KeyError` because the key is now `'1'`.

Malformed input raises usefully:

```python
json.loads("{bad}")
# JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2
```

`JSONDecodeError` carries `.msg`, `.lineno`, `.colno`, and `.pos` — use them in your error message
(L32 §7) rather than printing a bare "invalid JSON".

### Choosing between them

| | CSV | JSON |
|---|---|---|
| Structure | flat rows | arbitrary nesting |
| Types | everything is a string | numbers, booleans, null preserved |
| Size | compact | verbose |
| Streaming | natural, row by row | awkward — usually parse the whole document |
| Human editing | spreadsheets | text editor |

**Tabular and large → CSV. Nested or typed → JSON.** For very large JSON, look at newline-delimited
JSON (one object per line), which restores streaming.

---

## 3. Paths: `pathlib` over String Surgery

A path is not a string, and treating it as one produces code that breaks on the first Windows
machine or the first filename containing a space.

```python
from pathlib import Path

p = Path("/tmp/data") / "records" / "jan.csv"     # the / operator joins
p.name        # 'jan.csv'
p.stem        # 'jan'
p.suffix      # '.csv'
p.parent      # PosixPath('/tmp/data/records')
p.with_suffix(".json")    # PosixPath('/tmp/data/records/jan.json')
```

All verified. The `os.path` equivalents need four separate function calls (`join`, `basename`,
`splitext`, `dirname`) and return bare strings that carry no further behaviour.

`Path` objects also do the work directly:

```python
p.exists(), p.is_file(), p.is_dir()
p.read_text(encoding="utf-8")        # open, read, close — one call
p.write_text(data, encoding="utf-8")
p.mkdir(parents=True, exist_ok=True) # create the whole chain, no error if present
list(p.parent.glob("*.csv"))         # pattern matching over a directory
```

**Never build a path with `+` or f-strings.** `dir + "/" + name` breaks on Windows, doubles the
separator when `dir` already ends in one, and silently produces nonsense when `name` is absolute.
The `/` operator handles all three.

---

## 4. Atomic Writes: Not Losing the File You Are Updating

L31 §7 showed the failure. Here it is precisely, verified:

```python
t = Path("naive.txt")
t.write_text("GOOD DATA")
try:
    with open(t, "w") as f:          # truncates at open()
        raise RuntimeError("crash before writing")
except RuntimeError:
    pass
t.read_text()        # ''   ← the data is gone
```

Nothing was written wrongly. **Opening for writing destroyed the file**, and then an unrelated
failure left you with neither version.

The standard remedy is **write to a temporary file in the same directory, then rename**:

```python
import os, tempfile
from pathlib import Path

def atomic_write(path, data, encoding="utf-8"):
    """Write data to path so that path is never left partially written."""
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())      # force to the physical device
        os.replace(tmp, path)         # atomic on POSIX
    except BaseException:
        os.unlink(tmp)                # never leave debris
        raise
```

Verified: after a simulated crash mid-write the target still held its previous content, and no
`.tmp` files were left behind.

**Four details, each load-bearing:**

1. **The temporary lives in the target's directory.** `os.replace` is atomic only *within a
   filesystem*; a temp file in `/tmp` may be on a different one, and the "rename" becomes a
   copy-then-delete with a window of vulnerability.
2. **`os.replace`, not `os.rename`.** `replace` overwrites an existing target on every platform;
   `rename` fails on Windows if the destination exists.
3. **`fsync` before the rename.** `flush` only reaches the operating system's buffers. Without
   `fsync` the rename can be recorded while the data is still in flight, and a power cut leaves an
   empty file with the right name.
4. **`except BaseException` for cleanup.** Catching only `Exception` leaks the temp file on Ctrl-C.
   The bare `raise` re-raises unchanged — this is cleanup, not handling.

---

## 5. Reading Real-World Files Defensively

Real data is malformed. A parser that raises on the first bad row is useless against a million-row
file with three errors in it. The shape that works:

```python
def load_records(path):
    """Yield well-formed records; count and report the rest."""
    good = bad = 0
    with open(path, newline="", encoding="utf-8", errors="strict") as f:
        for lineno, row in enumerate(csv.DictReader(f), start=2):   # 2: header is line 1
            try:
                yield {"name": row["name"], "score": int(row["score"])}
                good += 1
            except (KeyError, ValueError, TypeError) as exc:
                bad += 1
                logging.warning("line %d: skipping malformed row: %s", lineno, exc)
    logging.info("parsed %d records, skipped %d", good, bad)
```

Four decisions worth naming:

- **`errors="strict"`** (the default) so encoding problems raise rather than corrupting silently —
  the opposite of L31's `errors="replace"` trap.
- **The `try` wraps only the conversion**, not the whole loop, so one bad row skips one row.
- **Specific exceptions.** `KeyError` for a missing column, `ValueError` for `int("abc")`. A bare
  `except` would also swallow your own bugs.
- **Counting and logging**, so "skipped 40,000 of 1,000,000" is visible rather than silent. This is
  L32 §5.2 applied.

**The general rule: be strict about what you accept, and loud about what you reject.** Skipping bad
data is legitimate; skipping it *silently* is not.

---

## 6. CS Connection — Formats Are Contracts

A file format is an **interface between programs that never meet**, quite possibly separated by
years. That has consequences you already know in other guises.

**Versioning.** PROG 101 Week 8 recommends a magic number and version field at the head of any
binary format, so a future reader can reject what it does not understand rather than misinterpret
it. JSON gets this cheaply — add a `"version"` key.

**Robustness.** The parsers above are lenient about extra columns and strict about types. That is
the *robustness principle*: accept liberally, emit conservatively — with the caveat, learned
painfully by the web, that excessive leniency lets malformed data propagate until it becomes the de
facto standard.

**Escaping is where security lives.** Every injection vulnerability — SQL, shell, HTML — is a
failure to escape data crossing a format boundary. The `csv` module doubling quotes is the same
mechanism as a database driver's parameterised query, and the reason to use the library rather than
string concatenation is identical in both cases.

---

## 7. Summary

| Idea | Takeaway |
|---|---|
| `split(",")` cannot parse CSV | Quoted delimiters, doubled quotes, embedded newlines |
| Pass `newline=""` to `open` for CSV | The module handles line endings itself |
| CSV values are always `str` | Convert, and handle conversion failure |
| JSON silently changes tuples → lists, int keys → str | No exception; the bug surfaces later |
| Sets and datetimes are not JSON | `TypeError` at dump time |
| Use `pathlib`, not string surgery | `/` joins; `.stem`, `.suffix`, `.with_suffix` |
| `open(path, "w")` truncates immediately | A later crash leaves nothing |
| Write to a temp file, then `os.replace` | Atomic; same directory, `fsync` first |
| Skip bad rows loudly | Count and log; never `except: pass` |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict each result.

```python
json.loads(json.dumps({"t": (1, 2)}))["t"]        # type?
list(json.loads(json.dumps({1: "a"})).keys())     # value?
json.dumps({1, 2})                                # ?
Path("/tmp/a/b.csv").stem                          # ?
Path("/tmp/a/b.csv").with_suffix(".json")          # ?
```

**2. (Explain.)** A colleague's CSV loader works for months, then breaks on one customer file,
reporting "expected 3 fields, got 4" on some rows and silently mis-aligning others. Give the two
distinct features of CSV most likely responsible, and explain why one of them corrupts *line-based*
processing rather than just one row.

**3. (Build.)** Write `save_scores(path, scores)` that writes a `{name: score}` dict to a CSV file
atomically — the existing file must survive any failure — with a header row and correct quoting.

**4. (Stretch.)** `atomic_write` puts its temporary file in the target's directory, calls `fsync`
before renaming, uses `os.replace` rather than `os.rename`, and cleans up under `BaseException`.
Explain what breaks if each of those four choices is reversed.

### Answers

**1.** `list`, `['1']`, **`TypeError`**, `'b'`, `PosixPath('/tmp/a/b.json')`.

The first two are the silent conversions: JSON has a single sequence type, so tuples come back as
lists; and JSON object keys are always strings, so the integer key `1` returns as `'1'`. **Neither
raises** — code that later does `d[1]` gets a `KeyError` with no obvious cause. Sets have no JSON
representation at all, so `json.dumps({1, 2})` raises
`TypeError: Object of type set is not JSON serializable`.

**2.** The two features are **quoted fields containing the delimiter** and **quoted fields
containing a newline**.

A quoted comma affects one row: `Ada,"Loves, commas",95` splits into four pieces instead of three,
producing exactly the "expected 3, got 4" error.

The embedded newline is worse, and explains the *silent* mis-alignment. A field like
`"line1\nline2"` occupies **two physical lines** in the file:

```
'Cy,"line1'
'line2",70'
```

So `for line in f` yields five lines for a four-row file. Every subsequent row is off by one, and a
line-based parser produces plausible-looking wrong records rather than an error. This is why the
`csv` module reads through its own reader object rather than being handed pre-split lines — it must
track quoting state across physical line boundaries.

(A third possibility worth credit: a doubled quote `""` inside a quoted field.)

**3.**

```python
import csv, io, os, tempfile
from pathlib import Path

def save_scores(path, scores):
    """Write {name: score} to path as CSV, atomically."""
    buf = io.StringIO(newline="")
    writer = csv.writer(buf)
    writer.writerow(["name", "score"])
    for name, score in scores.items():
        writer.writerow([name, score])

    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(buf.getvalue())
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise
```

The structure is: **build the complete output first, then commit it atomically.** Formatting into a
`StringIO` means a formatting error (an unserialisable value, say) raises *before* the temporary
file is even created, so there is nothing to clean up.

`newline=""` appears twice — once on the `StringIO` and once on the real file — because the `csv`
module emits its own `\r\n` and any additional translation would double it.

Accept a version that writes rows directly to the temp file, provided the atomic rename and the
cleanup handler are intact.

**4.** Each reversal breaks a different guarantee.

**Temp file elsewhere (e.g. `/tmp`)** — `os.replace` is atomic only within a filesystem. Across
filesystems it degrades to copy-then-delete, which has a window where the target is partially
written. On some systems it raises `OSError: Invalid cross-device link` instead, which at least
fails loudly.

**No `fsync`** — `flush` only moves data into the operating system's buffers. The rename can be
committed to disk while the file contents are still in RAM, so a power cut leaves a correctly named
file that is **empty or truncated**. This is the failure mode `fsync` exists for, and it is why
databases treat it as a deliberate, measured cost.

**`os.rename` instead of `os.replace`** — on Windows, `rename` **fails if the destination exists**,
so the update never happens. The code works on Linux and breaks on the first Windows machine, which
is the worst kind of portability bug.

**`except Exception` instead of `BaseException`** — `KeyboardInterrupt` and `SystemExit` derive from
`BaseException`, not `Exception` (verified in L32 §2). A Ctrl-C during the write therefore skips
the cleanup and **leaks the temporary file**, and a program interrupted repeatedly litters the
directory with `.tmp` debris.

The common thread: each choice defends against a *different* failure — wrong filesystem, power
loss, wrong platform, wrong signal. That is what makes the function worth memorising rather than
re-deriving.

---

## Reading

- **Python docs — `csv` module** — read the introduction and the `Dialect` discussion
- **Python docs — `json` module** — the conversion tables in particular
- **Python docs — `pathlib`** — skim the whole page; it is short and replaces most of `os.path`
- **Guttag, Ch. 4.6** — files (review)

---

*CS 101 · Week 10 · Lecture 33 (Fri) · © CSE Department*
