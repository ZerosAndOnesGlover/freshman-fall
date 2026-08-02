# CS 101 — Lecture 32 (Week 10, Lecture 2)
## Exceptions: Error Handling as Control Flow

---

## 0. The Problem Files Created

Yesterday every example assumed success. Real I/O does not cooperate: files are missing, paths are
directories, permissions are denied, disks fill, and encodings disagree. A program that ignores
this does not merely fail — it fails *late*, far from the cause, with a traceback that points at
the wrong line.

The answer is not to check everything before doing it. It is to have a **separate channel for
failure**, so that the normal path stays readable and errors cannot be silently ignored. That
channel is exceptions.

---

## 1. Exceptions Are Control Flow, Not Disasters

An exception **unwinds** the call stack until something catches it. Nothing about that is
inherently exceptional in the everyday sense — `StopIteration` ends every `for` loop you have ever
written.

```python
try:
    risky()
except SomeError:
    handle()
```

Compare with C, which has no exceptions and must return error codes:

```c
if (parse(s, &value) != 0) { /* handle */ }
```

The C style has a fatal weakness: **the caller can ignore the return value**, and nothing stops
them. An unhandled exception, by contrast, terminates the program with a traceback. The default
behaviour is loud — which is exactly right, because a silently wrong answer is worse than a crash.

---

## 2. The Hierarchy, and Why Clause Order Matters

Exceptions form an inheritance tree. Verified:

```python
issubclass(FileNotFoundError, OSError)          # True
issubclass(ZeroDivisionError, ArithmeticError)  # True
issubclass(ArithmeticError, Exception)          # True
issubclass(KeyboardInterrupt, Exception)        # False   ← note
issubclass(KeyboardInterrupt, BaseException)    # True
```

```
BaseException
├── KeyboardInterrupt        ← Ctrl-C
├── SystemExit               ← sys.exit()
└── Exception                ← everything you should normally catch
    ├── ArithmeticError → ZeroDivisionError
    ├── LookupError     → IndexError, KeyError
    ├── OSError         → FileNotFoundError, PermissionError, IsADirectoryError
    ├── ValueError      → UnicodeDecodeError
    └── TypeError, AttributeError, NameError, …
```

**`except` clauses are tested in order, and the first match wins.** So a broad clause placed first
makes every later clause unreachable:

```python
try:
    open("missing.txt")
except OSError:                 # ← matches first
    ...
except FileNotFoundError:       # ← UNREACHABLE
    ...
```

Verified: the broad-first version is caught by `OSError`; reversing the clauses gives
`FileNotFoundError`. Python does not warn you about the dead clause.

**Rule: order from most specific to most general.**

---

## 3. `try` / `except` / `else` / `finally`

All four parts, and the exact order they run in — verified:

```python
def demo(fail):
    try:
        log("try")
        if fail: raise ValueError("x")
        log("try-end")
    except ValueError:
        log("except")
    else:
        log("else")
    finally:
        log("finally")
```

| | Sequence |
|---|---|
| No exception | `try` → `try-end` → **`else`** → `finally` |
| Exception raised | `try` → **`except`** → `finally` |

- **`else`** runs only when the `try` block completed *without* an exception. Its purpose is to keep
  the `try` block as small as possible — only the operation that might fail belongs there, and
  everything that follows on success goes in `else`. That matters because a wide `try` can catch an
  exception from code you never intended to guard.
- **`finally`** runs on **every** path — success, handled exception, unhandled exception, even
  `return`. It is for cleanup that must happen regardless.

```python
def f():
    try:
        return "from try"
    finally:
        cleanup()          # runs, and the return value is still "from try"
```

> **Never `return` from a `finally` block.** It overrides the `try` block's return *and silently
> discards any in-flight exception* — turning a crash into a wrong answer. Python 3.14 now emits
> `SyntaxWarning: 'return' in a 'finally' block`, which is a good sign of how bad an idea it is.

In practice, prefer a **context manager** (`with`) over `try`/`finally` for resources. `with` is
`finally` with the cleanup written once, in the resource's own class, rather than at every use
site.

---

## 4. EAFP vs LBYL

Two philosophies:

```python
# LBYL — Look Before You Leap
if os.path.exists(path):
    with open(path) as f: ...

# EAFP — Easier to Ask Forgiveness than Permission
try:
    with open(path) as f: ...
except FileNotFoundError:
    ...
```

Python idiom favours EAFP, for two distinct reasons.

### The correctness reason: a race condition

Between `os.path.exists(path)` returning `True` and `open(path)` executing, **another process can
delete the file.** The check does not make the open safe; it only makes the failure rarer and
therefore harder to reproduce. This is a **TOCTOU** bug — time-of-check to time-of-use — and it is a
genuine security category, not a theoretical worry: privilege-escalation exploits are built on
exactly this window.

