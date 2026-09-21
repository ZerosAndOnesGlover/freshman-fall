# CS 101 · Week 10
## LAB 10 Solutions: INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Timings are machine-specific —
> grade the *ratios* and the conclusions, never the milliseconds.


> Lab sat Tuesday 8 December 2026. Revised 2026-09-21 to fit the 110-minute slot: the old Parts 4 (EAFP
> timing), 5 (TOCTOU) and 7 (SafeStore, which needed `@staticmethod`, never taught) were removed; the
> CSV loader is now Part 4. Marking-scheme notes about SafeStore no longer apply.
---

## Part 1 — Modes and the Truncation Hazard

### 1.1 Verified mode table

| Mode | `tell()` | File afterwards | Missing file |
|---|---|---|---|
| `"r"` | 0 | `'EXISTING'` | `FileNotFoundError` |
| `"w"` | 0 | **`''`** | created |
| `"a"` | **8** | `'EXISTING'` | created |
| `"r+"` | 0 | `'EXISTING'` | `FileNotFoundError` |
| `"w+"` | 0 | **`''`** | created |

**Only `"w"` and `"w+"` truncate, and they do so at `open()` — before any write.** `"a"` positions
at byte 8 (the end) but leaves content intact. Students who answer "when you write" have missed the
point of 1.2.

### 1.2 Verified

```
after crash during open('w'): ''
```

**Opening for writing destroyed the file**; the `RuntimeError` was unrelated and arrived too late to
matter. Expect the one-sentence answer to identify `open()` — not the exception — as the cause.

### 1.3 Reference `atomic_write`

```python
def atomic_write(path, data, encoding="utf-8"):
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp); raise
```

Verified: after a simulated failure the target still read `ORIGINAL`, and `list(Path('.').glob('*.tmp'))`
was empty.

**Four requirements, each load-bearing** — award a mark for each present:

1. **Temp in the target's directory** — `os.replace` is atomic only within a filesystem.
2. **`fsync` before rename** — otherwise the rename can be durable while the data is still buffered.
3. **`os.replace`, not `os.rename`** — `rename` fails on Windows if the destination exists.
4. **`except BaseException`** — `KeyboardInterrupt` is not an `Exception`, so Ctrl-C would leak the
   temp file.

---

## Part 2 — Encoding

```
raw bytes: b'caf\xc3\xa9 \xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'
utf-8    : 'café 日本語'
ascii    : UnicodeDecodeError (ordinal not in range(128)) at byte 3
replace  : 'caf�� ���������'
```

**Byte counts:** `café` needs 5 bytes (the `é` takes 2); `日本語` needs 9 (3 each).

**Expected answer to Q3.** The `errors="replace"` version raises **nothing** and destroys the data
**irreversibly** — every non-ASCII byte became U+FFFD, and the original cannot be recovered. An
exception stops the program at the point of the problem, where it is cheap to diagnose; silent
corruption propagates into whatever is stored or re-encoded next, and is typically discovered
weeks later by a user.

**Q4.** `locale.getpreferredencoding(False)` returns `UTF-8` here. On a `cp1252` machine, a program
omitting `encoding=` reads the same UTF-8 file as mojibake (`café` → `cafÃ©`) — or crashes on bytes
that are invalid in cp1252. **The same code, the same file, different results per machine.** That is
why the encoding must be explicit.

---

## Part 3 — Exception Mechanics

### 3.1 Verified

```
no exception: ['try', 'try-end', 'else', 'finally']
exception   : ['try', 'except', 'finally']
```

`else` runs **only** when the `try` block completed without raising. Its purpose is to keep the
`try` block minimal — only the operation that can fail belongs there — so that an exception from
*subsequent* code is not caught by a handler never intended for it.

### 3.2 Verified

```
which(True) -> 'OSError'          (broad clause first: specific one unreachable)
which(False) -> 'FileNotFoundError'
issubclass(FileNotFoundError, OSError) -> True
```

**Rule: order `except` clauses most specific → most general.** Python issues no warning for the dead
clause, because unreachability is undecidable in general.

### 3.3 Verified

```
issubclass(KeyboardInterrupt, Exception)     -> False
issubclass(KeyboardInterrupt, BaseException) -> True
```

A bare `except:` catches **`KeyboardInterrupt`** and **`SystemExit`**. For a long-running program
that means **Ctrl-C stops working** and the process can ignore its own shutdown — you end up killing
it with `SIGKILL`, losing whatever cleanup it would have done. Accept also "it catches your own
`NameError` typos and misreports them as the expected failure."

---

## Part 4 — Defensive CSV Loader

```python
def load_records(path):
    good, bad = [], []
    with open(path, newline="", encoding="utf-8") as f:
        for lineno, row in enumerate(csv.DictReader(f), start=2):
            try:
                good.append({"name": row["name"].strip(), "score": int(row["score"])})
            except (KeyError, ValueError, TypeError) as e:
                bad.append((lineno, str(e)))
    return good, bad
```

Verified against the hostile file:

```
good: [{'name': 'Ada', 'score': 95},
       {'name': 'Smith, John', 'score': 88},
       {'name': 'Dee', 'score': 70}]
bad : [(4, "invalid literal for int() with base 10: 'notanumber'"),
       (5, "int() argument must be a string ... not 'NoneType'")]
```

**Q2 — the short row raises `TypeError`, not `ValueError`.** `DictReader` fills a missing field with
`None`, and `int(None)` is a *type* error, not a bad *value*. **A submission catching only
`ValueError` crashes on line 5** — this is the discriminating test in the exercise, and it is worth
saying aloud at checkoff because the distinction is not obvious.

**Q3 —** `'"Smith, John",88'.split(",")` gives `['"Smith', ' John"', '88']` — three fields where
there should be two, with stray quotes attached. The `csv` module returns `'Smith, John'` correctly.

**Also check:** `enumerate(..., start=2)`. The header is line 1, so an off-by-one here makes every
reported line number wrong — which defeats the purpose of reporting them.

---

## Marking Scheme

Checkoff-graded against the criteria on the handout.

- **Method (≈60%).** Measurements actually taken, required technique used, conclusions drawn from
  the student's own data.
- **Result (≈40%).** Working implementations, correct tables, written answers reaching the
  *mechanism* rather than restating the observation.

**The four failure modes to watch for:**

1. **"The file got deleted"** for Part 1.2 — no. The file was *truncated by `open`*, and nothing was
   deleted. Precision matters here because the fix follows from the cause.
2. **Catching only `ValueError`** in Part 6 — crashes on the short row. Very common.
3. **Concluding from Part 4 that EAFP is simply faster.** It is faster on hits and materially slower
   on misses; a student who reports one half of the table has not run the other.
4. **A `SafeStore` that passes the happy path but not the corruption tests.** The atomic write is
   the easy half; recovery, repair, and the shape check are where the marks are.

---

*CS 101 · Week 10 · Lab Solutions · Instructor Copy · © CSE Department*
