# CS 101 · Lab 10
## Robust File Handling: Truncation, Encoding, Exceptions, and Atomic Writes

**Duration:** 3 hours | **Graded:** TA checkoff on completion and correctness
**Tuesday of Week 11 · Lab Section** — sat after this week's Wed–Fri lectures, and covers Week 10.

---

## Objectives

1. Reproduce the truncation hazard and prove `atomic_write` prevents it
2. Measure what encoding mistakes actually do to data
3. Establish `try`/`except`/`else`/`finally` ordering empirically
4. Measure EAFP against LBYL and find where each wins
5. Build a defensive CSV loader that survives real malformed input

---

## Setup

```bash
mkdir -p cs101/week10 && cd cs101/week10
# copy io_lab_starter.py here
python3 --version      # 3.10+
```

---

## Part 1: Modes and the Truncation Hazard (35 minutes)

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

## Part 2: Encoding (30 minutes)

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

## Part 3: Exception Mechanics (35 minutes)

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

## Part 4: EAFP vs LBYL, Measured (25 minutes)

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
    eafp = time.perf_counter() - t0
    return lbyl, eafp

print("hit :", bench("a"))
print("miss:", bench("z"))
```

**Record:** the four timings. Which style wins on hits? On misses? State the one-sentence rule, then
explain why the **correctness** argument for EAFP (Part 5) outranks this performance one.

---

## Part 5: TOCTOU (15 minutes)

No code required — reason it through and write it up.

```python
if os.path.exists(path):     # ← time of check
    with open(path) as f:    # ← time of use
        ...
```

**Record:** what can happen between those two lines, why adding the check makes debugging *harder*
rather than easier, the name of this bug class, and the version with no window.

---

## Part 6: A Defensive CSV Loader (30 minutes)

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

## Part 7: Build a Crash-Safe Key-Value Store (55 minutes)

This is the main build of the lab. Everything so far has been measurement; now you assemble the
pieces into something that genuinely cannot lose your data.

`SafeStore` is a dict-like store persisted as JSON. It must satisfy four properties:

1. **Durable** — changes survive process exit.
2. **Atomic** — a crash mid-write never leaves a partially written file.
3. **Recoverable** — if the main file is corrupted, a backup is used automatically.
4. **Loud** — unrecoverable corruption raises, with the file and position named.

### Exercise 7.1 — The skeleton

```python
import json, os, shutil, tempfile
from pathlib import Path

class StoreError(Exception): pass
class StoreCorrupt(StoreError): pass

class SafeStore:
    def __init__(self, path, recover=True):
        self.path = Path(path)
        self.backup = self.path.with_suffix(self.path.suffix + ".bak")
        self._data = self._load(recover)
```

### Exercise 7.2 — Reading, strictly

```python
    @staticmethod
    def _read(p):
        """Read one JSON object file. Raises StoreCorrupt on anything unusable."""
        try:
            text = p.read_text(encoding="utf-8")
        except OSError as e:
            raise StoreError(f"cannot read {p}: {e.strerror}") from e
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise StoreCorrupt(
                f"{p}: bad JSON at line {e.lineno} col {e.colno}: {e.msg}") from e
        if not isinstance(data, dict):
            raise StoreCorrupt(f"{p}: expected object, got {type(data).__name__}")
        return data
```

**Note the third check.** Valid JSON can be a list, a string, or a number — a syntactically perfect
file can still be the wrong *shape*, and the store would then break later rather than here.

### Exercise 7.3 — Committing, atomically

Implement `_commit(self, data)`. It must:

- copy the current file to `self.backup` **before** overwriting (only if the file exists),
- serialise with `json.dumps(data, indent=2, sort_keys=True)`,
- write via the atomic pattern from Part 1.3.

`sort_keys=True` is not decoration — it makes the file **diffable**, so a version-control diff shows
what actually changed rather than a reshuffle.

### Exercise 7.4 — Recovery

Implement `_load(self, recover)`:

- file absent → `{}` (a new store, not an error)
- file reads cleanly → return it
- file corrupt **and** `recover` **and** a backup exists → load the backup, **write it back** to the
  main path, and return it
- otherwise → let `StoreCorrupt` propagate

### Exercise 7.5 — The dict-like surface

```python
    def get(self, key, default=None): ...
    def set(self, key, value): ...        # commits immediately
    def delete(self, key): ...            # returns True if it existed
    def keys(self): ...                   # sorted
    def __len__(self): ...
    def __contains__(self, key): ...
