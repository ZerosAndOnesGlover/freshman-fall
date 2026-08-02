# CS 101 — Quiz 11 Solutions (Instructor)
## Week 11, Wednesday

**Total: 10 points** · Award partial credit generously where the reasoning is right and the
terminology is imprecise.

---

### Question 1 (2 points)

**Contents: empty.** The file is truncated to zero bytes. *(1 pt)*

**Truncation happens at `open()`**, not at write time — opening in `"w"` mode destroys the contents
immediately, before any write call. *(1 pt)*

*Common error:* "nothing happens because we didn't write." This is the single most damaging file-I/O
misconception, since it means data loss on a code path that never intended to write. Full deduction.

---

### Question 2 (2 points)

`log("failed")` runs; `recover()` is **unreachable**. *(1 pt)*

`ValueError` is a subclass of `Exception`, and Python tests `except` clauses **top to bottom, taking
the first match**. The broad clause is listed first, so it catches everything and the specific clause
below it can never run. *(1 pt)*

The rule: **order except clauses from most specific to most general.** Accept "specific before
general" or equivalent.

*Note:* Python does not warn about this — the code runs silently. Students who mention that deserve
credit for the observation, but it is not required.

---

### Question 3 (2 points)

Any **two** of the four, 1 point each — the requirement *and* its specific failure mode:

| Requirement | Prevents |
|---|---|
| Temp file in the **same directory** as the target | `os.replace` across filesystems is not atomic; a temp in `/tmp` can break the guarantee |
| **`fsync`** before the rename | Power loss after rename but before the data reaches disk leaves an empty or partial file |
| **`os.replace`**, not `os.rename` | `os.rename` fails on Windows when the destination exists |
| Cleanup under **`except BaseException`** | Ctrl-C (`KeyboardInterrupt`) during the write leaves an orphaned temp file |

*Marking:* the requirement alone is worth ½; the correct paired failure earns the rest. Reject vague
answers like "so it's safe."

---

### Question 4 (2 points)

`except Exception:` does **not** catch `KeyboardInterrupt`, `SystemExit`, or `GeneratorExit`; these
inherit from `BaseException` directly, deliberately placed outside `Exception` so that ordinary
error-handling code does not swallow them. *(1 pt — the distinction plus any one named class)*

`atomic_write`'s handler should use `BaseException` because its job is **cleanup, not recovery**: it
deletes the temp file and immediately **re-raises**. Ctrl-C during a write should still terminate the
program — but it should not leave a stray temp file behind. *(1 pt)*

*Full marks require the re-raise.* A student who says "catch BaseException so we can handle Ctrl-C"
without noting that the exception is re-raised has described exactly the anti-pattern the broader
clause is normally warned against.

---

### Question 5 (2 points)

**TOCTOU** — time-of-check to time-of-use. *(1 pt)* The file can be deleted, created, or replaced in
the window between the check and the open, so the check guarantees nothing about the open.

**Fix:** drop the check and just open the file, handling `FileNotFoundError`. *(1 pt)* This is
**EAFP** rather than LBYL — the open is atomic with respect to its own success, so the exception
carries information the check cannot.

```python
try:
    with open(path) as f: ...
except FileNotFoundError:
    ...
```

*Accept* "use EAFP / try-except instead of checking first." *Do not accept* "check again after
opening."

---

*CS 101 · Week 11 · Quiz 11 Solutions · Instructor copy — do not distribute*
