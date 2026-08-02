# CS 101 — Lecture 31 (Week 10, Lecture 1)
## Files and the I/O Boundary

---

## 0. Where Programs Meet the World

Everything so far has happened inside one process. Data appeared as literals, was transformed, and
vanished when the program exited. This week your programs start **persisting** — and the moment
they do, three new categories of problem arrive:

1. **The data outlives the program**, so its *format* becomes a contract you must honour.
2. **The world can refuse.** Files go missing, permissions fail, disks fill. Code that assumed
   success now has to cope with failure — which is Thursday's lecture.
3. **Bytes are not text.** L28's encoding boundary stops being theoretical: every `open()` is a
   decision about it, whether or not you make that decision deliberately.

This lecture covers the mechanism; L32 covers failure; L33 covers the formats worth using.

---

## 1. The File Abstraction

A file is a **named, persistent sequence of bytes** with a current position. Reading advances the
position; writing advances it and stores. That is the entire model, and it is deliberately
minimal — the same abstraction covers a text document, a hard disk, a network socket, and your
keyboard. PROG 101 Week 8 develops that "everything is a file" idea at the system-call level; here
we use Python's layer on top of it.

```python
f = open("data.txt")      # opens for reading, text mode, default encoding
content = f.read()
f.close()                 # ← easy to forget, and forgetting matters
```

Never write it that way. Use a **context manager**:

```python
with open("data.txt") as f:
    content = f.read()
# f is closed here — guaranteed
```

The guarantee is what matters. Verified:

```python
f = open("t.txt")
with f: pass
f.closed                            # True

try:
    with open("t.txt") as g:
        raise ValueError("boom")
except ValueError:
    pass
g.closed                            # True — closed even though the body raised
```

**The file closes even when the block raises.** That is the whole point: an exception in the middle
of processing must not leak an open file handle. Handles are a finite OS resource, and a
long-running program that leaks them eventually fails with `OSError: Too many open files` — far
from the code that caused it.

Reading from a closed file is itself an error, not silent nonsense:

```python
h = open("t.txt"); h.close()
h.read()        # ValueError: I/O operation on closed file.
```

---

## 2. Modes: What Each One Does to an Existing File

This table is verified — each row was run against a file containing `"EXISTING"`:

| Mode | Initial position | Can read? | File afterwards | Missing file |
|---|---|---|---|---|
| `"r"` | 0 | ✓ | `'EXISTING'` | **`FileNotFoundError`** |
| `"w"` | 0 | ✗ | **`''` — truncated** | created |
| `"a"` | **8 (end)** | ✗ | `'EXISTING'` | created |
| `"r+"` | 0 | ✓ | `'EXISTING'` | `FileNotFoundError` |
| `"w+"` | 0 | ✓ | **`''` — truncated** | created |
| `"a+"` | **8 (end)** | ✓ | `'EXISTING'` | created |

Three things deserve emphasis.

**`"w"` truncates immediately, at `open()` time** — before you write a single byte. Opening a file
for writing "just to check something" has already destroyed it. This is the single most expensive
beginner mistake in file handling, and §7 shows the standard defence.

**`"a"` starts at the end** and, on POSIX, forces every write to the end regardless of any `seek`.
That makes it the correct mode for log files, and safe under concurrent appends from multiple
processes.

**`"x"` fails if the file exists:**

```python
open("t.txt", "x")     # FileExistsError: [Errno 17] File exists: 't.txt'
```

Use `"x"` when you intend to create something new and overwriting would be a bug — it converts a
silent data loss into a loud error.

---

## 3. Streaming vs Slurping

Three ways to read, with very different memory behaviour:

```python
with open("data.txt") as f:
    everything = f.read()          # ONE str — entire file in memory
    lines      = f.readlines()     # list of str — entire file, plus list overhead
    for line in f:                 # one line at a time — O(1) memory
        process(line)
```

A file object **is its own iterator** (`iter(f) is f` — verified `True`), and iterating yields lines
lazily. For a 10 GB log, the first two forms fail and the third works.

**Default to iteration.** Use `.read()` only when you genuinely need the whole thing at once — say,
to run a regex across the entire text — and when you know it is small.

Note that lines retain their trailing `"\n"`. Strip it if you are comparing or storing:

```python
for line in f:
    record = line.rstrip("\n")     # not .strip(), which also eats leading spaces
```

### The counting trap

Here is the Python cousin of a bug you will meet in PROG 101 Week 8:

```python
with open("lines.txt") as f:
    count = 0
    while True:
        line = f.readline()
        count += 1              # counts BEFORE checking
        if not line:
            break
```

Verified against three files:

| File | Correct | Count-then-check |
|---|---|---|
| `"a\nb\nc\n"` | 3 | **4** |
| `"a\nb\nc"` | 3 | **4** |
| `""` (empty) | 0 | **1** |

**It always overcounts by exactly one**, because `readline()` returns `""` at end-of-file and the
counter has already been incremented. The correct form tests the read itself:

```python
count = sum(1 for _ in open("lines.txt"))
```