EAFP has no window. The open either succeeds or raises, atomically.

### The performance reason: it depends on the hit rate

Measured over 200,000 dictionary lookups:

| Scenario | LBYL | EAFP |
|---|---|---|
| Key present (hit-heavy) | 25.9 ms | **18.6 ms** |
| Key absent (miss-heavy) | **14.8 ms** | 52.7 ms |

**Setting up a `try` is nearly free; *raising* is expensive.** So EAFP wins when the exception is
rare and loses badly when it is common. If failure is the normal case — validating untrusted input,
say — check first. If failure is genuinely exceptional, ask forgiveness.

The correctness argument outranks the performance one. Where a race is possible, EAFP is not merely
faster on average, it is the only correct option.

---

## 5. The Three Ways to Get Error Handling Wrong

### 5.1 Bare `except`

```python
try:
    return int(user_input)
except:                  # ← catches EVERYTHING
    return None
```

A bare `except` catches `BaseException`, which includes **`KeyboardInterrupt`** and **`SystemExit`**.
Your program becomes un-interruptible by Ctrl-C and can ignore its own shutdown. It also catches
`NameError` from your typo three lines down, and reports it as bad user input.

Write `except Exception:` at minimum, and name the specific exception whenever you can.

### 5.2 Swallowing

```python
try:
    process(record)
except Exception:
    pass                 # ← the error happened; nobody will ever know
```

The failure is invisible. Data is silently dropped, and the symptom appears somewhere else entirely.
If you genuinely intend to continue, **say so and record it**:

```python
except (ValueError, KeyError) as exc:
    logging.warning("skipping malformed record %r: %s", record, exc)
    skipped += 1
```

### 5.3 Catching too much, too widely

```python
try:
    config = load(path)
    result = compute(config)      # ← not what you meant to guard
    save(result, out)             # ← nor this
except OSError:
    print("could not read config")
```

A disk error inside `save` now reports "could not read config". Keep the `try` block to the single
operation that can fail, and move the rest to `else`.

---

## 6. Raising Well

```python
if not path.exists():
    raise FileNotFoundError(f"config file not found: {path}")

if timeout < 0:
    raise ValueError(f"timeout must be non-negative, got {timeout!r}")
```

Two habits. **Choose the type that already exists** — `ValueError` for a bad value, `TypeError` for
a wrong type, `KeyError` for a missing key, `FileNotFoundError` for a missing file. Callers can then
catch precisely. And **put the offending value in the message**, using `!r` so `'5'` is
distinguishable from `5` (the L06 lesson, now earning its keep).

### Chaining preserves the cause

```python
try:
    raise ValueError("original")
except ValueError as e:
    raise RuntimeError("wrapper") from e
```

Verified: the `RuntimeError` carries `__cause__` pointing at the `ValueError`, and the traceback
shows both — *"The above exception was the direct cause of the following exception."* Use `from e`
whenever you translate a low-level failure into a domain-level one; without it you keep the new
message and lose the diagnosis.

### Custom exceptions

```python
class ConfigError(Exception):
    """Base for every configuration problem."""

class MissingKey(ConfigError):
    def __init__(self, key):
        super().__init__(f"missing required key: {key!r}")
        self.key = key
```

Verified: `except ConfigError` catches `MissingKey`, and the handler can still read `e.key`.

**Define a base class per subsystem, then specific subclasses.** Callers who care about the detail
catch the subclass; callers who just want "anything from the config layer" catch the base. Attaching
structured data (`self.key`) lets a handler act on the failure rather than merely reformatting a
string.

---

## 7. What a Good Error Message Contains

Python's own are a decent model:

```python
try:
    open("missing.txt")
except OSError as e:
    e.errno       # 2
    e.strerror    # 'No such file or directory'
    e.filename    # 'missing.txt'
```

Three ingredients: **what went wrong**, **which thing it went wrong on**, and **a code for
programmatic handling**. Compare:

| Bad | Better |
|---|---|
| `"Error"` | `"config file not found: /etc/app.conf"` |
| `"Invalid input"` | `"timeout must be non-negative, got -5"` |
| `"Failed to parse"` | `"line 47: expected 3 fields, got 5"` |

The message is read by someone at 3 a.m. who does not have your source open. Say what you were
trying to do, what you got, and where.

---

## 8. Summary

