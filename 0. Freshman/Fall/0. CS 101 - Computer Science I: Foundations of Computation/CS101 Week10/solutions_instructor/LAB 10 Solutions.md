# CS 101: Week 10
## LAB 10 Solutions: INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Timings are machine-specific —
> grade the *ratios* and the conclusions, never the milliseconds.

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

## Part 4 — EAFP vs LBYL

Two independent runs, both showing the same shape:

| Scenario | LBYL | EAFP |
|---|---|---|
| Hit-heavy (run A) | 25.9 ms | **18.6 ms** |
| Miss-heavy (run A) | **14.8 ms** | 52.7 ms |
| Hit-heavy (run B) | 10.9 ms | **6.9 ms** |
| Miss-heavy (run B) | **6.6 ms** | 35.3 ms |

**EAFP wins on hits; LBYL wins on misses.** The rule: **entering a `try` is nearly free; *raising*
is expensive.** So ask forgiveness when failure is rare, check first when failure is routine.

**Why correctness outranks this.** The performance argument assumes both options are correct. For
filesystem access they are not — LBYL introduces a TOCTOU window (Part 5) that no timing advantage
compensates for. Performance decides between two correct designs; it never rescues an incorrect one.

Grade the **direction and the rule**, not the numbers. Absolute timings vary several-fold across
machines and Python builds.

---

## Part 5 — TOCTOU

**Expected answer.** Between `os.path.exists(path)` and `open(path)`, another process can delete,
move, or replace the file — including replacing it with a symlink to something the caller should not
be able to read. The `open` therefore still needs its handler, so the check adds no safety.

**Why it makes debugging harder:** it converts a deterministic failure into a rare one. Without the
check, a missing file fails every time and is fixed immediately. With it, the failure happens only
when the timing lines up — in production, under load, unreproducibly.

Bug class: **TOCTOU** — time-of-check to time-of-use. It is a recognised security category, not a
theoretical concern.

No-window version:

```python
try:
    with open(path, encoding="utf-8") as f:
        ...
except FileNotFoundError:
    ...
```

---

## Part 6 — Defensive CSV Loader

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

## Part 7 — SafeStore

### Reference implementation

```python
class SafeStore:
    def __init__(self, path, recover=True):
        self.path = Path(path)
        self.backup = self.path.with_suffix(self.path.suffix + ".bak")
        self._data = self._load(recover)

    def _load(self, recover):
        if not self.path.exists():
            return {}                        # a new store is not an error
        try:
            return self._read(self.path)
        except StoreCorrupt:
            if recover and self.backup.exists():
                data = self._read(self.backup)   # may itself raise — correct
                self._data = data
                self._commit(data)               # repair the main file
                return data
            raise

    @staticmethod
    def _read(p):
        try:
            text = p.read_text(encoding="utf-8")
        except OSError as e:
            raise StoreError(f"cannot read {p}: {e.strerror}") from e
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise StoreCorrupt(f"{p}: bad JSON at line {e.lineno} col {e.colno}: {e.msg}") from e
        if not isinstance(data, dict):
            raise StoreCorrupt(f"{p}: expected object, got {type(data).__name__}")
        return data

    def _commit(self, data):
        if self.path.exists():
            shutil.copy2(self.path, self.backup)
        payload = json.dumps(data, indent=2, sort_keys=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(payload); f.flush(); os.fsync(f.fileno())
            os.replace(tmp, self.path)
        except BaseException:
            os.unlink(tmp); raise

    def get(self, key, default=None):   return self._data.get(key, default)
    def set(self, key, value):          self._data[key] = value; self._commit(self._data)
    def delete(self, key):
        if key in self._data:
            del self._data[key]; self._commit(self._data); return True
        return False
    def keys(self):                     return sorted(self._data)
    def __len__(self):                  return len(self._data)
    def __contains__(self, key):        return key in self._data
```

### Verified transcript

```
basic:        keys ['a','b'] | len 2 | 'a' in s True | get('zz','DEFAULT') -> 'DEFAULT'
persistence:  SafeStore(p).keys() -> ['a','b']  after a fresh instance
delete:       delete('a') -> True ; delete('a') again -> False ; keys -> ['b']
backup:       .bak exists and holds the PREVIOUS version
no backup:    StoreCorrupt: solo.json: bad JSON at line 1 col 2: Expecting property name...
with backup:  main {'x':10,'y':20}, bak {'x':10}; after corrupting main, recovery gives ['x']
              and the main file is repaired to {'x': 10}
crash inject: store file byte-identical; leftover .tmp files: []
```

### 7.6 — the recovery question

**Expected answer.** The recovered store holds `{'x': 10}` rather than `{'x': 10, 'y': 20}` because
the backup is written **before** each commit, so it always lags by exactly one write. Corrupting the
main file therefore costs the most recent `set`.

**Is it acceptable?** For a configuration store, yes — losing one change beats losing the file. For
a payment ledger, no.

**Doing better** requires a **write-ahead log**: append the intended change to a separate log *and*
`fsync` it *before* touching the main file, so recovery can replay whatever the main file is
missing. That costs a second `fsync` per operation — roughly doubling the expensive part of every
write.

**The general trade-off is durability against throughput**, and it is exactly the choice real
databases expose (PostgreSQL's `synchronous_commit`, SQLite's `PRAGMA synchronous`). Award full
marks for naming the one-write lag and the durability/performance tension; award bonus credit for
"write-ahead log" or "journalling".

### 7.7 — failure injection

Verified: after raising between `mkstemp` and `os.replace`, the store file is **byte-identical** and
`list(dir.glob('*.tmp'))` is empty. A student whose temp file survives has caught `Exception`
instead of `BaseException`, or has no cleanup handler at all.

### Marking notes for Part 7

- **`_load` returning `{}` for a missing file** — a new store is not an error. Raising here is the
  most common design mistake.
- **`_read` used for both the main file and the backup.** A student who writes separate readers has
  duplicated the validation and will let one drift.
- **The backup copy must precede the write**, and must be skipped when the file does not yet exist —
  otherwise the first `set` raises `FileNotFoundError` from `shutil.copy2`.
- **`sort_keys=True`** is worth a mark: it makes the on-disk file diffable, so a version-control diff
  shows the change rather than a reshuffle.
- **Recovery must repair the main file**, not merely return the data. Otherwise the next start-up
  hits the same corruption.
- **`isinstance(data, dict)`** — valid JSON that is a list must be rejected. Several submissions
  will pass every other test and fail this one.

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