> Worth comparing with C. There, the equivalent `while (!feof(f))` bug is **data-dependent** — it
> overcounts on a file ending with a newline and is correct on one that does not. Python's version
> is consistently wrong, which is oddly preferable: a bug that always fires is found immediately,
> while one that fires on some inputs reaches production. **The general rule in both languages is
> the same: check the result of the read, never a separate end-of-file flag.**

---

## 4. Encoding Is a Decision You Are Making Anyway

`open()` in text mode decodes bytes into `str`. If you do not name an encoding, one is chosen for
you — from the locale:

```python
import locale
locale.getpreferredencoding(False)      # 'UTF-8' on this machine
```

On another machine it may be `cp1252`. **A program that omits the encoding will read the same file
differently on different systems**, which is how "works on my laptop" data bugs are born.

Verified. A file containing `"café 日本語"` in UTF-8 is these bytes on disk:

```
b'caf\xc3\xa9 \xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'
```

Read three ways:

```python
open("enc.txt", encoding="utf-8").read()
# 'café 日本語'                                    ← correct

open("enc.txt", encoding="ascii").read()
# UnicodeDecodeError: ordinal not in range(128) at byte 3

open("enc.txt", encoding="ascii", errors="replace").read()
# 'caf�� ���������'                                ← corrupted, silently
```

The `errors="replace"` result is the dangerous one: **no exception, and the data is destroyed.**
Every non-ASCII byte became U+FFFD, irreversibly. Use `errors="replace"` only when you would rather
display something than nothing and you understand you are discarding information — never when the
data will be stored or re-encoded.

**Always pass `encoding=` explicitly.** `encoding="utf-8"` is the right default for essentially all
new text.

### Newline translation

Text mode also rewrites line endings:

```python
# file contains the bytes b'a\r\nb\n'
open("nl.txt").read()               # 'a\nb\n'      ← universal newlines: \r\n became \n
open("nl.txt", newline="").read()   # 'a\r\nb\n'    ← raw
```

Usually helpful — a Windows-authored file reads cleanly on Linux. Occasionally not: when writing
CSV you must pass `newline=""`, or the `csv` module's own `\r\n` gets translated again and you emit
blank lines between rows. L33 returns to this.

**For binary data, use `"rb"`/`"wb"` and skip text mode entirely.** No decoding, no newline
rewriting — you get exactly the bytes.

---

## 5. The Accumulator Pattern, Again

L29 established: build a list, then join once. Files present the same shape with a different
expensive operation.

```python
# WRONG — opens and closes the file n times
for record in records:
    with open("out.txt", "a") as f:
        f.write(record + "\n")

# RIGHT — one open, one close
with open("out.txt", "w", encoding="utf-8") as f:
    for record in records:
        f.write(record + "\n")
```

Each `open()` is a **system call**, costing on the order of a microsecond against the tens of
nanoseconds of a buffered write — a factor of roughly 100. The wrong version is not asymptotically
worse (both are Θ(n) writes) but the constant is brutal, and it is the same mistake as
`list.insert(0, x)` in a loop: **an expensive operation placed inside a loop that did not need it
there.**

For the read side, the equivalent is re-opening a file to answer repeated questions instead of
reading it once into a structure.

`writelines` does *not* add newlines, which surprises people:

```python
f.writelines(["a", "b"])          # writes 'ab', not 'a\nb'
f.writelines(f"{x}\n" for x in items)   # this is what you meant
```

---

## 6. Buffering, and Why Output Sometimes Vanishes

Writes are **buffered** — they accumulate in memory and reach the disk when the buffer fills, when
the file is closed, or when you call `flush()`. If a program crashes hard, buffered output is lost,
and the last thing you see is not the last thing that ran.

The `with` block closes (and therefore flushes) on the way out, including when an exception
propagates — which is another reason to use it. When you need a guarantee mid-stream:

```python
f.write(record)
f.flush()               # push to the OS
os.fsync(f.fileno())    # push the OS's own buffers to the physical device
```

`flush()` alone is not durability — it only moves data from Python's buffer into the operating
system's. `fsync` is what survives a power cut, and it is genuinely slow, which is why databases
treat it as a deliberate cost rather than a default.

---

## 7. Reading and Writing Without Losing Data

The naive write has a failure mode worth seeing:

```python
t = Path("naive.txt")
t.write_text("GOOD DATA")
try:
    with open(t, "w") as f:         # ← truncates at open()
        raise RuntimeError("crash before writing")
except RuntimeError:
    pass
t.read_text()        # ''  ← the original data is gone
```

**Opening for writing destroyed the file before anything went wrong.** Any crash, exception, or
power loss between `open` and the completed write leaves you with nothing — not the old version and
not the new one.

The fix is to **write elsewhere and rename**, which L33 develops in full. The one-line summary:
`os.replace` is atomic on POSIX, so the file is either entirely the old content or entirely the
new, never a truncated ruin.

---

## 8. Summary