```

### Exercise 7.6 — Prove all four properties

Write and run a test for each. Expected results — yours should match:

```python
s = SafeStore(p)
s.set("a", 1); s.set("b", {"nested": [1, 2]})
s.keys()                       # ['a', 'b']
len(s), "a" in s               # 2, True
s.get("zz", "DEFAULT")         # 'DEFAULT'

SafeStore(p).keys()            # ['a', 'b']   ← durable across instances
s.delete("a"), s.delete("a")   # True, False
```

**Corruption without a backup must raise:**

```python
Path("solo.json").write_text("{corrupt")
SafeStore("solo.json")
# StoreCorrupt: solo.json: bad JSON at line 1 col 2: Expecting property name ...
```

**Corruption with a backup must recover:**

```python
s = SafeStore("rec.json"); s.set("x", 10); s.set("y", 20)
# main = {'x': 10, 'y': 20}   backup = {'x': 10}
Path("rec.json").write_text("}}garbage{{")
SafeStore("rec.json").keys()   # ['x']  ← recovered
```

**Record and answer:** the recovered store contains `{'x': 10}`, **not** `{'x': 10, 'y': 20}`. Why?
Is that acceptable? What would it cost to do better, and what is the general name for the trade-off
you are making?

### Exercise 7.7 — Failure injection

Simulate a crash during `_commit` (raise after `mkstemp` but before `os.replace`). Verify:

- the store file is **byte-identical** to before, and
- no `.tmp` files remain.

**Record both.** This is the property the whole design exists for.

---

## Part 8: Commit and Reflection (10 minutes)

```bash
git add . && git commit -m "Week 10 Lab: robust file handling + SafeStore"
```

### Reflection in `LAB 10 Robust File Handling.md`:

1. Which of these failures would you most likely have shipped before this lab?
2. Part 1 destroyed a file without writing anything wrong. What habit prevents that class of bug
   generally, beyond this one function?
3. Parts 4 and 5 point in opposite directions for a miss-heavy workload. How would you decide?
4. `SafeStore` commits on **every** `set`. What does that cost, and what would you change if it were
   called a million times?

---

## TA Checkoff Criteria

- [ ] Part 1: mode table complete; truncation reproduced; `atomic_write` proven to protect the original with no `.tmp` debris
- [ ] Part 2: byte counts recorded; `errors="replace"` corruption shown and explained
- [ ] Part 3: both orderings recorded; unreachable-clause rule stated; `BaseException` point made
- [ ] Part 4: four timings; correct rule stated
- [ ] Part 5: TOCTOU named and the window described
- [ ] Part 6: loader handles all three defects; short-row exception type identified correctly
- [ ] Part 7: `SafeStore` passes all six behaviours; corruption-without-backup raises; corruption-with-backup recovers; failure injection leaves the file byte-identical with no `.tmp` debris
- [ ] Reflection complete

---

## Bonus Challenges

1. Make `atomic_write` preserve the original file's permissions (`os.stat` / `os.chmod`). Why does
   `mkstemp` not do this for you, and what is the security reason for its default?
2. Write `safe_update(path, transform)` that reads a file, applies `transform` to its text, and
   writes the result atomically — leaving the original untouched if `transform` raises.
3. Measure the cost of `fsync`: time 1,000 atomic writes with and without it. Is the difference what
   you expected? What does that tell you about why databases treat it as a deliberate cost?
4. Add `SafeStore.transaction()` as a context manager that batches many `set` calls into a single
   commit on exit — and rolls back if the block raises. Which of the four properties does this make
   harder to guarantee?
5. `SafeStore` keeps exactly one backup. Extend it to keep the last N versions, and explain what
   new failure mode you have introduced.
