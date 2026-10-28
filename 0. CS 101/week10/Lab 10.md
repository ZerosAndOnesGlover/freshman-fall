---
assessment: Lab 10
course: CS 101
component: Labs
possible: 100
score:
status: not-started
started:
submitted:
source: "LAB 10 Robust File Handling.md"
---

# CS 101 · Lab 10
## Answer Sheet

**Assessment:** `LAB 10 Robust File Handling.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Part 1 — Modes and the Truncation Hazard  (30 points)

1.1: the mode table; which modes truncate, and when.
1.2: the output, and what destroyed the data.
1.3: the surviving content after `atomic_write`, and whether any `.tmp` debris remained.

**Your answer:**



*Marks: ___ / 30*

---

### Part 2 — Encoding  (20 points)

1. The byte string; bytes needed by `café` and `日本語`.
2. What `errors="replace"` produced.
3. Why that is worse than the exception.
4. Your preferred encoding, and what happens to a program without `encoding=` on `cp1252`.

**Your answer:**



*Marks: ___ / 20*

---

### Part 3 — Exception Mechanics  (25 points)

3.1: both sequences; when `else` runs and why you would want it.
3.2: which clause catches in each ordering, and the rule.
3.3: two things `except:` catches that `except Exception:` does not, and why that matters.

**Your answer:**



*Marks: ___ / 25*

---

### Part 4 — A Defensive CSV Loader  (25 points)

1. Your `good` and `bad` lists.
2. The exception the short row raises, and why it is not `ValueError`.
3. What `line.split(",")` gives for the quoted-comma row.

**Your answer:**



*Marks: ___ / 25*

---

### Reflection (required, not scored)

1. The failure you would most likely have shipped before this lab.
2. The general habit that prevents the Part 1 class of bug.
3. When the loader should stop at the first bad row instead.

**Your answer:**



---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | ___ / 100 |
| **Percent** | ___ |
| **Graded** | ___ |

**Feedback:**