| Idea | Takeaway |
|---|---|
| Always use `with` | Closes even when the body raises — verified |
| `"w"` truncates at `open()` | Before any write; the classic data-loss bug |
| `"a"` starts at the end | Correct for logs; safe under concurrent appends |
| `"x"` fails if the file exists | Turns silent overwrite into a loud error |
| Iterate, don't slurp | `for line in f` is O(1) memory; `.read()` is O(file) |
| Count-then-check overcounts by 1 | Always — test the read, not a separate flag |
| Pass `encoding=` explicitly | Otherwise the locale decides, and it differs per machine |
| `errors="replace"` destroys data silently | No exception, irreversible corruption |
| One `open`, many writes | Each `open` is a syscall ≈ 100× a buffered write |
| Buffered output can vanish on a crash | `flush` reaches the OS; `fsync` reaches the disk |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** A file `t.txt` contains `EXISTING`. For each mode, state the file's contents after
`open("t.txt", mode)` followed immediately by closing it — no reads or writes in between.

```
"r"    "w"    "a"    "r+"    "w+"    "x"
```

**2. (Explain.)** This function reports 4 for a 3-line file and 1 for an empty file. Explain
precisely why, and give the one-line correct version.

```python
def count_lines(path):
    with open(path) as f:
        n = 0
        while True:
            line = f.readline()
            n += 1
            if not line:
                break
    return n
```

**3. (Build.)** Write `copy_filtered(src, dst, predicate)` that copies only the lines of `src`
satisfying `predicate`, streaming (never holding the whole file), with explicit UTF-8 encoding, and
leaving `dst` untouched if `src` does not exist.

**4. (Stretch.)** `open(path, "w")` truncates the file at open time. Show a two-line snippet where
this destroys data despite the program never writing anything wrong, then describe the standard fix
and why it works.

### Answers

**1.** `'EXISTING'`, **`''`**, `'EXISTING'`, `'EXISTING'`, **`''`**, and `"x"` raises
`FileExistsError`.

Only `"w"` and `"w+"` truncate, and they do so **at `open()`** — no write is required. `"a"` and
`"a+"` position at byte 8 (the end) but leave the content intact. `"r"` and `"r+"` require the file
to exist; `"r"` on a missing file raises `FileNotFoundError: [Errno 2] No such file or directory`.

**2.** `readline()` returns `""` at end-of-file, and the counter is incremented **before** the check
for it. So the final iteration — the one that discovers EOF — has already added 1. It therefore
overcounts by exactly one, **independent of the file's contents**:

| File | Correct | This function |
|---|---|---|
| `"a\nb\nc\n"` | 3 | 4 |
| `"a\nb\nc"` | 3 | 4 |
| `""` | 0 | 1 |

Correct version:

```python
def count_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)
```

**The general rule is to test the result of the read itself**, not a separate end-of-file signal.
The C equivalent, `while (!feof(f))`, has the same root cause but is *data-dependent* — it
overcounts a file ending in a newline and is correct on one that does not. Python's version being
consistently wrong is the better failure: it shows up on the first test rather than in production.

**3.**

```python
def copy_filtered(src, dst, predicate):
    """Copy lines of src satisfying predicate into dst. Streams; never slurps."""
    with open(src, encoding="utf-8") as fin:          # opens src FIRST
        with open(dst, "w", encoding="utf-8") as fout:
            for line in fin:                          # O(1) memory
                if predicate(line):
                    fout.write(line)
```

The ordering is the subtle part. **`src` must be opened before `dst`.** Written the other way
round, a missing `src` still leaves `dst` created and truncated, because `open(dst, "w")` executes
first and truncates immediately — exactly the §7 failure. With this ordering, a missing `src` raises
`FileNotFoundError` before `dst` is touched at all.

Note also that `line` keeps its trailing newline, so writing it back needs no `+ "\n"`.

**4.**

```python
Path("data.txt").write_text("IRREPLACEABLE")
with open("data.txt", "w") as f:      # truncates HERE
    raise RuntimeError("network fetch failed")
# data.txt is now ''
```

Verified: the file reads back as `''`. Nothing was written incorrectly — the *opening* destroyed it,
and the program then failed for an unrelated reason.

**The standard fix is write-to-temporary-then-rename:**

```python
import os, tempfile
from pathlib import Path

def atomic_write(path, data):
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)        # atomic on POSIX
    except BaseException:
        os.unlink(tmp)               # never leave debris
        raise
```

**Why it works:** the original file is not opened for writing at all, so it cannot be truncated. The
new content is built in a separate file, and `os.replace` swaps the directory entry in a single
atomic operation — any observer sees either the complete old file or the complete new one, never a
half-written state. Verified: after a simulated crash mid-write, the target still held its previous
content and no `.tmp` debris remained.

The temporary must live **in the same directory** as the target, because `os.replace` is only
atomic within a filesystem. And `fsync` before the rename is what makes the guarantee survive a
power failure rather than merely a process crash.

---

## Reading

- **Guttag, Ch. 4.6** — files (primary)
- **Python docs — `io` module, "Text I/O"** — the encoding and newline discussion of §4
- **Python docs — Built-in Functions: `open`** — read the full mode and `errors` tables

---

*CS 101 · Week 10 · Lecture 31 (Wed) · © CSE Department*
