# CS 101: Week 10 Reading Guide & Resources
## Files, I/O, and Error Handling

---

## Required Reading

### Guttag — *Introduction to Computation and Programming Using Python*
- **Ch. 4.6** — files
- **Ch. 7** — exceptions and assertions (primary this week)

### Python Documentation
- **Errors and Exceptions tutorial**, §8.3–§8.6 — read fully before Thursday
- **Built-in Functions: `open`** — the complete mode and `errors` tables
- **`pathlib`** — skim the whole page; it is short and replaces most of `os.path`
- **`csv` module** — introduction and the `Dialect` discussion
- **`json` module** — the conversion tables in particular

### Optional
- **Python docs — `io`, "Text I/O"** — the encoding and newline machinery behind L31 §4
- **Built-in Exceptions** — skim the hierarchy diagram; know where `OSError` sits

---

## Focused REPL / Experimentation Sessions

### Session A: What the modes actually do (15 min)

```python
from pathlib import Path
for mode in ("r", "w", "a", "r+", "w+"):
    Path("t.txt").write_text("EXISTING")
    with open("t.txt", mode) as f:
        pos = f.tell()
    print(mode, pos, repr(Path("t.txt").read_text()))
```

Then the one that matters:

```python
Path("data.txt").write_text("IRREPLACEABLE")
try:
    with open("data.txt", "w") as f:
        raise RuntimeError("failure before writing")
except RuntimeError:
    pass
Path("data.txt").read_text()      # ''
```

**Question to sit with:** nothing was written incorrectly. What destroyed the file?

### Session B: Encoding is a decision (15 min)

```python
Path("enc.txt").write_text("café 日本語", encoding="utf-8")
open("enc.txt", "rb").read()                                   # count the bytes
open("enc.txt", encoding="utf-8").read()
open("enc.txt", encoding="ascii").read()                       # raises
open("enc.txt", encoding="ascii", errors="replace").read()     # does NOT raise

import locale; locale.getpreferredencoding(False)
```

**Which of those four is the most dangerous, and why is it the one that does not raise?**

### Session C: Exception mechanics (20 min)

```python
def demo(fail):
    log = []
    try:
        log.append("try")
        if fail: raise ValueError("x")
        log.append("try-end")
    except ValueError:
        log.append("except")
    else:
        log.append("else")
    finally:
        log.append("finally")
    return log

demo(False), demo(True)

issubclass(FileNotFoundError, OSError)          # ?
issubclass(KeyboardInterrupt, Exception)        # ?
issubclass(KeyboardInterrupt, BaseException)    # ?
```

Then chaining:

```python
try:
    try: raise ValueError("original")
    except ValueError as e: raise RuntimeError("wrapper") from e
except RuntimeError as e:
    type(e.__cause__), e.__cause__
```

### Session D: EAFP vs LBYL, measured (15 min)

```python
import time
d = {"a": 1}
def bench(key, n=200_000):
    t0 = time.perf_counter()
    for _ in range(n):
        if key in d: _ = d[key]
    lbyl = time.perf_counter() - t0
    t0 = time.perf_counter()
    for _ in range(n):
        try: _ = d[key]
        except KeyError: pass
    return lbyl*1000, (time.perf_counter()-t0)*1000

bench("a")   # hit-heavy
bench("z")   # miss-heavy
```

**Both directions matter.** Running only one half gives exactly the wrong rule.

---

## Quick Reference Card

### Modes

| Mode | Read | Write | Position | Existing file | Missing file |
|---|---|---|---|---|---|
| `r` | ✓ | ✗ | start | preserved | **error** |
| `w` | ✗ | ✓ | start | **truncated at open** | created |
| `a` | ✗ | ✓ | **end** | preserved | created |
| `r+` | ✓ | ✓ | start | preserved | **error** |
| `w+` | ✓ | ✓ | start | **truncated at open** | created |
| `a+` | ✓ | ✓ | **end** | preserved | created |
| `x` | ✗ | ✓ | start | **error** | created |

Add `b` for binary (no decoding, no newline translation).

### Always

```python
with open(path, encoding="utf-8") as f:     # explicit encoding, context manager
    for line in f:                          # stream, don't slurp
        ...
```

### Exception order

```
BaseException
├── KeyboardInterrupt      ← bare `except:` catches these
├── SystemExit             ←
└── Exception              ← catch this at most
    ├── OSError → FileNotFoundError, PermissionError, IsADirectoryError
    ├── LookupError → KeyError, IndexError
    └── ValueError, TypeError, …
```

**Order clauses specific → general.** `try` → `except` → `finally`, or `try` → `else` → `finally`.

### Atomic write (memorise this)

```python
fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
try:
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)
except BaseException:
    os.unlink(tmp); raise
```

Same directory · `fsync` first · `os.replace` · clean up on `BaseException`.

---

## Self-Test

Without notes:

1. Which modes truncate, and at what moment?
2. Why must `encoding=` be explicit? What decides it otherwise?
3. What does `errors="replace"` do, and why is that worse than an exception?
4. Give the execution order of `try`/`except`/`else`/`finally` in both cases.
5. Why is `except OSError` before `except FileNotFoundError` a bug?
6. Name two things a bare `except:` catches that you don't want.
7. What does `raise X from e` preserve?
8. What is TOCTOU, and which style avoids it?
9. When is LBYL faster than EAFP, and why?
10. State the four requirements of a correct atomic write.

*(Answers: 1. `w`, `w+` (and `x` errors instead) — at `open()`, before any write. 2. otherwise the
locale decides, and it differs per machine. 3. replaces undecodable bytes with U+FFFD, silently and
irreversibly — no exception means the corruption propagates. 4. success: try→else→finally; failure:
try→except→finally. 5. `FileNotFoundError` is a subclass, so the broad clause matches first and the
specific one is unreachable. 6. `KeyboardInterrupt` and `SystemExit`. 7. `__cause__` — the original
exception and its traceback. 8. time-of-check to time-of-use; **EAFP** avoids it. 9. when failure is
the common case — entering a `try` is cheap, raising is not. 10. temp in the target's directory,
`fsync` before rename, `os.replace` not `os.rename`, cleanup under `BaseException`.)*

---

## Looking Ahead

**📌 Midterm 2 is this week**, covering Weeks 6–9. Week 10 material is **not** on it — see
`MIDTERM 2 Review and Practice Exam.md`.

**Week 11** turns to **computability** — which problems can be solved by *any* program at all. It
picks up the thread L30 left hanging: regular expressions cannot parse nested structure, and that
was a *theorem*, not an implementation limit. Week 11 builds the machinery for proving statements of
that kind, culminating in the halting problem.

---

*CS 101 · Week 10 · © CSE Department*
