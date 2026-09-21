# CS 101 · Quiz 11
## Week 11, Wednesday — In-Class Assessment

**Date:** Wednesday 9 December 2026 · 09:00–09:10 (start of L34) · Week 11
**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 10 material: files, the I/O boundary, exceptions, structured formats

---

### Question 1 (2 points)

A file contains `EXISTING`. State its contents immediately after `open(path, "w")` followed by
`close()`, with no read and no write performed. Then state, in one sentence, when the truncation
happens.

&nbsp;

&nbsp;

---

### Question 2 (2 points)

```python
try:
    risky()
except Exception:
    log("failed")
except ValueError:
    recover()
```

State what happens when `risky()` raises `ValueError`, and why. Name the rule about clause ordering
that this violates.

&nbsp;

&nbsp;

---

### Question 3 (2 points)

Name **two** of the four requirements for a crash-safe atomic write, and for each state the specific
failure that requirement prevents.

&nbsp;

&nbsp;

&nbsp;

---

### Question 4 (2 points)

`except BaseException:` and `except Exception:` differ in exactly one practically important way.
State it, name one exception class caught by the first but not the second, and say why a cleanup
handler in `atomic_write` should use the broader one.

&nbsp;

&nbsp;

---

### Question 5 (2 points)

A program checks `if os.path.exists(path):` and then opens the file on the next line. Name the class
of bug this creates, and state the one-line fix.

&nbsp;

&nbsp;

---

**Total: 10 points**

*CS 101 · Week 11 · Quiz 11 · © CSE Department*
