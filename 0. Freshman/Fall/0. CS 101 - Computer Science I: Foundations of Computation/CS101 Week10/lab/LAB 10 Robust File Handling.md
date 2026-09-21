# CS 101 · Lab 10
## Robust File Handling: Truncation, Encoding, Exceptions, and Atomic Writes

**Date:** Tuesday 8 December 2026 · 15:00–16:50 · Lab Section (Week 11) — covers Week 10 (L31–L33)
*Duration: 2 hours · 100 points via TA checkoff, part of the Labs component (10%)*

---

## Objectives

1. Reproduce the truncation hazard and prove `atomic_write` prevents it
2. Measure what encoding mistakes actually do to data
3. Establish `try`/`except`/`else`/`finally` ordering empirically
4. Build a defensive CSV loader that survives real malformed input

---

## Setup

```bash
mkdir -p "$CS101/week10" && cd "$CS101/week10"        # set in ~/.bashrc -- see Lab 0
# copy io_lab_starter.py here
python3 --version      # 3.10+
```

---

## Part 1: Modes and the Truncation Hazard (30 minutes)

### Exercise 1.1 — What each mode does

```python
from pathlib import Path
for mode in ("r", "w", "a", "r+", "w+"):
    Path("t.txt").write_text("EXISTING")
    try:
        with open("t.txt", mode) as f:
            pos = f.tell()
        print(f"  {mode:3} tell={pos}  file after = {Path('t.txt').read_text()!r}")
    except OSError as e:
        print(f"  {mode:3} {type(e).__name__}: {e}")
```

**Record the table.** Which modes truncate? At what moment?

### Exercise 1.2 — Losing a file without writing anything wrong

```python
Path("data.txt").write_text("IRREPLACEABLE")
try:
    with open("data.txt", "w") as f:
        raise RuntimeError("simulated failure before writing")
except RuntimeError:
    pass
print(repr(Path("data.txt").read_text()))
```

**Record the output** and explain, in one sentence, what destroyed the data.

### Exercise 1.3 — Atomic write

Implement `atomic_write(path, data)` in the starter: temp file **in the target's directory**,
`fsync` before renaming, `os.replace`, cleanup under `BaseException`. Then prove it:

```python
Path("keep.txt").write_text("ORIGINAL")
try:
    atomic_write_failing("keep.txt", "NEW")     # raises partway through
except RuntimeError:
    pass
print(repr(Path("keep.txt").read_text()))       # should still be ORIGINAL
print("leftover:", list(Path(".").glob("*.tmp")))
```

**Record:** the surviving content, and whether any `.tmp` debris remained.

---

## Part 2: Encoding (20 minutes)

```python
Path("enc.txt").write_text("café 日本語", encoding="utf-8")
print(open("enc.txt", "rb").read())                                    # raw bytes
print(repr(open("enc.txt", encoding="utf-8").read()))                  # correct
try:
    open("enc.txt", encoding="ascii").read()
except UnicodeDecodeError as e:
    print("ascii strict:", e.reason, "at byte", e.start)
print(repr(open("enc.txt", encoding="ascii", errors="replace").read()))  # !!
```

**Record:**

1. The byte string, and how many bytes each of `café` and `日本語` needed.
2. What `errors="replace"` produced.
3. In two sentences: why is the `errors="replace"` result **worse** than the exception?
4. Run `import locale; locale.getpreferredencoding(False)`. What would happen to a program that
   omits `encoding=` and is run on a machine reporting `cp1252`?

---

## Part 3: Exception Mechanics (25 minutes)

### Exercise 3.1 — Ordering

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

print(demo(False))
print(demo(True))
```

**Record both sequences.** When does `else` run, and why would you ever want it?

### Exercise 3.2 — The unreachable clause

```python
def which(broad_first):
    try:
        open("missing.txt")
    except (OSError if broad_first else FileNotFoundError):
        return "OSError" if broad_first else "FileNotFoundError"
    except (FileNotFoundError if broad_first else OSError):
        return "FileNotFoundError" if broad_first else "OSError"

print(which(True), which(False))
print(issubclass(FileNotFoundError, OSError))
```

**Record:** which clause catches in each ordering, and the rule that follows.

### Exercise 3.3 — What a bare `except` swallows

```python
print(issubclass(KeyboardInterrupt, Exception))      # ?
print(issubclass(KeyboardInterrupt, BaseException))  # ?
```

**Record:** name two things `except:` catches that `except Exception:` does not, and why that
matters for a long-running program.

---

## Part 4: A Defensive CSV Loader (30 minutes)

Create a deliberately hostile file:

```python
Path("recs.csv").write_text(
    'name,score\n'
    'Ada,95\n'
    '"Smith, John",88\n'      # quoted comma
    'Bob,notanumber\n'        # bad int
    'Cy\n'                    # missing column
    'Dee,70\n')
```

Implement `load_records(path) -> (good, bad)` where `bad` holds `(line_number, reason)` pairs and
the header counts as line 1.

**Record:**

1. Your `good` and `bad` lists.
2. Which exception type the **short row** raises, and why it is *not* `ValueError`.
3. What `line.split(",")` would have produced for the quoted-comma row.

---

## Part 5: Commit and Reflection (5 minutes)

```bash
git add . && git commit -m "CS 101 Lab 10: robust file handling"
```

### Reflection in `LAB 10 Robust File Handling.md`:

1. Which of these failures would you most likely have shipped before this lab?
2. Part 1 destroyed a file without writing anything wrong. What habit prevents that class of bug
   generally, beyond this one function?
3. Your CSV loader skips bad rows. When would it be better to stop at the first bad row instead?

---

## TA Checkoff Criteria

| Part | Points | Show your TA |
|---|---|---|
| 1 | 30 | Mode table complete; truncation reproduced; `atomic_write` protects the original with no `.tmp` debris |
| 2 | 20 | Byte counts recorded; `errors="replace"` corruption shown and explained |
| 3 | 25 | Both orderings recorded; unreachable-clause rule stated; `BaseException` point made |
| 4 | 25 | Loader handles all three defects; short-row exception type identified correctly |
| **Total** | **100** | Reflection answered and work committed (required) |

---

*CS 101 · Week 10 · Lab 10 · Tuesday 8 December 2026 · © CSE Department*
