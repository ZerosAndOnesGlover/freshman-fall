---
assessment: Lab 8
course: CS 101
component: Labs
possible: 100
score:
status: not-started
started:
submitted:
source: "LAB 8 Hash Tables from Scratch.md"
---

# CS 101 · Lab 8
## Answer Sheet

**Assessment:** `LAB 8 Hash Tables from Scratch.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Part 1 — Both Hash Table Variants  (40 points)

`hash_table.py`: paste the five `✓` lines from `run_tests()`.

**Your answer:**



*Marks: ___ / 40*

---

### Part 2 — Load Factor vs. Performance  (25 points)

Both tables from `load_factor_experiment()` (two runs), then:
1. Chaining against 1 + α/2.
2. Open addressing near α = 0.9–0.95, against ½(1 + 1/(1−α)).
3. Why Python's dict resizes by about 2/3 while a chained table can wait until 0.75 or more.

**Your answer:**



*Marks: ___ / 25*

---

### Part 3 — Two-Sum  (15 points)

Paste the `✓ two_sum` output.

**Your answer:**



*Marks: ___ / 15*

---

### Part 4 — The `__hash__`/`__eq__` Contract  (20 points)

The investigation output, then:
1. Why `d[p2]` returns `"first"`.
2. Why Python makes `BadPoint` unhashable.

**Your answer:**



*Marks: ___ / 20*

---

### Reflection (required, not scored)

**Q1.** Chaining or open addressing for a general-purpose table, from your data.
**Q2.** What breaks if `_resize` copies the old buckets across.

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