| Idea | Takeaway |
|---|---|
| Exceptions are a separate channel for failure | Unignorable by default, unlike return codes |
| Order clauses specific → general | A broad clause first makes later ones unreachable |
| `else` keeps the `try` block small | Only the risky operation belongs in `try` |
| `finally` always runs | Never `return` from it — 3.14 warns |
| EAFP avoids TOCTOU races | The check does not make the use safe |
| Exceptions are cheap to try, costly to raise | 18.6 ms vs 52.7 ms — depends on the hit rate |
| Bare `except` catches Ctrl-C | Use `except Exception:` at minimum |
| `raise ... from e` preserves the cause | Otherwise the diagnosis is lost |
| Messages need what, which, and where | Written for someone without your source |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Give the exact sequence of appended strings for `demo(False)` and `demo(True)`.

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
```

**2. (Explain.)** This code never reaches its second clause, and Python gives no warning. Explain
why, and state the general rule.

```python
try:
    open("missing.txt")
except OSError:
    print("os error")
except FileNotFoundError:
    print("not found")
```

**3. (Build.)** Write `load_config(path)` that returns a dict from a JSON file, raising
`ConfigError` (your own type) for a missing file, unreadable file, or malformed JSON — preserving
the original cause in each case. Define the exception classes too.

**4. (Stretch.)** `if os.path.exists(p): open(p)` looks safer than a bare `open(p)`. Explain why it
is not, name the bug class, and give the measured circumstances under which the alternative is
nonetheless the slower choice.

### Answers

**1.**

```
demo(False) -> ['try', 'try-end', 'else', 'finally']
demo(True)  -> ['try', 'except', 'finally']
```

`else` runs **only** when the `try` block completes without raising — so it is absent from the
second. `finally` runs on **both** paths, and would also run if the exception were unhandled or if
the function returned early. Note `"try-end"` is absent from the failing run because `raise`
transfers control immediately.

**2.** `except` clauses are checked **in written order**, and `FileNotFoundError` is a **subclass**
of `OSError` (verified: `issubclass(FileNotFoundError, OSError)` is `True`). The first clause
therefore matches every `FileNotFoundError` too, and the second can never run. Verified: the
broad-first version prints `"os error"`; swapping the clauses prints `"not found"`.

Python does not warn, because a later clause *can* legitimately be unreachable only for some
subclasses and the general case is undecidable.

**The rule: order `except` clauses from most specific to most general** — subclasses before their
base classes, exactly as you would order `if`/`elif` from narrow to broad.

**3.**

```python
import json
from pathlib import Path


class ConfigError(Exception):
    """Base for every configuration failure."""


class ConfigNotFound(ConfigError):
    pass


class ConfigInvalid(ConfigError):
    pass


def load_config(path):
    """Load a JSON config. Raises ConfigError (or a subclass) on any failure."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ConfigNotFound(f"config file not found: {path}") from exc
    except OSError as exc:
        raise ConfigError(f"could not read config {path}: {exc.strerror}") from exc

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ConfigInvalid(
            f"{path}: malformed JSON at line {exc.lineno} column {exc.colno}: {exc.msg}"
        ) from exc

    if not isinstance(data, dict):
        raise ConfigInvalid(f"{path}: expected a JSON object, got {type(data).__name__}")
    return data
```

Four things earn the marks. **`FileNotFoundError` is caught before `OSError`** — specific first, per
Q2. **`from exc` on every re-raise** keeps the original traceback, so a permissions problem is still
diagnosable through the wrapper. **Every message names the file and the position**, satisfying §7.
And the **base class `ConfigError`** lets a caller write `except ConfigError` to mean "anything wrong
with configuration" without enumerating the subclasses.

The final `isinstance` check matters more than it looks: valid JSON can be a list, a string, or a
number, so a syntactically perfect file can still be the wrong *shape*.

**4.** It is not safer because of a **race condition**. Between `os.path.exists(p)` returning `True`
and `open(p)` running, another process can delete or replace the file. The check narrows the window
but does not close it — and by making the failure rare, it makes the eventual crash harder to
reproduce and diagnose. The `open` still needs its exception handler, so the check has added no
safety at all.

The bug class is **TOCTOU** — time-of-check to time-of-use. It is a real security category: attacks
replace the checked file with a symlink in the gap, turning a permitted read into a privileged one.

**When LBYL is nonetheless faster:** when the failure is the *common* case. Measured over 200,000
dictionary lookups, EAFP beat LBYL on hits (18.6 ms vs 25.9 ms) because entering a `try` costs
almost nothing — but lost badly on misses (52.7 ms vs 14.8 ms), because actually **raising** an
exception is expensive. So for validating untrusted input, where most inputs are expected to be
bad, checking first is reasonable.

That performance argument never overrides the correctness one. Where a race is possible — anything
touching the filesystem or another process — EAFP is the only correct choice regardless of the hit
rate.

---

## Reading

- **Guttag, Ch. 7** — exceptions and assertions (primary)
- **Python docs — Errors and Exceptions tutorial** — read §8.3 through §8.6
- **Python docs — Built-in Exceptions** — skim the hierarchy diagram; know where `OSError` sits

---

*CS 101 · Week 10 · Lecture 32 (Thu) · © CSE Department*
